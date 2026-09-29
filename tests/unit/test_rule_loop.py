"""Unit tests for RuleLoop (no HID)."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass

import pytest

from nge_studio.rules import RuleContext, RuleLoop
from nge_studio.runner.context import RunContext


@dataclass
class _FSM:
    beats: int = 0
    last_grab_ok: bool = False
    last_grab_shape: object | None = None
    flag: str = ""


class _FakeEngine:
    def __init__(self) -> None:
        self.grabs = 0
        self.capture = self

    def grab(self):
        self.grabs += 1
        return type("F", (), {"shape": (2, 2, 3)})()


def test_priority_one_action_per_tick() -> None:
    loop = RuleLoop(one_action_per_tick=True, tick_interval_sec=0)
    acted: list[str] = []

    @loop.rule(name="low", priority=1)
    def low(rctx: RuleContext) -> bool:
        acted.append("low")
        return True

    @loop.rule(name="high", priority=10)
    def high(rctx: RuleContext) -> bool:
        acted.append("high")
        return True

    ctx = RunContext()

    def stop_soon() -> None:
        time.sleep(0.05)
        ctx.request_stop()

    threading.Thread(target=stop_soon, daemon=True).start()
    loop.run(_FakeEngine(), ctx, state=_FSM())
    assert acted[0] == "high"
    assert all(a == "high" for a in acted)


def test_cooldown_only_after_true() -> None:
    loop = RuleLoop(one_action_per_tick=False, tick_interval_sec=0)
    fires = {"n": 0}

    @loop.rule(name="cd", priority=1, cooldown=10.0)
    def cd(rctx: RuleContext) -> bool:
        fires["n"] += 1
        return True

    ctx = RunContext()
    ticks = {"n": 0}

    def stopper() -> None:
        while ticks["n"] < 3 and not ctx.should_stop():
            time.sleep(0.01)
        ctx.request_stop()

    def run_and_count() -> None:
        original_tick = loop._tick

        def wrapped(engine, studio_ctx) -> None:
            ticks["n"] += 1
            original_tick(engine, studio_ctx)

        loop._tick = wrapped  # type: ignore[method-assign]
        loop.run(_FakeEngine(), ctx, state=_FSM())

    threading.Thread(target=stopper, daemon=True).start()
    run_and_count()
    assert fires["n"] == 1


def test_pause_gates_and_stop_exits() -> None:
    loop = RuleLoop(one_action_per_tick=True, tick_interval_sec=0.02)
    count = {"n": 0}

    @loop.rule(name="work", priority=1)
    def work(rctx: RuleContext) -> bool:
        count["n"] += 1
        return True

    ctx = RunContext()
    ctx.set_paused(True)

    def control() -> None:
        time.sleep(0.08)
        assert count["n"] == 0
        ctx.set_paused(False)
        time.sleep(0.08)
        assert count["n"] > 0
        ctx.request_stop()

    threading.Thread(target=control, daemon=True).start()
    loop.run(_FakeEngine(), ctx, state=_FSM())
    assert ctx.should_stop()


def test_rule_exception_skips_rest_of_tick() -> None:
    loop = RuleLoop(one_action_per_tick=False, tick_interval_sec=0)
    seen: list[str] = []

    @loop.rule(name="boom", priority=10)
    def boom(rctx: RuleContext) -> bool:
        seen.append("boom")
        raise RuntimeError("boom")

    @loop.rule(name="after", priority=1)
    def after(rctx: RuleContext) -> bool:
        seen.append("after")
        return True

    ctx = RunContext()

    def stop_soon() -> None:
        time.sleep(0.05)
        ctx.request_stop()

    threading.Thread(target=stop_soon, daemon=True).start()
    loop.run(_FakeEngine(), ctx, state=_FSM())
    assert "boom" in seen
    assert "after" not in seen


def test_dataclass_fsm_attribute_updates() -> None:
    loop = RuleLoop(one_action_per_tick=True, tick_interval_sec=0)
    fsm = _FSM()

    @loop.rule(name="set", priority=1)
    def set_flag(rctx: RuleContext) -> bool:
        rctx.state.flag = "ok"
        rctx.state.beats += 1
        return True

    ctx = RunContext()

    def stop_soon() -> None:
        time.sleep(0.05)
        ctx.request_stop()

    threading.Thread(target=stop_soon, daemon=True).start()
    loop.run(_FakeEngine(), ctx, state=fsm)
    assert fsm.flag == "ok"
    assert fsm.beats >= 1


def test_dict_state_rejected() -> None:
    loop = RuleLoop(tick_interval_sec=0)
    with pytest.raises(TypeError, match="dataclass"):
        loop.run(_FakeEngine(), RunContext(), state={})  # type: ignore[arg-type]


def test_smoke_capture_probe_with_stub() -> None:
    import importlib.util
    import sys
    from pathlib import Path

    demo_dir = Path(__file__).resolve().parents[2] / "game_scripts" / "demo"
    smoke_path = demo_dir / "smoke" / "main.py"
    sys.path.insert(0, str(demo_dir))
    try:
        spec = importlib.util.spec_from_file_location("smoke_demo_main_test", smoke_path)
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)

        import rules as demo_rules

        engine = _FakeEngine()
        rctx = RuleContext(engine=engine, state=_FSM(), studio=RunContext())
        assert demo_rules.capture_probe(rctx) is True
        assert engine.grabs == 1
        assert rctx.state.last_grab_ok is True
    finally:
        sys.modules.pop("smoke_demo_main_test", None)
        try:
            sys.path.remove(str(demo_dir))
        except ValueError:
            pass
