"""Unit tests for RunContext."""

from __future__ import annotations

import threading
import time

import pytest

from nge_studio.runner.context import RunContext, ScriptStopped


def test_pause_and_resume() -> None:
    ctx = RunContext()
    assert not ctx.is_paused()
    ctx.set_paused(True)
    assert ctx.is_paused()
    done = threading.Event()

    def waiter() -> None:
        ctx.wait_if_paused()
        done.set()

    t = threading.Thread(target=waiter)
    t.start()
    time.sleep(0.05)
    assert not done.is_set()
    ctx.set_paused(False)
    t.join(timeout=1)
    assert done.is_set()


def test_checkpoint_raises_on_stop() -> None:
    ctx = RunContext()
    ctx.request_stop()
    with pytest.raises(ScriptStopped):
        ctx.checkpoint()


def test_stop_unblocks_pause() -> None:
    ctx = RunContext()
    ctx.set_paused(True)
    done = threading.Event()

    def waiter() -> None:
        ctx.wait_if_paused()
        done.set()

    t = threading.Thread(target=waiter)
    t.start()
    time.sleep(0.05)
    ctx.request_stop()
    t.join(timeout=1)
    assert done.is_set()
    assert ctx.should_stop()
