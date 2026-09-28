"""Demo smoke script — RuleLoop + cooperative Studio pause/stop."""

from __future__ import annotations

import logging
from typing import Any

from nge_studio.rules import RuleContext, RuleLoop

log = logging.getLogger("nge.demo.smoke")

loop = RuleLoop(one_action_per_tick=True, tick_interval_sec=0.5)


@loop.rule(name="capture_probe", priority=20, cooldown=2.0)
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
    rctx.state["last_grab_ok"] = True
    rctx.state["last_grab_shape"] = shape
    return True


@loop.rule(name="heartbeat", priority=1, cooldown=0.0)
def heartbeat(rctx: RuleContext) -> bool:
    n = int(rctx.state.get("beats", 0)) + 1
    rctx.state["beats"] = n
    log.info("心跳 #%s (grab_ok=%s)", n, rctx.state.get("last_grab_ok"))
    if hasattr(rctx.engine, "log"):
        try:
            rctx.engine.log.info("demo heartbeat %s", n)
        except Exception:
            pass
    return True


def run(engine: Any, ctx: Any) -> None:
    """Studio entry: engine may be real NGE2 or a test fake."""
    log.info("冒烟脚本启动 RuleLoop (engine=%s)", type(engine).__name__)
    loop.state.clear()
    loop.run(engine, ctx)
    log.info("冒烟脚本结束")
