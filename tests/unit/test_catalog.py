"""Catalog validation tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from nge_studio.catalog.discover import discover_catalog
from nge_studio.catalog.validate import CatalogValidationError, validate_catalog_tree


def _write_script(root: Path, game: str, script: str, *, manifest: str, main: str) -> Path:
    d = root / game / script
    d.mkdir(parents=True)
    (d / "manifest.json").write_text(manifest, encoding="utf-8")
    (d / "main.py").write_text(main, encoding="utf-8")
    return d


VALID_MANIFEST = """
{"display_name": "T", "defaults": {"resource_dir": ".", "capture": "dxcam"}}
"""
VALID_MAIN = "def run(engine, ctx):\n    return\n"


def test_validate_ok(tmp_path: Path) -> None:
    _write_script(tmp_path, "g1", "s1", manifest=VALID_MANIFEST, main=VALID_MAIN)
    passed = validate_catalog_tree(tmp_path)
    assert passed == [("g1", "s1")]
    games = discover_catalog(tmp_path)
    assert len(games) == 1
    assert games[0].scripts[0].display_name == "T"
    assert games[0].display_name == "g1"


def test_missing_manifest_fails(tmp_path: Path) -> None:
    d = tmp_path / "g1" / "s1"
    d.mkdir(parents=True)
    (d / "main.py").write_text(VALID_MAIN, encoding="utf-8")
    with pytest.raises(CatalogValidationError) as ei:
        validate_catalog_tree(tmp_path)
    assert "manifest" in str(ei.value).lower() or "缺少" in str(ei.value)


def test_unknown_manifest_key_fails(tmp_path: Path) -> None:
    _write_script(
        tmp_path,
        "g1",
        "s1",
        manifest='{"display_name":"T","extra":1}',
        main=VALID_MAIN,
    )
    with pytest.raises(CatalogValidationError):
        validate_catalog_tree(tmp_path)


def test_game_manifest_absent_ok(tmp_path: Path) -> None:
    _write_script(tmp_path, "g1", "s1", manifest=VALID_MANIFEST, main=VALID_MAIN)
    validate_catalog_tree(tmp_path)
    game = discover_catalog(tmp_path)[0]
    assert game.manifest is None
    assert game.display_name == "g1"


def test_game_manifest_display_name(tmp_path: Path) -> None:
    _write_script(tmp_path, "g1", "s1", manifest=VALID_MANIFEST, main=VALID_MAIN)
    (tmp_path / "g1" / "manifest.json").write_text(
        '{"display_name": "我的游戏", "description": "d"}',
        encoding="utf-8",
    )
    validate_catalog_tree(tmp_path)
    game = discover_catalog(tmp_path)[0]
    assert game.display_name == "我的游戏"
    assert game.manifest is not None
    assert game.manifest.description == "d"


def test_game_manifest_empty_display_falls_back(tmp_path: Path) -> None:
    _write_script(tmp_path, "g1", "s1", manifest=VALID_MANIFEST, main=VALID_MAIN)
    (tmp_path / "g1" / "manifest.json").write_text('{"display_name": "  "}', encoding="utf-8")
    validate_catalog_tree(tmp_path)
    assert discover_catalog(tmp_path)[0].display_name == "g1"


def test_game_manifest_forbids_defaults(tmp_path: Path) -> None:
    _write_script(tmp_path, "g1", "s1", manifest=VALID_MANIFEST, main=VALID_MAIN)
    (tmp_path / "g1" / "manifest.json").write_text(
        '{"display_name": "G", "defaults": {}}',
        encoding="utf-8",
    )
    with pytest.raises(CatalogValidationError) as ei:
        validate_catalog_tree(tmp_path)
    assert "defaults" in str(ei.value) or "未知" in str(ei.value)


def test_game_manifest_invalid_json_fails(tmp_path: Path) -> None:
    _write_script(tmp_path, "g1", "s1", manifest=VALID_MANIFEST, main=VALID_MAIN)
    (tmp_path / "g1" / "manifest.json").write_text("{not-json", encoding="utf-8")
    with pytest.raises(CatalogValidationError):
        validate_catalog_tree(tmp_path)
