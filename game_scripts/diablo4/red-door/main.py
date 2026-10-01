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

log = logging.getLogger("nge.diablo4.red-door")

TARGET_MAP_NAME = "憎恨大厅"

@dataclass
class FSM:
    STATE: common.GameState = common.GameState.NOT_IN_PARTY
    FRIEND_NAME: str = "路西法"

loop = RuleLoop(one_action_per_tick=True, tick_interval_sec=0.25)
loop.add_rule(rules.goto_team, name="goto_team", priority=30, cooldown=5.0)
loop.add_rule(rules.fallback_behavior, name="fallback_behavior", priority=0, cooldown=1.0)

@loop.rule(name="click_bag_close", priority=20, cooldown=0.8)
def click_bag_close(ctx: RuleContext) -> bool:
    return True

@loop.rule(name="town_press_i", priority=10, cooldown=1.0)
def town_press_i(ctx: RuleContext) -> bool:
    return True

def run(engine: NGE2, ctx: RunContext) -> None:
    log.info("脚本启动 (engine=%s)", type(engine).__name__)
    loop.run(engine, ctx, state=FSM())
    log.info("脚本结束")
