"""Helpers for launch-parameter path browse dialogs (FR-005a–c)."""

from __future__ import annotations

from pathlib import Path


def browse_start_directory(resource_dir: str) -> str:
    """Return dialog start dir: existing ``resource_dir``, else user home."""
    text = (resource_dir or "").strip()
    if text:
        path = Path(text)
        if path.is_dir():
            return str(path.resolve())
    return str(Path.home())


def store_picked_path(picked: str, resource_dir: str) -> str:
    """Store relative to ``resource_dir`` when under it; otherwise absolute."""
    picked_path = Path(picked).resolve()
    root_text = (resource_dir or "").strip()
    if root_text:
        root = Path(root_text)
        if root.is_dir():
            try:
                return picked_path.relative_to(root.resolve()).as_posix()
            except ValueError:
                pass
    return str(picked_path)


def hours_to_seconds(hours: float) -> float:
    return hours * 3600.0


def seconds_to_hours_text(seconds: float) -> str:
    hours = seconds / 3600.0
    if hours == int(hours):
        return str(int(hours))
    text = f"{hours:.6f}".rstrip("0").rstrip(".")
    return text
