"""Diablo IV test script — find bag-close template + OCR town name."""

from __future__ import annotations

import logging
import common
from dataclasses import dataclass
from typing import TYPE_CHECKING

from nge_studio.rules import RuleContext, RuleLoop
import rules

if TYPE_CHECKING:
    from nge2 import NGE2

    from nge_studio.runner.context import RunContext

log = logging.getLogger("nge.d4.test")

@dataclass
class FSM:
    EXECUTE_ONCE: int = 1
    SPEED: float = 196.0

loop = RuleLoop(one_action_per_tick=True, tick_interval_sec=0.25)

@loop.rule(name="测试跑图", priority=50, cooldown=0.0)
def test_walk(ctx: RuleContext) -> bool:
    log.info("--------------【测试跑图】---------------")
    common.walk(ctx, -128.4, 365.1, ctx.state.SPEED)
    common.walk(ctx, 135.8, 323.9, ctx.state.SPEED)
    common.walk(ctx, -118.1, 458.1, ctx.state.SPEED)
    common.walk(ctx, -55.8, 466.5, ctx.state.SPEED)
    common.walk(ctx, -51.0, 575.2, ctx.state.SPEED)
    common.walk(ctx, -20.5, 349.0, ctx.state.SPEED)
    common.walk(ctx, 5.6, 412.9, ctx.state.SPEED)
    common.walk(ctx, 36.5, 494.0, ctx.state.SPEED)
    common.walk(ctx, 51.0, 613.6, ctx.state.SPEED)
    common.walk(ctx, 50.1, 609.1, ctx.state.SPEED)
    if ctx.state.EXECUTE_ONCE == 1:
        ctx.studio.request_stop()
    return True

def run(engine: NGE2, ctx: RunContext) -> None:
    execute_once = int(ctx.script_params.get("execute_once", 1))
    log.info(
        "脚本启动 (engine=%s) execute_once=%s",
        type(engine).__name__,
        execute_once,
    )
    loop.run(engine, ctx, state=FSM(EXECUTE_ONCE=execute_once))
    log.info("脚本结束")
