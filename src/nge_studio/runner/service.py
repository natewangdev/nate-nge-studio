"""Single-flight script runner on a worker thread."""

from __future__ import annotations

import logging
import threading
from collections.abc import Callable
from enum import Enum
from typing import Any

from nge_studio.catalog.models import LaunchParameters, Script
from nge_studio.runner.context import RunContext
from nge_studio.runner.engine_factory import EngineFactory, default_engine_factory
from nge_studio.runner.loader import load_run_callable

log = logging.getLogger("nge.studio.runner")

HUNG_GRACE_SEC = 10.0


class RunState(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPING = "stopping"


class ScriptRunner:
    """Owns at most one active script run."""

    def __init__(
        self,
        *,
        engine_factory: EngineFactory | None = None,
        on_state: Callable[[RunState, str | None], None] | None = None,
        on_error: Callable[[str], None] | None = None,
        on_hung: Callable[[], None] | None = None,
        on_finished: Callable[[], None] | None = None,
    ) -> None:
        self._engine_factory = engine_factory or default_engine_factory
        self._on_state = on_state
        self._on_error = on_error
        self._on_hung = on_hung
        self._on_finished = on_finished
        self._lock = threading.RLock()
        self._state = RunState.IDLE
        self._thread: threading.Thread | None = None
        self._ctx: RunContext | None = None
        self._timeout_timer: threading.Timer | None = None
        self._script_key: str | None = None

    @property
    def state(self) -> RunState:
        with self._lock:
            return self._state

    @property
    def script_key(self) -> str | None:
        with self._lock:
            return self._script_key

    def start(self, script: Script, params: LaunchParameters) -> None:
        with self._lock:
            if self._state != RunState.IDLE:
                raise RuntimeError("已有脚本在运行，同一时间只能运行一个")
            params.validate_for_start()
            self._ctx = RunContext()
            self._script_key = script.key
            self._set_state_unlocked(RunState.RUNNING)
            self._thread = threading.Thread(
                target=self._worker,
                args=(script, params, self._ctx),
                name=f"nge-script-{script.key}",
                daemon=True,
            )
            self._thread.start()
            if params.run_duration_sec and params.run_duration_sec > 0:
                self._timeout_timer = threading.Timer(
                    float(params.run_duration_sec),
                    self._on_timeout,
                )
                self._timeout_timer.daemon = True
                self._timeout_timer.start()

    def pause(self) -> None:
        with self._lock:
            if self._state != RunState.RUNNING or self._ctx is None:
                return
            self._ctx.set_paused(True)
            self._set_state_unlocked(RunState.PAUSED)

    def resume(self) -> None:
        with self._lock:
            if self._state != RunState.PAUSED or self._ctx is None:
                return
            self._ctx.set_paused(False)
            self._set_state_unlocked(RunState.RUNNING)

    def stop(self) -> None:
        with self._lock:
            if self._state in (RunState.IDLE, RunState.STOPPING) or self._ctx is None:
                return
            self._cancel_timeout_unlocked()
            self._ctx.request_stop()
            self._set_state_unlocked(RunState.STOPPING)
            thread = self._thread
        if thread is not None and thread.is_alive():
            thread.join(timeout=HUNG_GRACE_SEC)
            if thread.is_alive() and self._on_hung:
                self._on_hung()

    def _on_timeout(self) -> None:
        log.info("Studio 运行时长超时，正在结束")
        try:
            self.stop()
        except Exception:
            log.exception("超时结束失败")

    def _worker(self, script: Script, params: LaunchParameters, ctx: RunContext) -> None:
        engine: Any = None
        try:
            run = load_run_callable(script.path)
            engine = self._engine_factory(params, script.path)
            run(engine, ctx)
        except Exception as exc:
            # ScriptStopped is a clean exit
            from nge_studio.runner.context import ScriptStopped

            if isinstance(exc, ScriptStopped):
                log.info("脚本协作式结束: %s", script.key)
            else:
                log.exception("脚本运行错误: %s", script.key)
                if self._on_error:
                    self._on_error(str(exc))
        finally:
            if engine is not None:
                close = getattr(engine, "close", None)
                if callable(close):
                    try:
                        close()
                    except Exception:
                        log.exception("关闭引擎失败")
            with self._lock:
                self._cancel_timeout_unlocked()
                self._thread = None
                self._ctx = None
                self._script_key = None
                self._set_state_unlocked(RunState.IDLE)
            if self._on_finished:
                self._on_finished()

    def _cancel_timeout_unlocked(self) -> None:
        if self._timeout_timer is not None:
            self._timeout_timer.cancel()
            self._timeout_timer = None

    def _set_state_unlocked(self, state: RunState) -> None:
        self._state = state
        if self._on_state:
            self._on_state(state, self._script_key)
