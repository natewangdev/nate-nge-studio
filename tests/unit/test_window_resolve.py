"""Unit tests for window title → hwnd resolution."""

from __future__ import annotations

import sys
import types
from types import SimpleNamespace

import pytest

from nge_studio.catalog.models import LaunchParameters
from nge_studio.runner.window_resolve import WindowResolveError, resolve_hwnd_for_launch


def _install_fake_nge2_window(monkeypatch: pytest.MonkeyPatch, find_by_title):
    """Stub ``nge2.window.Window`` so resolve can run without real NGE2."""
    window_mod = types.ModuleType("nge2.window")

    class Window:
        def __init__(self, _hwnd=None) -> None:
            pass

        def find_by_title(self, query: str):
            return find_by_title(self, query)

    window_mod.Window = Window
    nge2_mod = types.ModuleType("nge2")
    nge2_mod.window = window_mod  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "nge2", nge2_mod)
    monkeypatch.setitem(sys.modules, "nge2.window", window_mod)


def test_explicit_hwnd_wins(monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(_self, _query: str):
        raise AssertionError("find_by_title should not run when hwnd set")

    _install_fake_nge2_window(monkeypatch, boom)
    assert resolve_hwnd_for_launch(LaunchParameters(hwnd=42, window_title="Anything")) == 42


def test_title_first_match(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_fake_nge2_window(
        monkeypatch,
        lambda _self, query: [
            SimpleNamespace(hwnd=111, title=f"AAA {query}"),
            SimpleNamespace(hwnd=222, title=f"BBB {query}"),
        ],
    )
    assert resolve_hwnd_for_launch(LaunchParameters(window_title="Game")) == 111


def test_title_miss_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_fake_nge2_window(monkeypatch, lambda _self, _q: [])
    with pytest.raises(WindowResolveError, match="未找到"):
        resolve_hwnd_for_launch(LaunchParameters(window_title="Missing"))


def test_both_empty_unbound() -> None:
    assert resolve_hwnd_for_launch(LaunchParameters()) is None
