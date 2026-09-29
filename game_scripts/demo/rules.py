"""Shared demo rules (imported by smoke)."""

from __future__ import annotations

import logging

import common as demo_common

from nge_studio.rules import RuleContext

log = logging.getLogger("nge.demo.rules")


def capture_probe(rctx: RuleContext) -> bool:
    """Real NGE2 perception path: grab one frame when capture is available."""
    engine = rctx.engine
    capture = getattr(engine, "capture", None)
    if capture is None or not hasattr(capture, "grab"):
        log.warning("capture_probe: engine 无 capture.grab，跳过本 tick")
        return False
    try:
        frame = capture.grab()
    except Exception as exc:
        log.warning("capture_probe: grab 失败（可降级）: %s", exc)
        return False
    shape = getattr(frame, "shape", None)
    log.info("capture_probe: grab ok shape=%s", shape)
    rctx.state.last_grab_ok = True
    rctx.state.last_grab_shape = shape
    return True


def heartbeat(rctx: RuleContext) -> bool:
    rctx.state.beats = int(rctx.state.beats) + 1
    log.info(
        "%s",
        demo_common.format_heartbeat(rctx.state.beats, grab_ok=bool(rctx.state.last_grab_ok)),
    )
    if hasattr(rctx.engine, "log"):
        try:
            rctx.engine.log.info("demo heartbeat %s", rctx.state.beats)
        except Exception:
            pass
    return True
