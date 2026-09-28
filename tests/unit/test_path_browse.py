"""Unit tests for path browse helpers and hour conversion."""

from __future__ import annotations

from pathlib import Path

from nge_studio.ui.path_browse import (
    browse_start_directory,
    hours_to_seconds,
    seconds_to_hours_text,
    store_picked_path,
)


def test_browse_start_falls_back_to_home(tmp_path: Path) -> None:
    home = Path.home()
    assert browse_start_directory("") == str(home)
    assert browse_start_directory(str(tmp_path / "missing")) == str(home)


def test_browse_start_uses_existing_resource_dir(tmp_path: Path) -> None:
    assert browse_start_directory(str(tmp_path)) == str(tmp_path.resolve())


def test_store_picked_relative_under_resource(tmp_path: Path) -> None:
    nested = tmp_path / "models"
    nested.mkdir()
    file_path = nested / "yolo.onnx"
    file_path.write_text("x", encoding="utf-8")
    stored = store_picked_path(str(file_path), str(tmp_path))
    assert stored == "models/yolo.onnx"


def test_store_picked_absolute_outside_resource(tmp_path: Path) -> None:
    other = tmp_path / "other"
    other.mkdir()
    root = tmp_path / "res"
    root.mkdir()
    stored = store_picked_path(str(other), str(root))
    assert Path(stored).is_absolute()
    assert Path(stored) == other.resolve()


def test_hours_seconds_roundtrip() -> None:
    assert hours_to_seconds(0.5) == 1800.0
    assert seconds_to_hours_text(1800.0) == "0.5"
    assert seconds_to_hours_text(3600.0) == "1"
