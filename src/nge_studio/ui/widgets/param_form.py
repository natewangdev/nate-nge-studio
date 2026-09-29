"""Launch parameter form."""

from __future__ import annotations

import json
from typing import Any

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from nge_studio.catalog.models import LaunchParameters
from nge_studio.ui.path_browse import (
    browse_start_directory,
    hours_to_seconds,
    seconds_to_hours_text,
    store_picked_path,
)


def _row_button(text: str) -> QPushButton:
    btn = QPushButton(text)
    btn.setObjectName("rowButton")
    return btn


def _input_with_button(edit: QLineEdit, button: QPushButton) -> QWidget:
    row = QWidget()
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(6)
    layout.addWidget(edit, stretch=1)
    layout.addWidget(button)
    return row


class ParamForm(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.resource_dir = QLineEdit()
        self.resource_browse = _row_button("选择")
        self.hwnd = QLineEdit()
        self.hwnd.setPlaceholderText("可选，留空=屏幕坐标")
        self.pick_btn = _row_button("点选窗口")
        self.window_title = QLineEdit()
        self.window_title.setPlaceholderText("可选；无 hwnd 时按标题包含匹配第一个窗口")
        self.hwnd_title = QLabel("")
        self.hwnd_title.setObjectName("hintLabel")
        self.capture = QComboBox()
        self.capture.addItems(["dxcam", "mss"])
        self.humanize = QCheckBox("拟人化移动")
        self.humanize.setChecked(True)
        self.control_mode = QSpinBox()
        self.control_mode.setRange(0, 10)
        self.control_mode.setValue(2)
        self.log_dir = QLineEdit()
        self.log_browse = _row_button("选择")
        self.yolo_model = QLineEdit()
        self.yolo_model_browse = _row_button("选择")
        self.yolo_names = QLineEdit()
        self.yolo_names_browse = _row_button("选择")
        self.ocr_kwargs = QLineEdit()
        self.ocr_kwargs.setPlaceholderText('JSON 对象，如 {"use_angle_cls": true}')
        self.run_duration = QLineEdit()
        self.run_duration.setPlaceholderText("小时，如 0.5；留空=不限时")
        self.reset_btn = QPushButton("重置为默认")

        form = QFormLayout()
        form.addRow(
            "资源目录 resource_dir",
            _input_with_button(self.resource_dir, self.resource_browse),
        )
        form.addRow("窗口标题 window_title", self.window_title)
        form.addRow("窗口句柄 hwnd", _input_with_button(self.hwnd, self.pick_btn))
        form.addRow("", self.hwnd_title)
        form.addRow("截屏 capture", self.capture)
        form.addRow("", self.humanize)
        form.addRow("控制模式 control_mode", self.control_mode)
        form.addRow("日志目录 log_dir", _input_with_button(self.log_dir, self.log_browse))
        form.addRow("YOLO 模型", _input_with_button(self.yolo_model, self.yolo_model_browse))
        form.addRow("YOLO names", _input_with_button(self.yolo_names, self.yolo_names_browse))
        form.addRow("OCR kwargs", self.ocr_kwargs)
        form.addRow("运行时长(小时)", self.run_duration)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(self.reset_btn)

        self.resource_browse.clicked.connect(self._browse_resource_dir)
        self.log_browse.clicked.connect(self._browse_log_dir)
        self.yolo_model_browse.clicked.connect(self._browse_yolo_model)
        self.yolo_names_browse.clicked.connect(self._browse_yolo_names)

    def _start_dir(self) -> str:
        return browse_start_directory(self.resource_dir.text())

    def _apply_picked(self, edit: QLineEdit, picked: str) -> None:
        edit.setText(store_picked_path(picked, self.resource_dir.text()))

    def _browse_resource_dir(self) -> None:
        path = QFileDialog.getExistingDirectory(
            self,
            "选择资源目录",
            self._start_dir(),
        )
        if path:
            # Choosing resource_dir itself: store absolute (or as typed resolve)
            self.resource_dir.setText(path)

    def _browse_log_dir(self) -> None:
        path = QFileDialog.getExistingDirectory(
            self,
            "选择日志目录",
            self._start_dir(),
        )
        if path:
            self._apply_picked(self.log_dir, path)

    def _browse_yolo_model(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "选择 YOLO 模型",
            self._start_dir(),
            "ONNX 模型 (*.onnx);;所有文件 (*.*)",
        )
        if path:
            self._apply_picked(self.yolo_model, path)

    def _browse_yolo_names(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "选择 YOLO names",
            self._start_dir(),
            "Names (*.names *.txt);;所有文件 (*.*)",
        )
        if path:
            self._apply_picked(self.yolo_names, path)

    def set_parameters(self, params: LaunchParameters, *, picked_title: str = "") -> None:
        self.resource_dir.setText(params.resource_dir or "")
        self.hwnd.setText("" if params.hwnd is None else str(params.hwnd))
        self.window_title.setText(params.window_title or "")
        self.hwnd_title.setText(picked_title or params.window_title or "")
        idx = self.capture.findText(params.capture)
        self.capture.setCurrentIndex(max(0, idx))
        self.humanize.setChecked(bool(params.humanize))
        self.control_mode.setValue(int(params.control_mode))
        self.log_dir.setText(params.log_dir or "")
        self.yolo_model.setText(params.yolo_model or "")
        self.yolo_names.setText("" if params.yolo_names is None else str(params.yolo_names))
        if params.ocr_kwargs is None:
            self.ocr_kwargs.setText("")
        else:
            self.ocr_kwargs.setText(json.dumps(params.ocr_kwargs, ensure_ascii=False))
        if params.run_duration_sec is None:
            self.run_duration.setText("")
        else:
            self.run_duration.setText(seconds_to_hours_text(float(params.run_duration_sec)))

    def get_parameters(self) -> LaunchParameters:
        hwnd_text = self.hwnd.text().strip()
        hwnd = int(hwnd_text) if hwnd_text else None
        ocr_text = self.ocr_kwargs.text().strip()
        ocr: dict[str, Any] | None
        if not ocr_text:
            ocr = None
        else:
            parsed = json.loads(ocr_text)
            if not isinstance(parsed, dict):
                raise ValueError("ocr_kwargs 必须是 JSON 对象")
            ocr = parsed
        dur_text = self.run_duration.text().strip()
        if dur_text:
            hours = float(dur_text)
            duration = hours_to_seconds(hours)
        else:
            duration = None
        yolo_names = self.yolo_names.text().strip()
        log_dir = self.log_dir.text().strip()
        title = self.window_title.text().strip()
        return LaunchParameters(
            resource_dir=self.resource_dir.text().strip(),
            hwnd=hwnd,
            window_title=title or None,
            capture=self.capture.currentText(),
            humanize=self.humanize.isChecked(),
            control_mode=int(self.control_mode.value()),
            log_dir=log_dir or None,
            yolo_model=self.yolo_model.text().strip() or "models/yolo.onnx",
            yolo_names=yolo_names or None,
            ocr_kwargs=ocr,
            run_duration_sec=duration,
        )

    def set_hwnd(self, hwnd: int, title: str) -> None:
        self.hwnd.setText(str(hwnd))
        self.hwnd_title.setText(title)
        self.window_title.setText(title)
