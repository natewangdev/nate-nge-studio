"""Build NGE2 from LaunchParameters."""

from __future__ import annotations

import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any

from nge_studio.catalog.models import LaunchParameters
from nge_studio.logging_bridge.qt_handler import restore_nge_handlers, snapshot_nge_handlers

EngineFactory = Callable[[LaunchParameters, Path], Any]

log = logging.getLogger("nge.studio.engine")


def _patch_nge2_logging_bootstrap() -> None:
    """Prevent NGE2 from wiping host-attached ``nge`` handlers (UI live log)."""
    import nge2.log as nge_log

    if getattr(nge_log, "_studio_logging_patched", False):
        return

    def _configure_root_preserve_host() -> None:
        if nge_log._configured:
            return
        root = logging.getLogger("nge")
        has_stream = any(
            isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)
            for h in root.handlers
        )
        if not has_stream:
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter(nge_log._LOG_FORMAT, datefmt=nge_log._LOG_DATEFMT)
            )
            root.addHandler(handler)
        root.setLevel(nge_log._DEFAULT_LEVEL)
        root.propagate = False
        nge_log._configured = True

    nge_log._configure_root = _configure_root_preserve_host  # type: ignore[method-assign]
    nge_log._studio_logging_patched = True  # type: ignore[attr-defined]


def create_nge2_engine(params: LaunchParameters, script_dir: Path) -> Any:
    from nge2 import NGE2

    _patch_nge2_logging_bootstrap()

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
        "humanize": params.humanize,
        "control_mode": params.control_mode,
        "log_dir": log_path,
        "yolo_model": yolo_model,
        "yolo_names": yolo_names,
        "ocr_kwargs": params.ocr_kwargs,
    }
    preserved = snapshot_nge_handlers()
    log.info("正在初始化 NGE2（截屏 / OCR / YOLO / HID，可能需要数秒）…")
    engine: Any = None
    try:
        from nge_studio.runner.window_resolve import resolve_hwnd_for_launch

        hwnd = resolve_hwnd_for_launch(params)
        kwargs["hwnd"] = hwnd
        engine = NGE2(**kwargs)
        if hwnd is not None:
            log.info("正在激活绑定窗口 hwnd=%s…", hwnd)
            try:
                engine.window.activate()
            except Exception:
                try:
                    engine.close()
                except Exception:
                    log.exception("激活失败后关闭引擎出错")
                raise
    finally:
        restore_nge_handlers(preserved)
    log.info("NGE2 初始化完成")
    return engine


def default_engine_factory(params: LaunchParameters, script_dir: Path) -> Any:
    return create_nge2_engine(params, script_dir)
