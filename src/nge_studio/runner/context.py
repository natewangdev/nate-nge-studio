"""RunContext cooperative pause/stop protocol."""

from __future__ import annotations

import threading
from datetime import UTC, datetime
from typing import Any


class ScriptStopped(Exception):
    """Raised by RunContext.checkpoint when stop was requested."""


class RunContext:
    """Thread-safe cooperative control signals for a script entry."""

    def __init__(self, *, script_params: dict[str, Any] | None = None) -> None:
        self._lock = threading.RLock()
        self._paused = False
        self._stop = False
        self._pause_event = threading.Event()
        self._pause_event.set()
        self.started_at = datetime.now(UTC)
        self.script_params: dict[str, Any] = dict(script_params or {})

    def set_paused(self, paused: bool) -> None:
        with self._lock:
            self._paused = bool(paused)
            if self._paused:
                self._pause_event.clear()
            else:
                self._pause_event.set()

    def request_stop(self) -> None:
        """Script- or Studio-initiated cooperative stop."""
        with self._lock:
            self._stop = True
            self._paused = False
            self._pause_event.set()

    def is_paused(self) -> bool:
        with self._lock:
            return self._paused and not self._stop

    def should_stop(self) -> bool:
        with self._lock:
            return self._stop

    def wait_if_paused(self, poll_sec: float = 0.05) -> None:
        while True:
            if self.should_stop():
                return
            if not self.is_paused():
                return
            self._pause_event.wait(timeout=max(poll_sec, 0.01))

    def checkpoint(self) -> None:
        self.wait_if_paused()
        if self.should_stop():
            raise ScriptStopped("脚本已请求结束")
