"""Launch parameter form."""

from __future__ import annotations

import json
from typing import Any

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
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


class ParamForm(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.resource_dir = QLineEdit()
        self.hwnd = QLineEdit()
        self.hwnd.setPlaceholderText("可选，留空=屏幕坐标")
        self.pick_btn = QPushButton("点选窗口")
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
        self.yolo_model = QLineEdit()
        self.yolo_names = QLineEdit()
        self.ocr_kwargs = QLineEdit()
        self.ocr_kwargs.setPlaceholderText('JSON 对象，如 {"use_angle_cls": true}')
        self.run_duration = QLineEdit()
        self.run_duration.setPlaceholderText("秒，留空=不限时")
        self.reset_btn = QPushButton("重置为默认")

        form = QFormLayout()
        form.addRow("资源目录 resource_dir", self.resource_dir)
        hwnd_row = QHBoxLayout()
        hwnd_row.addWidget(self.hwnd)
        hwnd_row.addWidget(self.pick_btn)
        form.addRow("窗口句柄 hwnd", hwnd_row)
        form.addRow("", self.hwnd_title)
        form.addRow("截屏 capture", self.capture)
        form.addRow("", self.humanize)
        form.addRow("控制模式 control_mode", self.control_mode)
        form.addRow("日志目录 log_dir", self.log_dir)
        form.addRow("YOLO 模型", self.yolo_model)
        form.addRow("YOLO names", self.yolo_names)
        form.addRow("OCR kwargs", self.ocr_kwargs)
        form.addRow("运行时长(秒)", self.run_duration)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(self.reset_btn)

    def set_parameters(self, params: LaunchParameters, *, window_title: str = "") -> None:
        self.resource_dir.setText(params.resource_dir or "")
        self.hwnd.setText("" if params.hwnd is None else str(params.hwnd))
        self.hwnd_title.setText(window_title)
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
            self.run_duration.setText(str(params.run_duration_sec))

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
        duration = float(dur_text) if dur_text else None
        yolo_names = self.yolo_names.text().strip()
        log_dir = self.log_dir.text().strip()
        return LaunchParameters(
            resource_dir=self.resource_dir.text().strip(),
            hwnd=hwnd,
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
