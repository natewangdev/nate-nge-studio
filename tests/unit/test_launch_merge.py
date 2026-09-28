"""Launch parameter merge tests."""

from __future__ import annotations

from nge_studio.catalog.models import LaunchParameters, merge_launch_parameters


def test_overlay_wins() -> None:
    defaults = LaunchParameters(resource_dir=".", hwnd=None, capture="dxcam")
    overlay = LaunchParameters(resource_dir="res", hwnd=9, capture="mss")
    merged = merge_launch_parameters(defaults, overlay)
    assert merged.resource_dir == "res"
    assert merged.hwnd == 9
    assert merged.capture == "mss"


def test_partial_dict_overlay() -> None:
    defaults = LaunchParameters(resource_dir=".", humanize=True)
    merged = merge_launch_parameters(defaults, {"hwnd": 1})
    assert merged.hwnd == 1
    assert merged.humanize is True
    assert merged.resource_dir == "."
