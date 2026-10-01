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


def control_tick(rctx: RuleContext) -> bool:
    """control_params demo: count ticks then request_stop."""
    state = rctx.state
    state.ticks = int(state.ticks) + 1
    if state.verbose:
        log.info("tick %s/%s (%s) mode=%s", state.ticks, state.max_ticks, state.greeting, state.mode)
    if state.ticks >= int(state.max_ticks):
        log.info("达到 max_ticks，调用 ctx.request_stop()（不会触发关机）")
        rctx.studio.request_stop()
    return True
