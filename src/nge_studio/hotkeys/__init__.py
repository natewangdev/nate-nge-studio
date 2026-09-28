"""hotkeys package."""

from nge_studio.hotkeys.win32 import GlobalHotkeys, HotkeyRegistrationError, dispatch_hotkey_message

__all__ = ["GlobalHotkeys", "HotkeyRegistrationError", "dispatch_hotkey_message"]
