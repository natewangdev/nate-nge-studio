"""Runner integration with fake engine."""

from __future__ import annotations

import logging
import time
from pathlib import Path

import pytest

from nge_studio.catalog.models import LaunchParameters, Manifest, Script
from nge_studio.runner.service import RunState, ScriptRunner


class FakeEngine:
    def __init__(self) -> None:
        self.closed = False
        self.log = logging.getLogger("nge.fake")

    def close(self) -> None:
        self.closed = True


def _script(tmp_path: Path, body: str) -> Script:
    d = tmp_path / "demo" / "s"
    d.mkdir(parents=True)
    (d / "manifest.json").write_text('{"display_name":"S"}', encoding="utf-8")
    (d / "main.py").write_text(body, encoding="utf-8")
    return Script(
        game_id="demo",
        script_id="s",
        path=d,
        manifest=Manifest(display_name="S"),
    )


def test_single_flight_and_stop(tmp_path: Path) -> None:
    body = """
import time
def run(engine, ctx):
    while not ctx.should_stop():
        ctx.wait_if_paused()
        time.sleep(0.05)
"""
    script = _script(tmp_path, body)
    engines: list[FakeEngine] = []

    def factory(params, script_dir):
        eng = FakeEngine()
        engines.append(eng)
        return eng

    runner = ScriptRunner(engine_factory=factory)
    params = LaunchParameters(resource_dir=".")
    runner.start(script, params)
    time.sleep(0.1)
    assert runner.state in (RunState.RUNNING, RunState.PAUSED)
    with pytest.raises(RuntimeError):
        runner.start(script, params)
    runner.pause()
    time.sleep(0.05)
    assert runner.state == RunState.PAUSED
    runner.resume()
    time.sleep(0.05)
    runner.stop()
    time.sleep(0.2)
    assert runner.state == RunState.IDLE
    assert engines and engines[0].closed


def test_timeout_stops(tmp_path: Path) -> None:
    body = """
import time
def run(engine, ctx):
    while not ctx.should_stop():
        time.sleep(0.05)
"""
    script = _script(tmp_path, body)
    engines: list[FakeEngine] = []

    def factory(params, script_dir):
        eng = FakeEngine()
        engines.append(eng)
        return eng

    runner = ScriptRunner(engine_factory=factory)
    runner.start(script, LaunchParameters(resource_dir=".", run_duration_sec=0.2))
    time.sleep(0.8)
    assert runner.state == RunState.IDLE
    assert engines and engines[0].closed
