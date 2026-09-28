"""Build NGE2 from LaunchParameters."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from nge_studio.catalog.models import LaunchParameters

EngineFactory = Callable[[LaunchParameters, Path], Any]


def create_nge2_engine(params: LaunchParameters, script_dir: Path) -> Any:
    from nge2 import NGE2

    resource = Path(params.resource_dir)
    if not resource.is_absolute():
        resource = (script_dir / resource).resolve()
    log_dir = params.log_dir
    if log_dir is not None and str(log_dir).strip() != "":
        log_path: Path | None = Path(log_dir)
        if not log_path.is_absolute():
            log_path = (script_dir / log_path).resolve()
    else:
        log_path = None

    yolo_model = params.yolo_model
    yolo_names = params.yolo_names
    kwargs: dict[str, Any] = {
        "resource_dir": resource,
        "capture": params.capture,
        "hwnd": params.hwnd,
        "humanize": params.humanize,
        "control_mode": params.control_mode,
        "log_dir": log_path,
        "yolo_model": yolo_model,
        "yolo_names": yolo_names,
        "ocr_kwargs": params.ocr_kwargs,
    }
    return NGE2(**kwargs)


def default_engine_factory(params: LaunchParameters, script_dir: Path) -> Any:
    return create_nge2_engine(params, script_dir)
