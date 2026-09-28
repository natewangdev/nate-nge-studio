"""Live log panel."""

from __future__ import annotations

from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QPlainTextEdit, QVBoxLayout, QWidget

from nge_studio.logging_bridge.qt_handler import LogBuffer


class LogPanel(QWidget):
    def __init__(self, parent: QWidget | None = None, *, maxlen: int = 5000) -> None:
        super().__init__(parent)
        self.buffer = LogBuffer(maxlen=maxlen)
        self._view = QPlainTextEdit()
        self._view.setReadOnly(True)
        self._view.setMaximumBlockCount(maxlen)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._view)

    def append_line(self, line: str) -> None:
        # Handler may already have buffered; UI view is source of truth for display.
        self._view.appendPlainText(line)
        self._view.moveCursor(QTextCursor.MoveOperation.End)

    def clear(self) -> None:
        self.buffer.clear()
        self._view.clear()
