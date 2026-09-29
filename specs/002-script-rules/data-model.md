# Data Model: Script Rule Helper

**Feature**: `002-script-rules` | **Date**: 2026-09-28

## Rule

| Field | Type | Rules |
|-------|------|-------|
| name | str | Non-empty; used in logs |
| priority | int | Higher runs earlier; default `0` |
| cooldown | float | Seconds ≥ 0; default `0`; refreshed only after `fn` returns `True` |
| fn | Callable[[RuleContext], bool] | `True` = acted this tick |

Internal: `_last_fired: float | None` for cooldown readiness.

## RuleContext

| Field | Type | Rules |
|-------|------|-------|
| engine | Any / NGE2 | Studio-constructed NGE2 or test fake |
| state | dataclass instance | **Required** author `@dataclass` FSM; attribute access only; **not** `dict` |
| studio | RunContext | Pause/stop signals (read-only usage by rules; loop owns checkpointing) |

Rules MAY read `studio.should_stop()` but MUST NOT replace loop-owned pause gating.

## RuleLoop

| Field | Type | Rules |
|-------|------|-------|
| rules | list[Rule] | Sorted by priority descending each tick |
| one_action_per_tick | bool | Default `True` |
| tick_interval_sec | float | Default `0.1`; sleep between ticks; **no jitter** |
| state | dataclass instance | Set for the run via `run(..., state=...)`; same object on each `RuleContext` |

### Lifecycle

```text
run(engine, studio_ctx, state: DataclassFSM):
  require is_dataclass(state) and not isinstance(state, type)
  while not studio_ctx.should_stop():
    studio_ctx.checkpoint()   # wait if paused; raise/return on stop
    evaluate ready rules...   # rctx.state is the FSM instance
    sleep(tick_interval_sec)
```

No `session_max`, no framework pause API on `RuleLoop`. Dict state is rejected.
