# Tasks: Script Rule Helper

**Input**: Design documents from `/specs/002-script-rules/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Included — spec FR-011 / SC-003 require helper unit tests without HID.

## Phase 1: Setup

- [x] T001 Confirm package layout `src/nge_studio/rules/` per [plan.md](./plan.md)
- [x] T002 [P] Add bilingual note in feature docs that MVP `run(engine, ctx)` entry is unchanged (already in spec; no code)

## Phase 2: Foundational

- [x] T003 Implement `Rule` dataclass (name, priority, cooldown≥0, fn; readiness via last-fired) in `src/nge_studio/rules/models.py` per data-model
- [x] T004 Implement `RuleContext` (engine, state, studio) in `src/nge_studio/rules/models.py`
- [x] T005 Implement `RuleLoop` (`add_rule`, optional `@rule` decorator, `run` with checkpoint-per-tick, priority sort, cooldown, one_action_per_tick, fixed interval, exception isolation) in `src/nge_studio/rules/loop.py` per [contracts/rule-helper.md](./contracts/rule-helper.md)
- [x] T006 Export public API from `src/nge_studio/rules/__init__.py`

**Checkpoint**: Helper importable; ready for US1 tests

## Phase 3: User Story 1 — Reusable Rule loop (P1)

**Goal**: Authors can register prioritized rules and run under Studio pause/stop  
**Independent Test**: `tests/unit/test_rule_loop.py` with fake RunContext

- [x] T007 [P] [US1] Unit tests: priority + one_action_per_tick in `tests/unit/test_rule_loop.py`
- [x] T008 [P] [US1] Unit tests: cooldown only after True in `tests/unit/test_rule_loop.py`
- [x] T009 [US1] Unit tests: pause gates evaluation; stop exits loop in `tests/unit/test_rule_loop.py`
- [x] T010 [US1] Fix helper until T007–T009 pass

**Checkpoint**: US1 independently testable

## Phase 4: User Story 2 — Smoke with real NGE2 I/O (P1)

**Goal**: Rewrite smoke to use RuleLoop; ≥1 rule calls capture/control API with degrade  
**Independent Test**: Catalog validate + manual Studio run; unit path via stub engine optional

- [x] T011 [US2] Rewrite `game_scripts/demo/smoke/main.py` to use `RuleLoop` with heartbeat rule + `capture.grab` probe rule (degrade on failure)
- [x] T012 [US2] Ensure `manifest.json` still validates; run `scripts/validate_catalog.py`
- [x] T013 [P] [US2] Optional: stub-engine test that smoke `run` invokes grab path in `tests/unit/test_smoke_rules.py` if lightweight

**Checkpoint**: Smoke demonstrates Rule + Studio lifecycle ownership

## Phase 5: User Story 3 — Docs boundaries (P2)

**Goal**: Ownership boundaries documented for authors  
**Independent Test**: Doc review against FR-006/007

- [x] T014 [US3] Verify research/contract/quickstart state omitted Bot features and point to Studio lifecycle (already drafted; spot-fix completeness)
- [x] T015 [P] [US3] Add short author note in `README.md` linking to `specs/002-script-rules/contracts/rule-helper.md` (optional one paragraph)

## Phase 6: Polish

- [x] T016 Run `uv run pytest tests/unit/test_rule_loop.py tests/unit/test_path_browse.py -q` and `ruff check` on new modules
- [x] T017 Mark completed tasks in this file as done during implement

## Dependencies

- Phase 2 before US1/US2
- US1 tests can proceed before smoke (US2)
- US3 docs can parallelize after contracts exist (already written in plan)

## Parallel examples

- T007 ‖ T008 after T006
- T013 ‖ T012 after T011

## MVP scope

T001–T012 sufficient for demoable Rule helper + smoke.

## Implementation strategy

1. Foundational helper + unit tests (US1)
2. Smoke rewrite (US2)
3. README pointer + polish
