"""Global hotkeys via Win32 RegisterHotKey."""

from __future__ import annotations

import ctypes
from collections.abc import Callable
from typing import Any

user32 = ctypes.windll.user32

MOD_NOREPEAT = 0x4000
WM_HOTKEY = 0x0312

_VK_MAP = {
    "F1": 0x70,
    "F2": 0x71,
    "F3": 0x72,
    "F4": 0x73,
    "F5": 0x74,
    "F6": 0x75,
    "F7": 0x76,
    "F8": 0x77,
    "F9": 0x78,
    "F10": 0x79,
    "F11": 0x7A,
    "F12": 0x7B,
}

_ACTION_IDS = {"start": 1, "pause": 2, "stop": 3}


class HotkeyRegistrationError(Exception):
    pass


def _vk_for_key(key: str) -> int:
    k = key.strip().upper()
    if k in _VK_MAP:
        return _VK_MAP[k]
    if len(k) == 1 and "A" <= k <= "Z":
        return ord(k)
    raise HotkeyRegistrationError(f"不支持的快捷键: {key}")


class GlobalHotkeys:
    """Register three global hotkeys tied to an HWND message target."""

    def __init__(self, hwnd: int) -> None:
        self.hwnd = hwnd
        self._registered: list[int] = []

    def clear(self) -> None:
        for hotkey_id in list(self._registered):
            user32.UnregisterHotKey(self.hwnd, hotkey_id)
        self._registered.clear()

    def register_all(self, hotkeys: dict[str, dict[str, Any]]) -> None:
        self.clear()
        for action, hotkey_id in _ACTION_IDS.items():
            cfg = hotkeys.get(action) or {}
            key = str(cfg.get("key", ""))
            try:
                vk = _vk_for_key(key)
            except HotkeyRegistrationError:
                self.clear()
                raise
            mods = MOD_NOREPEAT
            for m in cfg.get("modifiers") or []:
                name = str(m).lower()
                if name in ("ctrl", "control"):
                    mods |= 0x0002
                elif name == "alt":
                    mods |= 0x0001
                elif name == "shift":
                    mods |= 0x0004
                elif name in ("win", "meta"):
                    mods |= 0x0008
            ok = user32.RegisterHotKey(self.hwnd, hotkey_id, mods, vk)
            if not ok:
                self.clear()
                raise HotkeyRegistrationError(f"注册快捷键失败: {action}={key}")
            self._registered.append(hotkey_id)

    @staticmethod
    def action_for_id(hotkey_id: int) -> str | None:
        for action, hid in _ACTION_IDS.items():
            if hid == hotkey_id:
                return action
        return None


def dispatch_hotkey_message(
    msg: int,
    wparam: int,
    handlers: dict[str, Callable[[], None]],
) -> bool:
    if msg != WM_HOTKEY:
        return False
    action = GlobalHotkeys.action_for_id(int(wparam))
    if action and action in handlers:
        handlers[action]()
        return True
    return False
