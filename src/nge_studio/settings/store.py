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


def default_settings_path() -> Path:
    base = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
    return Path(base) / "NGE-STUDIO" / "settings.json"


@dataclass
class AppSettings:
    version: int
    hotkeys: dict[str, dict[str, Any]]
    launch_configs: dict[str, dict[str, Any]]

    @classmethod
    def defaults(cls) -> AppSettings:
        return cls(version=1, hotkeys=dict(DEFAULT_HOTKEYS), launch_configs={})


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
            return (
                AppSettings(version=version, hotkeys=hotkeys, launch_configs=launch_configs),
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
