"""Window pick self-rejection tests (mocked)."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from nge_studio.window_pick.picker import WindowPickError, pick_at_cursor


def test_rejects_self_pid() -> None:
    with (
        patch("nge_studio.window_pick.picker.user32.GetCursorPos", return_value=1),
        patch("nge_studio.window_pick.picker.top_level_from_point", return_value=123),
        patch("nge_studio.window_pick.picker._pid_for_hwnd", return_value=42),
        patch("nge_studio.window_pick.picker.kernel32.GetCurrentProcessId", return_value=42),
    ):
        with pytest.raises(WindowPickError) as ei:
            pick_at_cursor()
        assert "自身" in str(ei.value)
