"""Manifest and catalog hard-fail validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nge_studio.catalog.models import CAPTURE_CHOICES, LaunchParameters, Manifest


class CatalogValidationError(Exception):
    def __init__(self, path: Path | str, reason: str) -> None:
        self.path = Path(path)
        self.reason = reason
        super().__init__(f"{self.path}: {reason}")


_MANIFEST_TOP = frozenset({"display_name", "description", "defaults"})
_DEFAULT_KEYS = frozenset(f.name for f in LaunchParameters.__dataclass_fields__.values())  # type: ignore[attr-defined]


def parse_manifest(data: dict[str, Any], *, source: Path) -> Manifest:
    unknown = set(data) - _MANIFEST_TOP
    if unknown:
        raise CatalogValidationError(source, f"manifest 含未知字段: {sorted(unknown)}")
    defaults_raw = data.get("defaults")
    if defaults_raw is None:
        defaults = LaunchParameters()
    elif not isinstance(defaults_raw, dict):
        raise CatalogValidationError(source, "defaults 必须是对象")
    else:
        unk = set(defaults_raw) - _DEFAULT_KEYS
        if unk:
            raise CatalogValidationError(source, f"defaults 含未知字段: {sorted(unk)}")
        try:
            defaults = LaunchParameters.from_dict(defaults_raw)
        except ValueError as exc:
            raise CatalogValidationError(source, str(exc)) from exc
        if defaults.capture not in CAPTURE_CHOICES:
            raise CatalogValidationError(source, f"非法 capture: {defaults.capture!r}")
    display = data.get("display_name")
    desc = data.get("description")
    if display is not None and not isinstance(display, str):
        raise CatalogValidationError(source, "display_name 必须是字符串")
    if desc is not None and not isinstance(desc, str):
        raise CatalogValidationError(source, "description 必须是字符串")
    return Manifest(display_name=display, description=desc, defaults=defaults)


def load_manifest_file(path: Path) -> Manifest:
    if not path.is_file():
        raise CatalogValidationError(path, "缺少 manifest.json")
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CatalogValidationError(path, f"JSON 无效: {exc}") from exc
    if not isinstance(raw, dict):
        raise CatalogValidationError(path, "manifest 根节点必须是对象")
    return parse_manifest(raw, source=path)


def validate_script_dir(script_dir: Path) -> Manifest:
    manifest = load_manifest_file(script_dir / "manifest.json")
    main_py = script_dir / "main.py"
    if not main_py.is_file():
        raise CatalogValidationError(main_py, "缺少 main.py")
    # Lightweight syntax/import check for `run` without executing game logic:
    source = main_py.read_text(encoding="utf-8")
    if "def run(" not in source:
        raise CatalogValidationError(main_py, "main.py 必须定义 def run(")
    return manifest


def validate_catalog_tree(root: Path) -> list[tuple[str, str]]:
    """Validate all script dirs under root. Raises CatalogValidationError on first failure.

    Returns list of (game_id, script_id) that passed.
    """
    if not root.is_dir():
        raise CatalogValidationError(root, "目录根不存在")
    passed: list[tuple[str, str]] = []
    for game_dir in sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")):
        script_dirs = [
            p
            for p in game_dir.iterdir()
            if p.is_dir() and not p.name.startswith(".") and p.name != "__pycache__"
        ]
        if not script_dirs:
            continue
        for script_dir in sorted(script_dirs):
            validate_script_dir(script_dir)
            passed.append((game_dir.name, script_dir.name))
    return passed
