"""Discover packaged game_scripts tree."""

from __future__ import annotations

import sys
from pathlib import Path

from nge_studio.catalog.models import Game, Script
from nge_studio.catalog.validate import validate_script_dir


def resolve_catalog_root(explicit: Path | None = None) -> Path:
    if explicit is not None:
        return explicit.resolve()
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            bundled = Path(meipass) / "game_scripts"
            if bundled.is_dir():
                return bundled.resolve()
        exe_dir = Path(sys.executable).resolve().parent
        beside = exe_dir / "game_scripts"
        if beside.is_dir():
            return beside.resolve()
    # Dev: repo root /game_scripts (src/nge_studio/catalog/discover.py → parents[3])
    here = Path(__file__).resolve()
    candidates = [
        here.parents[3] / "game_scripts",  # .../repo/game_scripts
        Path.cwd() / "game_scripts",
    ]
    for c in candidates:
        if c.is_dir():
            return c.resolve()
    return candidates[0].resolve()


def discover_catalog(root: Path | None = None, *, validate: bool = True) -> list[Game]:
    catalog_root = resolve_catalog_root(root)
    if not catalog_root.is_dir():
        return []
    games: list[Game] = []
    for game_dir in sorted(p for p in catalog_root.iterdir() if p.is_dir() and not p.name.startswith(".")):
        scripts: list[Script] = []
        for script_dir in sorted(
            p for p in game_dir.iterdir() if p.is_dir() and not p.name.startswith(".")
        ):
            if validate:
                manifest = validate_script_dir(script_dir)
            else:
                from nge_studio.catalog.validate import load_manifest_file

                manifest = load_manifest_file(script_dir / "manifest.json")
            scripts.append(
                Script(
                    game_id=game_dir.name,
                    script_id=script_dir.name,
                    path=script_dir.resolve(),
                    manifest=manifest,
                )
            )
        if scripts:
            games.append(Game(game_id=game_dir.name, path=game_dir.resolve(), scripts=scripts))
    return games
