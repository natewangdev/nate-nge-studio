"""Resolve packaged/static resource paths (icons, etc.)."""

from __future__ import annotations

import sys
from pathlib import Path


class ResourceError(FileNotFoundError):
    """Raised when a required product resource is missing."""


def _repo_root() -> Path:
    # src/nge_studio/resources.py → parents[2] = repo root
    return Path(__file__).resolve().parents[2]


def resolve_app_icon(*, required: bool = True) -> Path:
    """Return path to ``assets/icons/app.ico`` for Qt and packaging.

    Search order:
    1. Frozen: ``sys._MEIPASS/assets/icons/app.ico``
    2. Frozen: beside executable ``assets/icons/app.ico``
    3. Dev: repo ``assets/icons/app.ico``
    """
    candidates: list[Path] = []
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            candidates.append(Path(meipass) / "assets" / "icons" / "app.ico")
        candidates.append(Path(sys.executable).resolve().parent / "assets" / "icons" / "app.ico")
    candidates.append(_repo_root() / "assets" / "icons" / "app.ico")

    for path in candidates:
        if path.is_file():
            return path.resolve()

    msg = "缺少产品图标 assets/icons/app.ico（已搜索: " + ", ".join(str(p) for p in candidates) + ")"
    if required:
        raise ResourceError(msg)
    raise ResourceError(msg)
