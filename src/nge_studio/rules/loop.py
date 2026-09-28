"""RuleLoop: priority/cooldown tick loop bound to Studio RunContext."""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from typing import Any

from nge_studio.rules.models import Rule, RuleContext, RuleFn
from nge_studio.runner.context import ScriptStopped

log = logging.getLogger("nge.studio.rules")


class RuleLoop:
    """Slim decision loop (legacy Bot-inspired; Studio owns lifecycle)."""

    def __init__(
        self,
        *,
        one_action_per_tick: bool = True,
        tick_interval_sec: float = 0.1,
    ) -> None:
        if tick_interval_sec < 0:
            raise ValueError("tick_interval_sec must be >= 0")
        self.one_action_per_tick = bool(one_action_per_tick)
        self.tick_interval_sec = float(tick_interval_sec)
        self.state: dict[str, Any] = {}
        self._rules: list[Rule] = []

    def add_rule(
        self,
        fn: RuleFn,
        *,
        name: str | None = None,
        priority: int = 0,
        cooldown: float = 0.0,
    ) -> Rule:
        rule = Rule(
            name=name or getattr(fn, "__name__", "rule"),
            fn=fn,
            priority=int(priority),
            cooldown=float(cooldown),
        )
        self._rules.append(rule)
        return rule

    def rule(
        self,
        name: str | None = None,
        *,
        priority: int = 0,
        cooldown: float = 0.0,
    ) -> Callable[[RuleFn], RuleFn]:
        def decorator(fn: RuleFn) -> RuleFn:
            self.add_rule(fn, name=name, priority=priority, cooldown=cooldown)
            return fn

        return decorator

    def run(self, engine: Any, studio_ctx: Any) -> None:
        """Block until Studio stop; honor pause via ``checkpoint`` each tick."""
        for rule in self._rules:
            rule._last_fired = None
        log.info(
            "RuleLoop start (%s rules, interval=%.3fs, one_action=%s)",
            len(self._rules),
            self.tick_interval_sec,
            self.one_action_per_tick,
        )
        try:
            while not studio_ctx.should_stop():
                try:
                    studio_ctx.checkpoint()
                except ScriptStopped:
                    break
                self._tick(engine, studio_ctx)
                if studio_ctx.should_stop():
                    break
                if self.tick_interval_sec > 0:
                    time.sleep(self.tick_interval_sec)
        finally:
            log.info("RuleLoop end")

    def _tick(self, engine: Any, studio_ctx: Any) -> None:
        now = time.monotonic()
        rctx = RuleContext(engine=engine, state=self.state, studio=studio_ctx)
        ordered = sorted(self._rules, key=lambda r: r.priority, reverse=True)
        for rule in ordered:
            if not rule.ready(now):
                continue
            try:
                acted = bool(rule.fn(rctx))
            except Exception:
                log.exception("Rule %r raised; skipping rest of tick", rule.name)
                return
            if acted:
                rule.mark_fired(now)
                if self.one_action_per_tick:
                    return
