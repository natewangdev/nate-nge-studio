"""Injectable OS shutdown for duration_end_action=shutdown."""

from __future__ import annotations

import logging
import subprocess
import sys
from collections.abc import Callable

log = logging.getLogger("nge.studio.runner")

ShutdownExecutor = Callable[[], None]


def windows_forced_shutdown() -> None:
    """Force immediate Windows shutdown. No-op on non-Windows."""
    if sys.platform != "win32":
        log.warning("duration_end_action=shutdown 仅在 Windows 上执行，当前平台: %s", sys.platform)
        return
    # /s shut down, /t 0 immediate, /f force apps closed
    subprocess.run(
        ["shutdown", "/s", "/t", "0", "/f"],
        check=False,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )


def noop_shutdown() -> None:
    """Test-friendly no-op executor."""
    return
