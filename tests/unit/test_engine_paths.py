"""Tests for launch path resolution (resource_dir / log_dir)."""

from __future__ import annotations

from pathlib import Path

from nge_studio.runner.engine_factory import resolve_log_dir_for_launch, resolve_resource_dir


def test_relative_log_dir_joins_resource_dir(tmp_path: Path) -> None:
    resource = tmp_path / "d4"
    resource.mkdir()
    script_dir = tmp_path / "smoke"
    script_dir.mkdir()
    resolved = resolve_log_dir_for_launch("logs", resource.resolve())
    assert resolved == (resource / "logs").resolve()
    assert not str(resolved).startswith(str(script_dir.resolve()))


def test_absolute_log_dir_unchanged(tmp_path: Path) -> None:
    resource = (tmp_path / "d4").resolve()
    resource.mkdir()
    absolute = (tmp_path / "elsewhere" / "logs").resolve()
    assert resolve_log_dir_for_launch(str(absolute), resource) == absolute


def test_empty_log_dir_is_none(tmp_path: Path) -> None:
    resource = (tmp_path / "d4").resolve()
    resource.mkdir()
    assert resolve_log_dir_for_launch(None, resource) is None
    assert resolve_log_dir_for_launch("  ", resource) is None


def test_relative_resource_dir_joins_script_dir(tmp_path: Path) -> None:
    script_dir = tmp_path / "smoke"
    script_dir.mkdir()
    assert resolve_resource_dir(".", script_dir) == script_dir.resolve()
    nested = script_dir / "res"
    nested.mkdir()
    assert resolve_resource_dir("res", script_dir) == nested.resolve()


def test_absolute_resource_dir(tmp_path: Path) -> None:
    script_dir = tmp_path / "smoke"
    script_dir.mkdir()
    absolute = (tmp_path / "d4").resolve()
    absolute.mkdir()
    assert resolve_resource_dir(str(absolute), script_dir) == absolute
