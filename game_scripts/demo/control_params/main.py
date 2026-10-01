"""Demo: script_params + ctx.request_stop via RuleLoop (006).

Studio UI also exposes duration_end_action (none|shutdown) on the launch form;
shutdown only runs after run_duration timeout — not after request_stop.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

import rules as demo_rules

from nge_studio.rules import RuleLoop

if TYPE_CHECKING:
    from nge2 import NGE2

    from nge_studio.runner.context import RunContext

log = logging.getLogger("nge.demo.control_params")


@dataclass
class ControlParamsFSM:
    greeting: str = "hello"
    max_ticks: int = 3
    verbose: bool = True
    mode: str = "demo"
    ticks: int = 0


loop = RuleLoop(one_action_per_tick=True, tick_interval_sec=0.5)
loop.add_rule(demo_rules.control_tick, name="control_tick", priority=10, cooldown=0.0)


def run(engine: NGE2, ctx: RunContext) -> None:
    params = ctx.script_params
    greeting = str(params.get("greeting", "hello"))
    max_ticks = int(params.get("max_ticks", 3))
    interval = float(params.get("tick_interval_sec", 0.5))
    verbose = bool(params.get("verbose", True))
    mode = str(params.get("mode", "demo"))

    log.info(
        "control_params 启动 RuleLoop (engine=%s) script_params=%s",
        type(engine).__name__,
        params,
    )
    if verbose:
        log.info("问候: %s | mode=%s | max_ticks=%s", greeting, mode, max_ticks)

    loop.tick_interval_sec = max(interval, 0.05)
    loop.run(
        engine,
        ctx,
        state=ControlParamsFSM(
            greeting=greeting,
            max_ticks=max_ticks,
            verbose=verbose,
            mode=mode,
        ),
    )
    log.info("control_params 结束")
