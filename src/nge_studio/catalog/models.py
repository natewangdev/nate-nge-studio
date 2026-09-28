"""Catalog domain models and launch-parameter merge."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
from pathlib import Path
from typing import Any

CAPTURE_CHOICES = frozenset({"dxcam", "mss"})


@dataclass
class LaunchParameters:
    resource_dir: str = "."
    hwnd: int | None = None
    capture: str = "dxcam"
    humanize: bool = True
    control_mode: int = 2
    log_dir: str | None = None
    yolo_model: str = "models/yolo.onnx"
    yolo_names: str | None = "models/yolo.names"
    ocr_kwargs: dict[str, Any] | None = None
    run_duration_sec: float | None = None

    def validate_for_start(self) -> None:
        if self.resource_dir is None or str(self.resource_dir).strip() == "":
            raise ValueError("resource_dir 不能为空")
        if self.capture not in CAPTURE_CHOICES:
            raise ValueError(f"capture 必须是 dxcam 或 mss，收到: {self.capture!r}")
        if self.run_duration_sec is not None and self.run_duration_sec <= 0:
            raise ValueError("run_duration_sec 必须为空或大于 0")
        if self.ocr_kwargs is not None and not isinstance(self.ocr_kwargs, dict):
            raise ValueError("ocr_kwargs 必须是 JSON 对象或空")

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
        return obj


@dataclass
class Manifest:
    display_name: str | None = None
    description: str | None = None
    defaults: LaunchParameters = field(default_factory=LaunchParameters)


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
