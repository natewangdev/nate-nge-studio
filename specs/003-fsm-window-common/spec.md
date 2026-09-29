# Feature Specification: FSM State, Window Title, Game Commons

**Feature Branch**: `003-fsm-window-common`  
**Created**: 2026-09-30  
**Status**: Draft  

**Input**: Implement clarifications already recorded in `001` (Session 2026-09-30) and `002` (Session 2026-09-30): dataclass FSM for RuleLoop; `window_title` resolve + activate; game-level `common.py`/`rules.py` with demo usage.

**Authority**: Product requirements live in [`../001-nge-studio-mvp/spec.md`](../001-nge-studio-mvp/spec.md) (FR-005f/g, FR-017) and [`../002-script-rules/spec.md`](../002-script-rules/spec.md) (FR-008/009/011). This feature tracks implementation only.

## Clarifications

Inherited from 001/002 Session 2026-09-30 (dataclass required; title contains-match first; miss fails Start; hwnd wins; activate after construct; `common.py`+`rules.py`).

## User Stories

### US1 — Dataclass FSM on RuleLoop (P1)
Authors pass `@dataclass` FSM to `RuleLoop.run`; rules use `rctx.state.field`; dict rejected.

### US2 — window_title + activate (P1)
UI + LaunchParameters `window_title`; resolve hwnd; activate bound window before `run`.

### US3 — Game common modules + demo (P1)
`demo/common.py` + `demo/rules.py`; loader puts game dir on `sys.path`; smoke uses them + FSM.
