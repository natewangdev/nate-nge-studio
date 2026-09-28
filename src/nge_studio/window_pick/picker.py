"""Win32 window point-and-pick."""

from __future__ import annotations

import ctypes
from ctypes import wintypes
from dataclasses import dataclass

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32


@dataclass(frozen=True)
class WindowPickResult:
    hwnd: int
    title: str
    pid: int


class WindowPickError(Exception):
    pass


def _window_title(hwnd: int) -> str:
    length = user32.GetWindowTextLengthW(hwnd)
    if length <= 0:
        return ""
    buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value


def _pid_for_hwnd(hwnd: int) -> int:
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return int(pid.value)


def top_level_from_point(x: int, y: int) -> int:
    point = wintypes.POINT(x, y)
    hwnd = user32.WindowFromPoint(point)
    if not hwnd:
        raise WindowPickError("未命中窗口")
    # Ascend to root owner
    GA_ROOT = 2
    root = user32.GetAncestor(hwnd, GA_ROOT)
    return int(root or hwnd)


def pick_at_cursor(*, studio_pid: int | None = None) -> WindowPickResult:
    """Pick the top-level window under the cursor; reject Studio's own process."""
    class POINT(ctypes.Structure):
        _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]

    pt = POINT()
    if not user32.GetCursorPos(ctypes.byref(pt)):
        raise WindowPickError("无法读取光标位置")
    hwnd = top_level_from_point(int(pt.x), int(pt.y))
    pid = _pid_for_hwnd(hwnd)
    self_pid = studio_pid if studio_pid is not None else int(kernel32.GetCurrentProcessId())
    if pid == self_pid:
        raise WindowPickError("不能选择 NGE-STUDIO 自身窗口，请改选其他窗口")
    title = _window_title(hwnd) or f"HWND {hwnd}"
    return WindowPickResult(hwnd=hwnd, title=title, pid=pid)


def current_process_id() -> int:
    return int(kernel32.GetCurrentProcessId())
