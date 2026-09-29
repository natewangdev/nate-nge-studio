"""Rule dataclasses for Studio script decision loops."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field, is_dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from nge2 import NGE2

    from nge_studio.runner.context import RunContext


def require_dataclass_fsm(state: Any) -> Any:
    """Validate author FSM: must be a dataclass *instance*, not a dict or type."""
    if state is None or isinstance(state, dict):
        raise TypeError("RuleLoop.state 必须是 @dataclass 实例，不支持 dict")
    if isinstance(state, type) or not is_dataclass(state):
        raise TypeError("RuleLoop.state 必须是 @dataclass 实例")
    return state


@dataclass
class RuleContext:
    """Per-tick context passed to rule functions."""

    engine: NGE2
    state: Any  # author @dataclass FSM instance
    studio: RunContext


RuleFn = Callable[[RuleContext], bool]


@dataclass
class Rule:
    """Named decision unit: priority, cooldown, and act callback."""

    name: str
    fn: RuleFn
    priority: int = 0
    cooldown: float = 0.0
    _last_fired: float | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if not self.name or not str(self.name).strip():
            raise ValueError("Rule.name must be non-empty")
        if self.cooldown < 0:
            raise ValueError("Rule.cooldown must be >= 0")

    def ready(self, now: float) -> bool:
        if self._last_fired is None or self.cooldown <= 0:
            return True
        return (now - self._last_fired) >= self.cooldown

    def mark_fired(self, now: float) -> None:
        self._last_fired = now
