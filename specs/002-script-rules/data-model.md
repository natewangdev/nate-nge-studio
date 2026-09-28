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
| engine | Any | Studio-constructed NGE2 or test fake |
| state | dict[str, Any] | Shared mutable state for the run |
| studio | RunContext | Pause/stop signals (read-only usage by rules; loop owns checkpointing) |

Rules MAY read `studio.should_stop()` but MUST NOT replace loop-owned pause gating.

## RuleLoop

| Field | Type | Rules |
|-------|------|-------|
| rules | list[Rule] | Sorted by priority descending each tick |
| one_action_per_tick | bool | Default `True` |
| tick_interval_sec | float | Default `0.1`; sleep between ticks; **no jitter** |
| state | dict | Shared; same object exposed on each `RuleContext` |

### Lifecycle

```text
run(engine, studio_ctx):
  while not studio_ctx.should_stop():
    studio_ctx.checkpoint()   # wait if paused; raise/return on stop
    evaluate ready rules...
    sleep(tick_interval_sec)
```

No `session_max`, no framework pause API on `RuleLoop`.
