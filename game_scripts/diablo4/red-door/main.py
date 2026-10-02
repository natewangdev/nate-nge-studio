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

log = logging.getLogger("nge.d4.red-door")

@dataclass
class FSM:
    STATE: common.GameState = common.GameState.NOT_IN_PARTY
    FRIEND_NAME: str = ""
    TARGET_MAP_NAME = "崔斯特姆的回响"

loop = RuleLoop(one_action_per_tick=True, tick_interval_sec=0.25)
loop.add_rule(rules.team_up, name="组队", priority=100, cooldown=5.0)
loop.add_rule(rules.fallback_behavior, name="兜底", priority=0, cooldown=1.0)

def run(engine: NGE2, ctx: RunContext) -> None:
    friend_name = str(ctx.script_params.get("friend_name", "路西法"))
    log.info(
        "脚本启动 (engine=%s) friend_name=%s",
        type(engine).__name__,
        friend_name,
    )
    loop.run(engine, ctx, state=FSM(FRIEND_NAME=friend_name))
    log.info("脚本结束")
