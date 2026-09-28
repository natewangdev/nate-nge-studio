"""Demo smoke script — cooperative pause/stop + periodic logs."""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from nge2 import NGE2

    from nge_studio.runner.context import RunContext

log = logging.getLogger("nge.demo.smoke")


def run(engine: Any, ctx: Any) -> None:
    """Studio entry: engine may be real NGE2 or a test fake."""
    log.info("冒烟脚本启动 (engine=%s)", type(engine).__name__)
    ticks = 0
    while not ctx.should_stop():
        ctx.wait_if_paused()
        if ctx.should_stop():
            break
        ticks += 1
        log.info("心跳 #%s", ticks)
        # Light touch on engine if present
        if hasattr(engine, "log"):
            try:
                engine.log.info("demo tick %s", ticks)
            except Exception:
                pass
        time.sleep(0.5)
    log.info("冒烟脚本结束")
