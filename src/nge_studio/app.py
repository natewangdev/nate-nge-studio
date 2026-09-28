"""Application entry."""

from __future__ import annotations

import logging
import sys


def main(argv: list[str] | None = None) -> int:
    from PySide6.QtWidgets import QApplication

    from nge_studio.ui.main_window import MainWindow

    logging.basicConfig(level=logging.INFO)
    app = QApplication(argv if argv is not None else sys.argv)
    app.setApplicationName("NGE-STUDIO")
    app.setOrganizationName("nate")
    win = MainWindow()
    win.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
