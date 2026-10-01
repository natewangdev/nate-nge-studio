"""Main application window."""

from __future__ import annotations

import logging
from typing import Any

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from nge_studio.catalog.discover import discover_catalog
from nge_studio.catalog.models import Script, merge_launch_parameters, merge_script_params
from nge_studio.hotkeys.win32 import GlobalHotkeys, HotkeyRegistrationError, dispatch_hotkey_message
from nge_studio.logging_bridge.qt_handler import QtLogHandler, attach_nge_handler, detach_handler
from nge_studio.runner.service import RunState, ScriptRunner
from nge_studio.settings.store import DEFAULT_MAIN_SPLITTER_STRETCH, SettingsStore
from nge_studio.ui.styles import APP_QSS
from nge_studio.ui.widgets.catalog_panel import CatalogPanel
from nge_studio.ui.widgets.log_panel import LogPanel
from nge_studio.ui.widgets.param_form import ParamForm
from nge_studio.window_pick.picker import WindowPickError, pick_at_cursor

log = logging.getLogger("nge.studio.ui")


class MainWindow(QMainWindow):
    log_line = Signal(str)
    state_changed = Signal(object, object)
    run_error = Signal(str)
    run_hung = Signal()
    run_finished = Signal()

    def __init__(
        self,
        *,
        settings_store: SettingsStore | None = None,
        engine_factory: Any | None = None,
    ) -> None:
        super().__init__()
        self.setWindowTitle("NGE-STUDIO")
        self.resize(1180, 720)
        self.setStyleSheet(APP_QSS)

        self._store = settings_store or SettingsStore()
        self._settings, warn = self._store.load()
        self._selected: Script | None = None
        self._manifest_defaults = None
        self._picking = False
        self._log_handler: QtLogHandler | None = None
        self._hotkeys: GlobalHotkeys | None = None
        self._splitter_save_timer = QTimer(self)
        self._splitter_save_timer.setSingleShot(True)
        self._splitter_save_timer.setInterval(300)
        self._splitter_save_timer.timeout.connect(self._persist_splitter_sizes)

        brand = QLabel("NGE-STUDIO")
        brand.setObjectName("brandLabel")
        hint = QLabel("游戏脚本管理 · 基于 NGE2")
        hint.setObjectName("hintLabel")

        self.catalog = CatalogPanel()
        self.params = ParamForm()
        self.logs = LogPanel()

        self.btn_start = QPushButton("启动")
        self.btn_start.setObjectName("primaryButton")
        self.btn_pause = QPushButton("暂停")
        self.btn_stop = QPushButton("结束")
        self.btn_stop.setObjectName("dangerButton")
        self.status = QLabel("就绪")
        self.status.setObjectName("hintLabel")

        controls = QHBoxLayout()
        controls.addWidget(self.btn_start)
        controls.addWidget(self.btn_pause)
        controls.addWidget(self.btn_stop)
        controls.addStretch(1)
        controls.addWidget(self.status)

        left = QWidget()
        left.setMinimumWidth(160)
        left_l = QVBoxLayout(left)
        left_l.addWidget(brand)
        left_l.addWidget(hint)
        left_l.addWidget(self.catalog, stretch=1)

        center = QWidget()
        center.setMinimumWidth(240)
        center_l = QVBoxLayout(center)
        center_l.addWidget(QLabel("启动参数"))
        center_l.addWidget(self.params, stretch=1)
        center_l.addLayout(controls)

        right = QWidget()
        right.setMinimumWidth(240)
        right_l = QVBoxLayout(right)
        right_l.addWidget(QLabel("实时日志"))
        right_l.addWidget(self.logs, stretch=1)

        self._main_splitter = QSplitter()
        self._main_splitter.addWidget(left)
        self._main_splitter.addWidget(center)
        self._main_splitter.addWidget(right)
        for index, stretch in enumerate(DEFAULT_MAIN_SPLITTER_STRETCH):
            self._main_splitter.setStretchFactor(index, stretch)
        self._main_splitter.setChildrenCollapsible(False)
        self._main_splitter.splitterMoved.connect(self._on_splitter_moved)
        self.setCentralWidget(self._main_splitter)

        self.runner = ScriptRunner(
            engine_factory=engine_factory,
            on_state=lambda s, k: self.state_changed.emit(s, k),
            on_error=lambda m: self.run_error.emit(m),
            on_hung=lambda: self.run_hung.emit(),
            on_finished=lambda: self.run_finished.emit(),
        )

        self.catalog.script_selected.connect(self._on_script_selected)
        self.params.pick_btn.clicked.connect(self._begin_window_pick)
        self.params.reset_btn.clicked.connect(self._reset_defaults)
        self.btn_start.clicked.connect(self._on_start_clicked)
        self.btn_pause.clicked.connect(self._on_pause_clicked)
        self.btn_stop.clicked.connect(self._on_stop_clicked)
        self.log_line.connect(self.logs.append_line, Qt.ConnectionType.QueuedConnection)
        self.state_changed.connect(self._on_state, Qt.ConnectionType.QueuedConnection)
        self.run_error.connect(self._show_error, Qt.ConnectionType.QueuedConnection)
        self.run_hung.connect(
            lambda: self._show_error("脚本在结束宽限期内未返回，可能已挂起"),
            Qt.ConnectionType.QueuedConnection,
        )
        self.run_finished.connect(self._on_run_finished, Qt.ConnectionType.QueuedConnection)

        self._load_catalog()
        if warn:
            QMessageBox.warning(self, "设置", warn)
        QTimer.singleShot(0, self._setup_hotkeys)
        QTimer.singleShot(0, self._restore_splitter_sizes)

    def nativeEvent(self, eventType, message):  # noqa: N802
        try:
            from ctypes import wintypes

            if eventType in (b"windows_generic_MSG", "windows_generic_MSG"):
                msg = wintypes.MSG.from_address(int(message))
                handled = dispatch_hotkey_message(
                    int(msg.message),
                    int(msg.wParam),
                    {
                        "start": self._on_start_clicked,
                        "pause": self._on_pause_clicked,
                        "stop": self._on_stop_clicked,
                    },
                )
                if handled:
                    return True, 0
        except Exception:
            log.exception("快捷键消息处理失败")
        return super().nativeEvent(eventType, message)

    def closeEvent(self, event) -> None:  # noqa: N802
        try:
            if self.runner.state != RunState.IDLE:
                self.runner.stop()
        except Exception:
            pass
        if self._hotkeys:
            self._hotkeys.clear()
        if self._log_handler:
            detach_handler(self._log_handler)
        self._persist_selected_params()
        self._persist_splitter_sizes()
        super().closeEvent(event)

    def _on_splitter_moved(self, *_args: object) -> None:
        self._splitter_save_timer.start()

    def _restore_splitter_sizes(self) -> None:
        saved = self._settings.main_splitter_sizes()
        if saved is not None:
            self._main_splitter.setSizes(saved)
            return
        total = max(self._main_splitter.size().width(), self.width() - 40, 800)
        weights = DEFAULT_MAIN_SPLITTER_STRETCH
        weight_sum = sum(weights)
        self._main_splitter.setSizes([max(160, total * w // weight_sum) for w in weights])

    def _persist_splitter_sizes(self) -> None:
        sizes = [int(v) for v in self._main_splitter.sizes()]
        self._settings.set_main_splitter_sizes(sizes)
        try:
            self._store.save(self._settings)
        except Exception as exc:
            log.warning("保存布局失败: %s", exc)

    def _setup_hotkeys(self) -> None:
        try:
            wid = int(self.winId())
            self._hotkeys = GlobalHotkeys(wid)
            self._hotkeys.register_all(self._settings.hotkeys)
            self.statusBar().showMessage(
                f"全局快捷键: 启动 {self._settings.hotkeys['start']['key']} / "
                f"暂停 {self._settings.hotkeys['pause']['key']} / "
                f"结束 {self._settings.hotkeys['stop']['key']}",
                8000,
            )
        except HotkeyRegistrationError as exc:
            QMessageBox.warning(self, "快捷键", str(exc))
        except Exception as exc:
            QMessageBox.warning(self, "快捷键", f"注册失败: {exc}")

    def _load_catalog(self) -> None:
        try:
            games = discover_catalog()
        except Exception as exc:
            QMessageBox.critical(self, "目录", f"加载脚本目录失败:\n{exc}")
            games = []
        self.catalog.set_games(games)

    def _on_script_selected(self, script: Script | None) -> None:
        self._persist_selected_params()
        self._selected = script
        if script is None:
            self.params.set_script_param_schema([])
            return
        self._manifest_defaults = script.manifest.defaults
        overlay = self._store.get_launch_overlay(self._settings, script.key)
        merged = merge_launch_parameters(script.manifest.defaults, overlay)
        self.params.set_parameters(merged)
        sp_overlay = self._store.get_script_params_overlay(self._settings, script.key)
        sp_merged = merge_script_params(script.manifest.script_params, sp_overlay)
        self.params.set_script_param_schema(script.manifest.script_params, sp_merged)

    def _reset_defaults(self) -> None:
        if self._selected is None:
            return
        self.params.set_parameters(self._selected.manifest.defaults)
        self.params.set_script_param_schema(
            self._selected.manifest.script_params,
            merge_script_params(self._selected.manifest.script_params, None),
        )

    def _persist_selected_params(self) -> None:
        if self._selected is None:
            return
        try:
            params = self.params.get_parameters()
            script_params = self.params.get_script_params()
        except Exception:
            return
        self._store.set_launch_overlay(
            self._settings,
            self._selected.key,
            params,
            script_params=script_params,
        )
        try:
            self._store.save(self._settings)
        except Exception as exc:
            log.warning("保存设置失败: %s", exc)

    def _begin_window_pick(self) -> None:
        if self._picking:
            return
        self._picking = True
        self.status.setText("点选模式：将光标移到目标窗口后点击左键（Esc 取消）")
        self.grabMouse(QCursor(Qt.CursorShape.CrossCursor))
        self.grabKeyboard()

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if self._picking and event.button() == Qt.MouseButton.LeftButton:
            self._picking = False
            self.releaseMouse()
            self.releaseKeyboard()
            try:
                result = pick_at_cursor()
                self.params.set_hwnd(result.hwnd, result.title)
                self.status.setText(f"已选择窗口: {result.title}")
            except WindowPickError as exc:
                QMessageBox.information(self, "窗口点选", str(exc))
                self.status.setText("就绪")
            return
        super().mousePressEvent(event)

    def keyPressEvent(self, event) -> None:  # noqa: N802
        if self._picking and event.key() == Qt.Key.Key_Escape:
            self._picking = False
            self.releaseMouse()
            self.releaseKeyboard()
            self.status.setText("已取消点选")
            return
        super().keyPressEvent(event)

    def _on_start_clicked(self) -> None:
        state = self.runner.state
        if state == RunState.PAUSED:
            self.runner.resume()
            return
        if state != RunState.IDLE:
            QMessageBox.information(self, "运行", "已有脚本在运行，同一时间只能运行一个")
            return
        if self._selected is None:
            QMessageBox.information(self, "运行", "请先选择一个脚本")
            return
        try:
            params = self.params.get_parameters()
            params.validate_for_start()
            script_params = self.params.get_script_params()
        except Exception as exc:
            QMessageBox.warning(self, "参数无效", str(exc))
            return
        self._persist_selected_params()
        self.logs.clear()
        self._attach_log_handler()
        logging.getLogger("nge.studio").info("正在启动脚本: %s", self._selected.key)
        try:
            self.runner.start(self._selected, params, script_params=script_params)
        except Exception as exc:
            self._detach_log_handler(retain=False)
            QMessageBox.critical(self, "启动失败", str(exc))

    def _on_pause_clicked(self) -> None:
        if self.runner.state == RunState.RUNNING:
            self.runner.pause()

    def _on_stop_clicked(self) -> None:
        if self.runner.state != RunState.IDLE:
            self.runner.stop()

    def _on_state(self, state: RunState, _key: object) -> None:
        self.status.setText(f"状态: {state.value}")
        if state == RunState.PAUSED:
            self.btn_start.setText("恢复")
        else:
            self.btn_start.setText("启动")
        busy = state != RunState.IDLE
        self.btn_pause.setEnabled(state == RunState.RUNNING)
        self.btn_stop.setEnabled(busy)

    def _on_run_finished(self) -> None:
        # Keep log lines; detach handler so idle noise is reduced
        self._detach_log_handler(retain=True)
        self.status.setText("就绪")
        self.btn_start.setText("启动")

    def _attach_log_handler(self) -> None:
        if self._log_handler is not None:
            detach_handler(self._log_handler)
        self._log_handler = QtLogHandler(lambda line: self.log_line.emit(line), buffer=self.logs.buffer)
        attach_nge_handler(self._log_handler)

    def _detach_log_handler(self, *, retain: bool) -> None:
        if self._log_handler is not None:
            detach_handler(self._log_handler)
            self._log_handler = None
        if not retain:
            self.logs.clear()

    def _show_error(self, message: str) -> None:
        QMessageBox.warning(self, "NGE-STUDIO", message)
