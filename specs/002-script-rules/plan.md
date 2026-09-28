# Implementation Plan: Script Rule Helper

**Branch**: `002-script-rules` | **Date**: 2026-09-28 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-script-rules/spec.md`

Chinese companion: [`plan.zh-CN.md`](./plan.zh-CN.md).

## Summary

Add a reusable **Rule loop helper** under `nge_studio.rules` inspired by legacy
nate-gaming-engine `Bot`/`Rule` (priority, cooldown, one-action-per-tick, shared state),
bound to Studio `RunContext` for pause/stop. Omit Bot session max, tick jitter, and
`break_every`. Rewrite `demo/smoke` to use the helper with at least one rule that calls
real NGE2 perception and/or control APIs. Start / Pause / Stop / run duration remain
Studio UI + runner owned.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Existing Studio stack (`nge_studio`, `nge2`); no new third-party
deps for the Rule helper

**Storage**: N/A (in-memory rule list + shared state for a run)

**Testing**: `pytest` unit tests for helper (fake `RunContext` + stub engine); smoke remains
catalog-valid; no HID required in CI

**Target Platform**: Windows (same as Studio); helper itself is OS-agnostic Python

**Project Type**: Library module inside desktop app package + sample script update

**Performance Goals**: Pause stops further rule actions within ~2s (tick interval + wait);
stop exits cooperatively within existing Studio SC-003

**Constraints**: Must not reimplement Studio lifecycle; must not import legacy `nge.bot`;
slim feature set per clarifications; rule exceptions isolated per tick

**Scale/Scope**: One helper package (`nge_studio.rules`), one rewritten smoke script,
unit tests, bilingual Spec Kit docs for `002`

## Constitution Check

| Gate | Status | Notes |
|------|--------|-------|
| I. Desktop product first | PASS | Helper serves catalog scripts run by the desktop product |
| II. NGE2 sole engine via pip | PASS | Rules receive Studio-constructed `engine`; no alternate engine |
| III. Packaged script catalog | PASS | Smoke stays under `game_scripts/` with manifest + `run` |
| IV. Cooperative + single runner | PASS | Loop gates on existing `RunContext`; no second runner |
| V. Observability & hotkeys | PASS | Unchanged; rules use logging |
| VI–VII. Bilingual artifacts | PASS | EN+zh-CN for this feature’s Spec Kit docs |
| Platform | PASS | No platform change |

**Post-design re-check**: PASS — contracts define helper API only; lifecycle stays in `001`.

## Project Structure

### Documentation (this feature)

```text
specs/002-script-rules/
├── plan.md / plan.zh-CN.md
├── research.md / research.zh-CN.md
├── data-model.md / data-model.zh-CN.md
├── quickstart.md / quickstart.zh-CN.md
├── contracts/
│   ├── rule-helper.md
│   └── rule-helper.zh-CN.md
└── tasks.md
```

### Source Code

```text
src/nge_studio/rules/
├── __init__.py          # export RuleLoop, Rule, RuleContext
├── models.py            # Rule dataclass
└── loop.py              # RuleLoop.run bound to RunContext

game_scripts/demo/smoke/
├── main.py              # rewritten with RuleLoop + NGE2 I/O rule
└── manifest.json        # unchanged protocol; defaults ok

tests/unit/
└── test_rule_loop.py    # priority, cooldown, pause, stop
```

**Structure Decision**: Keep helper inside `nge_studio` (clarification Option B) so scripts
depend on Studio’s author-facing package, not a second Bot in NGE2.

## Complexity Tracking

N/A — no constitution violations.
