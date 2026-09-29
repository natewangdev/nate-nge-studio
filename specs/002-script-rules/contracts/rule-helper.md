# Contract: Rule Helper API

**Feature**: `002-script-rules` | **Date**: 2026-09-28

Chinese companion: [`rule-helper.zh-CN.md`](./rule-helper.zh-CN.md).

Author-facing API for catalog scripts. Complements (does not replace) MVP
[`script-protocol`](../../001-nge-studio-mvp/contracts/script-protocol.md).

## Import

```python
from dataclasses import dataclass
from nge_studio.rules import RuleLoop, RuleContext

@dataclass
class SmokeFSM:
    beats: int = 0
    last_grab_ok: bool = False

loop = RuleLoop(one_action_per_tick=True, tick_interval_sec=0.1)

@loop.rule(name="probe", priority=10, cooldown=1.0)
def probe(rctx: RuleContext) -> bool:
    rctx.state.beats += 1
    return True

def run(engine, ctx):
    loop.run(engine, ctx, state=SmokeFSM())
```

### Guarantees

| Topic | Behavior |
|-------|----------|
| Pause | Each tick starts with `ctx.checkpoint()`; no rules while paused |
| Stop / timeout | Loop exits when `should_stop` / `ScriptStopped`; no session_max on loop |
| Cooldown | Updated only when `fn` returns `True` |
| Priority | Higher `priority` evaluated first |
| one_action_per_tick | After first `True`, remaining rules skipped that tick |
| Exceptions | Logged; rule treated as non-acting; remaining rules that tick skipped |
| State | **Required** `@dataclass` FSM via `run(..., state=...)`; `rctx.state.field` access; **dict rejected** |
| Omitted | `session_max_seconds`, tick jitter, `break_every` |

### RuleContext

| Attr | Meaning |
|------|---------|
| `engine` | NGE2 instance (or test fake) |
| `state` | Author `@dataclass` FSM for the run |
| `studio` | Studio `RunContext` |

## Non-goals

- Replacing `def run(engine, ctx)` entry
- Owning engine construct/close
- Legacy Bot human-break scheduler
