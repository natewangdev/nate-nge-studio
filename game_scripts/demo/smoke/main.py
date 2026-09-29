"""Demo smoke script — RuleLoop + dataclass FSM + game commons."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import rules as demo_rules

from nge_studio.rules import RuleLoop

if TYPE_CHECKING:
    from nge2 import NGE2

    from nge_studio.runner.context import RunContext

log = logging.getLogger("nge.demo.smoke")


@dataclass
class SmokeFSM:
    beats: int = 0
    last_grab_ok: bool = False
    last_grab_shape: Any = None


loop = RuleLoop(one_action_per_tick=True, tick_interval_sec=0.5)
loop.add_rule(demo_rules.capture_probe, name="capture_probe", priority=20, cooldown=2.0)
loop.add_rule(demo_rules.heartbeat, name="heartbeat", priority=1, cooldown=0.0)


def run(engine: NGE2, ctx: RunContext) -> None:
    """Studio entry: engine may be real NGE2 or a test fake."""
    log.info("冒烟脚本启动 RuleLoop (engine=%s)", type(engine).__name__)
    loop.run(engine, ctx, state=SmokeFSM())
    log.info("冒烟脚本结束")
