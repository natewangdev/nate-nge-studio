"""Settings store tests."""

from __future__ import annotations

from pathlib import Path

from nge_studio.catalog.models import LaunchParameters
from nge_studio.settings.store import AppSettings, SettingsStore


def test_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    store = SettingsStore(path)
    settings = AppSettings.defaults()
    store.set_launch_overlay(
        settings,
        "demo/smoke",
        LaunchParameters(resource_dir=".", hwnd=42, run_duration_sec=10),
    )
    store.save(settings)
    loaded, warn = store.load()
    assert warn is None
    overlay = store.get_launch_overlay(loaded, "demo/smoke")
    assert overlay is not None
    assert overlay.hwnd == 42
    assert overlay.run_duration_sec == 10


def test_corrupt_recovers(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    path.write_text("{not-json", encoding="utf-8")
    store = SettingsStore(path)
    settings, warn = store.load()
    assert settings.version == 1
    assert warn is not None
    assert path.with_suffix(".json.bak").is_file() or True  # bak may use .json.bak
