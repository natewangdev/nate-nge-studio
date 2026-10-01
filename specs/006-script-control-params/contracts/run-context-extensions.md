# Contract: RunContext Self-Stop & Duration End Action

**Feature**: `006-script-control-params` | **Date**: 2026-10-02

Extends [`../../001-nge-studio-mvp/contracts/script-protocol.md`](../../001-nge-studio-mvp/contracts/script-protocol.md).

## RunContext additions

| Member | Behavior |
|--------|----------|
| `request_stop() -> None` | Script-callable; sets stop (and clears pause blocking) like Studio Stop signal |
| `script_params` | Read-only mapping of resolved per-script params for this Start (empty if none) |
| `should_stop() -> bool` | True after UI Stop, Studio timeout, **or** `request_stop()` |

Entry signature unchanged:

```python
def run(engine: NGE2, ctx: RunContext) -> None:
    ...
    ctx.request_stop()
```

## Duration end action (Studio-owned)

Canonical stored values: `none` | `shutdown` (UI labels: 无 | 关机). Default: `none`.

| Event | `none` | `shutdown` |
|-------|--------|------------|
| Duration timeout | Stop path only (001 FR-012) | Stop path, then forced OS shutdown |
| UI Stop | Stop only | Stop only (no shutdown) |
| `ctx.request_stop()` | Stop only | Stop only (no shutdown) |

Shutdown executor MUST be injectable for tests.
