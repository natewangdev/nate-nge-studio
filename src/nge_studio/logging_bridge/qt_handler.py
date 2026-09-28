"""Qt logging bridge for live log panel."""

from __future__ import annotations

import logging
from collections import deque
from collections.abc import Callable


class LogBuffer:
    def __init__(self, maxlen: int = 5000) -> None:
        self._lines: deque[str] = deque(maxlen=maxlen)
        self.maxlen = maxlen

    def append(self, line: str) -> None:
        self._lines.append(line)

    def clear(self) -> None:
        self._lines.clear()

    def lines(self) -> list[str]:
        return list(self._lines)

    def __len__(self) -> int:
        return len(self._lines)


class QtLogHandler(logging.Handler):
    """logging.Handler that forwards formatted records to a callback."""

    def __init__(
        self,
        emit_line: Callable[[str], None],
        *,
        buffer: LogBuffer | None = None,
        level: int = logging.INFO,
    ) -> None:
        super().__init__(level=level)
        self._emit_line = emit_line
        self.buffer = buffer or LogBuffer()
        self.setFormatter(logging.Formatter("%(asctime)s %(levelname)-7s %(message)s", "%H:%M:%S"))

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self.buffer.append(msg)
            self._emit_line(msg)
        except Exception:
            self.handleError(record)


def attach_nge_handler(handler: logging.Handler) -> None:
    root = logging.getLogger("nge")
    root.addHandler(handler)
    if root.level == logging.NOTSET:
        root.setLevel(logging.INFO)


def detach_handler(handler: logging.Handler) -> None:
    root = logging.getLogger("nge")
    root.removeHandler(handler)
