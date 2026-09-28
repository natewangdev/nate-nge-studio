"""Modern tech-oriented QSS (dark cyan / slate — avoid purple-on-white cliché)."""

APP_QSS = """
QWidget {
  background-color: #0b1220;
  color: #e6edf7;
  font-family: "Segoe UI", "Microsoft YaHei UI", sans-serif;
  font-size: 13px;
}
QMainWindow, QDialog {
  background-color: #0b1220;
}
QTreeWidget, QPlainTextEdit, QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QTextEdit {
  background-color: #121a2b;
  border: 1px solid #243049;
  border-radius: 4px;
  padding: 4px 6px;
  selection-background-color: #1f6feb;
}
QHeaderView::section {
  background-color: #152238;
  color: #e6edf7;
  border: none;
  border-bottom: 1px solid #243049;
  padding: 6px 8px;
  font-weight: 600;
}
QTreeWidget::item:selected {
  background-color: #1f6feb;
}
QPushButton {
  background-color: #152238;
  border: 1px solid #2f4568;
  border-radius: 4px;
  padding: 6px 14px;
  min-height: 28px;
}
QPushButton:hover {
  background-color: #1c2e4a;
  border-color: #3d6ea8;
}
QPushButton:pressed {
  background-color: #0f1a2c;
}
QPushButton#primaryButton {
  background-color: #0e7c66;
  border-color: #14b8a6;
  font-weight: 600;
}
QPushButton#dangerButton {
  background-color: #7f1d1d;
  border-color: #ef4444;
}
QPushButton:disabled {
  color: #6b7280;
  background-color: #101826;
  border-color: #1f2937;
}
QLabel#brandLabel {
  color: #5eead4;
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 1px;
}
QLabel#hintLabel {
  color: #94a3b8;
}
QGroupBox {
  border: 1px solid #243049;
  border-radius: 6px;
  margin-top: 10px;
  padding-top: 8px;
}
QGroupBox::title {
  subcontrol-origin: margin;
  left: 10px;
  padding: 0 4px;
  color: #7dd3fc;
}
QStatusBar {
  background: #070d18;
  color: #94a3b8;
}
"""
