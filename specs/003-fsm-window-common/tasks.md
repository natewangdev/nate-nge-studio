# Tasks: 003-fsm-window-common

## Phase 1: Foundational

- [x] T001 Add `window_title` to `LaunchParameters` in `src/nge_studio/catalog/models.py`
- [x] T002 Implement `resolve_hwnd_for_launch` in `src/nge_studio/runner/window_resolve.py`
- [x] T003 Require dataclass FSM in `RuleLoop.run` / `RuleContext` in `src/nge_studio/rules/`

## Phase 2: US2 window title

- [x] T004 [US2] Wire resolve + activate in `src/nge_studio/runner/engine_factory.py`
- [x] T005 [US2] Add `window_title` field to `src/nge_studio/ui/widgets/param_form.py`; fill on pick
- [x] T006 [P] [US2] Unit tests in `tests/unit/test_window_resolve.py`

## Phase 3: US1 FSM

- [x] T007 [US1] Update `tests/unit/test_rule_loop.py` for dataclass FSM; reject dict
- [x] T008 [US1] Fix helper until tests pass

## Phase 4: US3 demo commons

- [x] T009 [US3] Put game dir on `sys.path` in `src/nge_studio/runner/loader.py`
- [x] T010 [US3] Add `game_scripts/demo/common.py` and `rules.py`
- [x] T011 [US3] Rewrite `game_scripts/demo/smoke/main.py` for FSM + shared imports
- [x] T012 [US3] Update diablo4 test script FSM if it uses RuleLoop state

## Phase 5: Polish

- [x] T013 Run pytest + validate_catalog + ruff; mark tasks done
