# Contract: Script Entry Protocol

**Feature**: `001-nge-studio-mvp` | **Date**: 2026-09-28

Chinese companion: [`script-protocol.zh-CN.md`](./script-protocol.zh-CN.md).

This is the contract between NGE-STUDIO and each catalog script.

## Layout

```text
game_scripts/<game_id>/
  common.py          # optional — shared helpers for this game (not a catalog script)
  rules.py           # optional — shared rules for this game (not a catalog script)
  <script_id>/
    manifest.json    # required — see manifest-schema.md
    main.py          # required — must define run()
    ...              # optional resources referenced by parameters
```

Catalog discovery walks **only** `<game_id>/<script_id>/` directories. Files `common.py` / `rules.py` at the game level MUST NOT be treated as scripts. When loading a script, Studio MUST put the game directory on `sys.path` (or equivalent) so `import common` / `import rules` work from `main.py`.

## Entry point

```python
from nge2 import NGE2
# RunContext imported from nge_studio (exact import path fixed at implement)

def run(engine: NGE2, ctx: "RunContext") -> None:
    """Called by Studio on a worker thread after NGE2 is constructed."""
    ...
```

Rules:

- Studio imports `main` from the script directory (sys.path / importlib per implement plan) and calls `run`.
- Studio owns construction and `close()` of `engine` (caller MUST NOT rely on keeping the engine after return).
- `run` SHOULD return promptly after `ctx.should_stop()` becomes true.
- Long loops MUST call `ctx.wait_if_paused()` or `ctx.checkpoint()` regularly so pause/stop remain cooperative within SC-003 targets.

## RunContext (conceptual)

| Member | Behavior |
|--------|----------|
| `is_paused() -> bool` | True while Pause is active |
| `should_stop() -> bool` | True after Stop or Studio timeout |
| `wait_if_paused(poll_sec=0.05) -> None` | Blocks while paused; returns when resumed or stop requested |
| `checkpoint() -> None` | `wait_if_paused()` then raise/return path if stop requested (implement chooses `ScriptStop` exception vs bool; document in code — prefer raising a Studio-defined `ScriptStopped` for clean unwind) |

Recommended pattern:

```python
def run(engine, ctx):
    while not ctx.should_stop():
        ctx.wait_if_paused()
        if ctx.should_stop():
            break
        # do one unit of work...
```

## Lifecycle guarantees from Studio

1. At most one `run` active process-wide.
2. On Stop/timeout: set stop → wait up to **10s** join → `engine.close()` in `finally` when worker exits; if join exceeds 10s, set hung warning (no force-kill in MVP).
3. Logging under logger hierarchy `nge` is mirrored to the UI panel for the active session.

## Non-goals

- Alternate entry names (`main()`, `__call__`) in MVP
- Async `async def run` in MVP
