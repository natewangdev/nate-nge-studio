"""Handler restore / NGE2 logging bootstrap patch."""

from __future__ import annotations

import logging

from nge_studio.logging_bridge.qt_handler import (
    attach_nge_handler,
    restore_nge_handlers,
    snapshot_nge_handlers,
)
from nge_studio.runner.engine_factory import _patch_nge2_logging_bootstrap


def test_restore_after_clear() -> None:
    root = logging.getLogger("nge")
    old = list(root.handlers)
    root.handlers.clear()
    try:
        lines: list[str] = []
        handler = logging.Handler()
        handler.emit = lambda record: lines.append(record.getMessage())  # type: ignore[method-assign]
        attach_nge_handler(handler)
        preserved = snapshot_nge_handlers()
        root.handlers.clear()
        root.addHandler(logging.StreamHandler())
        assert handler not in root.handlers
        restore_nge_handlers(preserved)
        assert handler in root.handlers
        logging.getLogger("nge.test").info("hello-ui")
        assert any("hello-ui" in m for m in lines)
    finally:
        root.handlers.clear()
        for h in old:
            root.addHandler(h)


def test_patch_prevents_clear() -> None:
    import nge2.log as nge_log

    root = logging.getLogger("nge")
    old_handlers = list(root.handlers)
    old_configured = nge_log._configured
    old_fn = nge_log._configure_root
    root.handlers.clear()
    try:
        nge_log._configured = False
        lines: list[str] = []
        handler = logging.Handler()
        handler.emit = lambda record: lines.append(record.getMessage())  # type: ignore[method-assign]
        attach_nge_handler(handler)
        _patch_nge2_logging_bootstrap()
        nge_log._configure_root()
        assert handler in root.handlers
        logging.getLogger("nge.x").info("kept")
        assert any("kept" in m for m in lines)
    finally:
        nge_log._configure_root = old_fn
        nge_log._configured = old_configured
        if hasattr(nge_log, "_studio_logging_patched"):
            delattr(nge_log, "_studio_logging_patched")
        root.handlers.clear()
        for h in old_handlers:
            root.addHandler(h)
