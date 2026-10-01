"""Catalog domain models and launch-parameter merge."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path
from typing import Any

CAPTURE_CHOICES = frozenset({"dxcam", "mss"})
DURATION_END_ACTIONS = frozenset({"none", "shutdown"})
SCRIPT_PARAM_TYPES = frozenset({"string", "int", "number", "bool", "choice"})
SCRIPT_PARAM_ID_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


@dataclass
class LaunchParameters:
    resource_dir: str = "."
    hwnd: int | None = None
    window_title: str | None = None
    capture: str = "dxcam"
    humanize: bool = True
    control_mode: int = 2
    log_dir: str | None = None
    yolo_model: str = "models/yolo.onnx"
    yolo_names: str | None = "models/yolo.names"
    ocr_kwargs: dict[str, Any] | None = None
    run_duration_sec: float | None = None
    duration_end_action: str = "none"

    def validate_for_start(self) -> None:
        if self.resource_dir is None or str(self.resource_dir).strip() == "":
            raise ValueError("resource_dir 不能为空")
        if self.capture not in CAPTURE_CHOICES:
            raise ValueError(f"capture 必须是 dxcam 或 mss，收到: {self.capture!r}")
        if self.run_duration_sec is not None and self.run_duration_sec <= 0:
            raise ValueError("run_duration_sec 必须为空或大于 0")
        if self.ocr_kwargs is not None and not isinstance(self.ocr_kwargs, dict):
            raise ValueError("ocr_kwargs 必须是 JSON 对象或空")
        action = (self.duration_end_action or "none").strip().lower()
        if action not in DURATION_END_ACTIONS:
            raise ValueError(f"duration_end_action 必须是 none 或 shutdown，收到: {action!r}")
        self.duration_end_action = action

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> LaunchParameters:
        if not data:
            return cls()
        allowed = {f.name for f in fields(cls)}
        unknown = set(data) - allowed
        if unknown:
            raise ValueError(f"未知启动参数字段: {sorted(unknown)}")
        kwargs: dict[str, Any] = {}
        for name in allowed:
            if name in data:
                kwargs[name] = data[name]
        obj = cls(**kwargs)
        if obj.capture not in CAPTURE_CHOICES:
            raise ValueError(f"capture 必须是 dxcam 或 mss，收到: {obj.capture!r}")
        if obj.run_duration_sec is not None and obj.run_duration_sec <= 0:
            raise ValueError("run_duration_sec 必须为空或大于 0")
        action = (obj.duration_end_action or "none").strip().lower()
        if action not in DURATION_END_ACTIONS:
            raise ValueError(f"duration_end_action 必须是 none 或 shutdown，收到: {action!r}")
        obj.duration_end_action = action
        return obj


@dataclass
class ScriptParamField:
    id: str
    type: str
    label: str | None = None
    default: Any = None
    choices: list[str] | None = None

    @property
    def ui_label(self) -> str:
        return (self.label or "").strip() or self.id


@dataclass
class Manifest:
    display_name: str | None = None
    description: str | None = None
    defaults: LaunchParameters = field(default_factory=LaunchParameters)
    script_params: list[ScriptParamField] = field(default_factory=list)


@dataclass
class GameManifest:
    display_name: str | None = None
    description: str | None = None


@dataclass
class Script:
    game_id: str
    script_id: str
    path: Path
    manifest: Manifest

    @property
    def key(self) -> str:
        return f"{self.game_id}/{self.script_id}"

    @property
    def display_name(self) -> str:
        name = (self.manifest.display_name or "").strip()
        return name if name else self.script_id

    @property
    def entry_module(self) -> Path:
        return self.path / "main.py"


@dataclass
class Game:
    game_id: str
    path: Path
    scripts: list[Script] = field(default_factory=list)
    manifest: GameManifest | None = None

    @property
    def display_name(self) -> str:
        if self.manifest is None:
            return self.game_id
        name = (self.manifest.display_name or "").strip()
        return name if name else self.game_id


def merge_launch_parameters(
    defaults: LaunchParameters,
    overlay: LaunchParameters | dict[str, Any] | None,
) -> LaunchParameters:
    """Merge manifest defaults with last-used overlay (overlay wins when present)."""
    base = defaults.to_dict()
    if overlay is None:
        return LaunchParameters.from_dict(base)
    if isinstance(overlay, LaunchParameters):
        over = overlay.to_dict()
    else:
        over = dict(overlay)
    merged = dict(base)
    for key, value in over.items():
        if key in base:
            merged[key] = value
    return LaunchParameters.from_dict(merged)


def coerce_script_param_value(field_def: ScriptParamField, value: Any) -> Any:
    t = field_def.type
    if t == "string":
        return "" if value is None else str(value)
    if t == "bool":
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in {"1", "true", "yes", "on"}
        return bool(value)
    if t == "int":
        if value is None or value == "":
            return 0 if field_def.default is None else int(field_def.default)
        return int(value)
    if t == "number":
        if value is None or value == "":
            return 0.0 if field_def.default is None else float(field_def.default)
        return float(value)
    if t == "choice":
        choices = field_def.choices or []
        text = "" if value is None else str(value)
        if text in choices:
            return text
        if field_def.default is not None and str(field_def.default) in choices:
            return str(field_def.default)
        if choices:
            return choices[0]
        raise ValueError(f"script_params.{field_def.id} 无可用 choices")
    raise ValueError(f"不支持的 script_params 类型: {t}")


def default_script_params(fields_list: list[ScriptParamField]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for f in fields_list:
        out[f.id] = coerce_script_param_value(f, f.default)
    return out


def merge_script_params(
    fields_list: list[ScriptParamField],
    overlay: dict[str, Any] | None,
) -> dict[str, Any]:
    merged = default_script_params(fields_list)
    if not overlay:
        return merged
    by_id = {f.id: f for f in fields_list}
    for key, value in overlay.items():
        if key in by_id:
            merged[key] = coerce_script_param_value(by_id[key], value)
    return merged
