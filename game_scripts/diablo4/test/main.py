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
    common.walk(ctx, -104.9, 458.4, ctx.state.SPEED)
    common.walk(ctx, -48.5, 592.9, ctx.state.SPEED)
    common.walk(ctx, -31.3, 446.9, ctx.state.SPEED)
    common.walk(ctx, -66.9, 323.9, ctx.state.SPEED)
   
    if ctx.state.EXECUTE_ONCE == 1:
        ctx.studio.request_stop()
    return True

# @loop.rule(name="测试拾取物品", priority=50, cooldown=0.0)
def test_walk(ctx: RuleContext) -> bool:
    log.info("--------------【测试拾取物品】---------------")
    common.loot(ctx)
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
