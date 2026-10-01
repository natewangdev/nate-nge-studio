"""Settings store tests."""

from __future__ import annotations

from pathlib import Path

from nge_studio.catalog.models import LaunchParameters
from nge_studio.settings.store import AppSettings, SettingsStore, normalize_main_splitter_sizes


def test_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    store = SettingsStore(path)
    settings = AppSettings.defaults()
    store.set_launch_overlay(
        settings,
        "demo/smoke",
        LaunchParameters(resource_dir=".", hwnd=42, run_duration_sec=10),
        script_params={"loops": 3},
    )
    store.save(settings)
    loaded, warn = store.load()
    assert warn is None
    overlay = store.get_launch_overlay(loaded, "demo/smoke")
    assert overlay is not None
    assert overlay.hwnd == 42
    assert overlay.run_duration_sec == 10
    assert store.get_script_params_overlay(loaded, "demo/smoke") == {"loops": 3}


def test_set_launch_preserves_script_params(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    store = SettingsStore(path)
    settings = AppSettings.defaults()
    store.set_launch_overlay(
        settings,
        "demo/smoke",
        LaunchParameters(resource_dir="."),
        script_params={"a": 1},
    )
    store.set_launch_overlay(settings, "demo/smoke", LaunchParameters(resource_dir=".", hwnd=1))
    assert store.get_script_params_overlay(settings, "demo/smoke") == {"a": 1}


def test_corrupt_recovers(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    path.write_text("{not-json", encoding="utf-8")
    store = SettingsStore(path)
    settings, warn = store.load()
    assert settings.version == 1
    assert warn is not None


def test_splitter_sizes_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    store = SettingsStore(path)
    settings = AppSettings.defaults()
    settings.set_main_splitter_sizes([200, 300, 300])
    store.save(settings)
    loaded, warn = store.load()
    assert warn is None
    assert loaded.main_splitter_sizes() == [200, 300, 300]


def test_invalid_splitter_sizes_ignored_on_load(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    path.write_text(
        """{
          "version": 1,
          "hotkeys": {
            "start": {"key": "F9", "modifiers": []},
            "pause": {"key": "F10", "modifiers": []},
            "stop": {"key": "F11", "modifiers": []}
          },
          "launch_configs": {},
          "ui": {"main_splitter_sizes": [10, -1, 10]}
        }""",
        encoding="utf-8",
    )
    loaded, warn = SettingsStore(path).load()
    assert warn is None
    assert loaded.main_splitter_sizes() is None


def test_normalize_main_splitter_sizes() -> None:
    assert normalize_main_splitter_sizes([2, 3, 3]) == [2, 3, 3]
    assert normalize_main_splitter_sizes([1, 2]) is None
    assert normalize_main_splitter_sizes(None) is None
    assert normalize_main_splitter_sizes(["a", 2, 3]) is None
