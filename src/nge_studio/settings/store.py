"""Persisted settings under LOCALAPPDATA/NGE-STUDIO."""

from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from nge_studio.catalog.models import LaunchParameters

DEFAULT_HOTKEYS: dict[str, dict[str, Any]] = {
    "start": {"key": "F9", "modifiers": []},
    "pause": {"key": "F10", "modifiers": []},
    "stop": {"key": "F11", "modifiers": []},
}

# Default main splitter stretch weights (left : center : right)
DEFAULT_MAIN_SPLITTER_STRETCH = (2, 3, 3)


def normalize_main_splitter_sizes(raw: Any) -> list[int] | None:
    """Return three positive ints, or None if invalid/missing."""
    if raw is None:
        return None
    if not isinstance(raw, (list, tuple)) or len(raw) != 3:
        return None
    sizes: list[int] = []
    for item in raw:
        try:
            value = int(item)
        except (TypeError, ValueError):
            return None
        if value <= 0:
            return None
        sizes.append(value)
    return sizes


def default_settings_path() -> Path:
    base = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
    return Path(base) / "NGE-STUDIO" / "settings.json"


@dataclass
class AppSettings:
    version: int
    hotkeys: dict[str, dict[str, Any]]
    launch_configs: dict[str, dict[str, Any]]
    ui: dict[str, Any]

    @classmethod
    def defaults(cls) -> AppSettings:
        return cls(version=1, hotkeys=dict(DEFAULT_HOTKEYS), launch_configs={}, ui={})

    def main_splitter_sizes(self) -> list[int] | None:
        return normalize_main_splitter_sizes((self.ui or {}).get("main_splitter_sizes"))

    def set_main_splitter_sizes(self, sizes: list[int]) -> None:
        normalized = normalize_main_splitter_sizes(sizes)
        if normalized is None:
            return
        if self.ui is None:
            self.ui = {}
        self.ui["main_splitter_sizes"] = normalized


class SettingsStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or default_settings_path()

    def load(self) -> tuple[AppSettings, str | None]:
        """Return settings and optional warning message."""
        if not self.path.is_file():
            return AppSettings.defaults(), None
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(raw, dict):
                raise ValueError("根节点不是对象")
            version = int(raw.get("version", 1))
            hotkeys = raw.get("hotkeys") or dict(DEFAULT_HOTKEYS)
            for action, default in DEFAULT_HOTKEYS.items():
                hotkeys.setdefault(action, default)
            launch_configs = raw.get("launch_configs") or {}
            if not isinstance(launch_configs, dict):
                raise ValueError("launch_configs 无效")
            ui_raw = raw.get("ui") or {}
            if not isinstance(ui_raw, dict):
                ui_raw = {}
            ui: dict[str, Any] = dict(ui_raw)
            sizes = normalize_main_splitter_sizes(ui.get("main_splitter_sizes"))
            if sizes is None:
                ui.pop("main_splitter_sizes", None)
            else:
                ui["main_splitter_sizes"] = sizes
            return (
                AppSettings(
                    version=version,
                    hotkeys=hotkeys,
                    launch_configs=launch_configs,
                    ui=ui,
                ),
                None,
            )
        except Exception as exc:
            backup = self.path.with_suffix(self.path.suffix + ".bak")
            try:
                shutil.copy2(self.path, backup)
            except OSError:
                pass
            return AppSettings.defaults(), f"设置文件损坏，已恢复默认（{exc}）"

    def save(self, settings: AppSettings) -> None:
        self._validate_hotkeys(settings.hotkeys)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": settings.version,
            "hotkeys": settings.hotkeys,
            "launch_configs": settings.launch_configs,
            "ui": settings.ui or {},
        }
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.path)

    def get_launch_overlay(self, settings: AppSettings, script_key: str) -> LaunchParameters | None:
        entry = settings.launch_configs.get(script_key)
        if not entry:
            return None
        params = entry.get("parameters")
        if not isinstance(params, dict):
            return None
        return LaunchParameters.from_dict(params)

    def set_launch_overlay(
        self,
        settings: AppSettings,
        script_key: str,
        params: LaunchParameters,
    ) -> None:
        settings.launch_configs[script_key] = {
            "updated_at": datetime.now(UTC).isoformat(timespec="seconds"),
            "parameters": params.to_dict(),
        }

    @staticmethod
    def _validate_hotkeys(hotkeys: dict[str, dict[str, Any]]) -> None:
        keys: list[str] = []
        for action in ("start", "pause", "stop"):
            if action not in hotkeys:
                raise ValueError(f"缺少快捷键动作: {action}")
            key = str(hotkeys[action].get("key", "")).upper()
            if not key:
                raise ValueError(f"快捷键为空: {action}")
            keys.append(key)
        if len(set(keys)) != 3:
            raise ValueError("启动/暂停/结束快捷键不能重复")
