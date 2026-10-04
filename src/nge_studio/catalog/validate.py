"""Manifest and catalog hard-fail validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nge_studio.catalog.models import (
    CAPTURE_CHOICES,
    SCRIPT_PARAM_ID_RE,
    SCRIPT_PARAM_TYPES,
    GameManifest,
    LaunchParameters,
    Manifest,
    ScriptParamField,
)


class CatalogValidationError(Exception):
    def __init__(self, path: Path | str, reason: str) -> None:
        self.path = Path(path)
        self.reason = reason
        super().__init__(f"{self.path}: {reason}")


_MANIFEST_TOP = frozenset({"display_name", "description", "defaults", "script_params", "sort_order"})
_GAME_MANIFEST_TOP = frozenset({"display_name", "description", "sort_order"})
_DEFAULT_KEYS = frozenset(f.name for f in LaunchParameters.__dataclass_fields__.values())  # type: ignore[attr-defined]
_SCRIPT_PARAM_KEYS = frozenset({"id", "type", "label", "default", "choices"})


def parse_sort_order(data: dict[str, Any], *, source: Path) -> int | None:
    if "sort_order" not in data:
        return None
    value = data["sort_order"]
    if isinstance(value, bool) or not isinstance(value, int):
        raise CatalogValidationError(source, "sort_order 必须是整数")
    return value


def parse_script_params(raw: Any, *, source: Path) -> list[ScriptParamField]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise CatalogValidationError(source, "script_params 必须是数组")
    seen: set[str] = set()
    fields_out: list[ScriptParamField] = []
    for i, item in enumerate(raw):
        prefix = f"script_params[{i}]"
        if not isinstance(item, dict):
            raise CatalogValidationError(source, f"{prefix} 必须是对象")
        unk = set(item) - _SCRIPT_PARAM_KEYS
        if unk:
            raise CatalogValidationError(source, f"{prefix} 含未知字段: {sorted(unk)}")
        pid = item.get("id")
        if not isinstance(pid, str) or not SCRIPT_PARAM_ID_RE.match(pid):
            raise CatalogValidationError(
                source,
                f"{prefix}.id 必须是合法标识符（字母/下划线开头）",
            )
        if pid in seen:
            raise CatalogValidationError(source, f"script_params id 重复: {pid}")
        seen.add(pid)
        ptype = item.get("type")
        if ptype not in SCRIPT_PARAM_TYPES:
            raise CatalogValidationError(
                source,
                f"{prefix}.type 非法: {ptype!r}（允许 {sorted(SCRIPT_PARAM_TYPES)}）",
            )
        label = item.get("label")
        if label is not None and not isinstance(label, str):
            raise CatalogValidationError(source, f"{prefix}.label 必须是字符串")
        choices = item.get("choices")
        if ptype == "choice":
            if not isinstance(choices, list) or not choices:
                raise CatalogValidationError(source, f"{prefix}.choices 必须是非空字符串数组")
            if not all(isinstance(c, str) for c in choices):
                raise CatalogValidationError(source, f"{prefix}.choices 元素必须是字符串")
        elif choices is not None:
            raise CatalogValidationError(source, f"{prefix}.choices 仅允许 type=choice")
        default = item.get("default")
        if ptype == "choice" and default is not None and default not in choices:
            raise CatalogValidationError(
                source,
                f"{prefix}.default 必须落在 choices 内",
            )
        if ptype == "bool" and default is not None and not isinstance(default, bool):
            raise CatalogValidationError(source, f"{prefix}.default 必须是布尔值")
        if ptype == "int" and default is not None and not isinstance(default, int):
            raise CatalogValidationError(source, f"{prefix}.default 必须是整数")
        if ptype == "number" and default is not None and not isinstance(default, (int, float)):
            raise CatalogValidationError(source, f"{prefix}.default 必须是数字")
        if ptype == "string" and default is not None and not isinstance(default, str):
            raise CatalogValidationError(source, f"{prefix}.default 必须是字符串")
        fields_out.append(
            ScriptParamField(
                id=pid,
                type=ptype,
                label=label,
                default=default,
                choices=list(choices) if isinstance(choices, list) else None,
            )
        )
    return fields_out


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
    script_params = parse_script_params(data.get("script_params"), source=source)
    return Manifest(
        display_name=display,
        description=desc,
        defaults=defaults,
        script_params=script_params,
        sort_order=parse_sort_order(data, source=source),
    )


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


def parse_game_manifest(data: dict[str, Any], *, source: Path) -> GameManifest:
    unknown = set(data) - _GAME_MANIFEST_TOP
    if unknown:
        raise CatalogValidationError(source, f"游戏 manifest 含未知字段: {sorted(unknown)}")
    display = data.get("display_name")
    desc = data.get("description")
    if display is not None and not isinstance(display, str):
        raise CatalogValidationError(source, "display_name 必须是字符串")
    if desc is not None and not isinstance(desc, str):
        raise CatalogValidationError(source, "description 必须是字符串")
    return GameManifest(
        display_name=display,
        description=desc,
        sort_order=parse_sort_order(data, source=source),
    )


def load_game_manifest_file(path: Path) -> GameManifest | None:
    """Load optional game-level manifest. Missing file → None; present+invalid → raise."""
    if not path.is_file():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CatalogValidationError(path, f"JSON 无效: {exc}") from exc
    if not isinstance(raw, dict):
        raise CatalogValidationError(path, "游戏 manifest 根节点必须是对象")
    return parse_game_manifest(raw, source=path)


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
        load_game_manifest_file(game_dir / "manifest.json")
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
