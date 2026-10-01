# Tasks: 006 Script Control Params

## Phase 1: Setup

- [x] T001 Confirm branch `006-script-control-params` and specs present

## Phase 2: Foundational

- [x] T002 Add `ScriptParamField`, `Manifest.script_params`, `duration_end_action` on `LaunchParameters` in `src/nge_studio/catalog/models.py`
- [x] T003 Parse/validate `script_params` in `src/nge_studio/catalog/validate.py`
- [x] T004 Extend `RunContext` with `script_params` + ensure `request_stop` is the script API in `src/nge_studio/runner/context.py`
- [x] T005 Persist `script_params` beside launch parameters in `src/nge_studio/settings/store.py`

## Phase 3: US1 Self-stop

- [x] T006 [US1] Integration/unit test: worker calls `ctx.request_stop()` and run ends idle without shutdown in `tests/integration/test_runner.py` / `tests/unit/test_run_context.py`

## Phase 4: US2 Script params

- [x] T007 [US2] Dynamic script-params UI section in `src/nge_studio/ui/widgets/param_form.py`
- [x] T008 [US2] Wire select/start/reset + `ctx.script_params` in `src/nge_studio/ui/main_window.py` and `src/nge_studio/runner/service.py`
- [x] T009 [P] [US2] Unit tests for schema parse/merge in `tests/unit/test_script_params.py`

## Phase 5: US3 Duration end action

- [x] T010 [US3] Add shutdown helper + injectable executor in `src/nge_studio/runner/shutdown.py`
- [x] T011 [US3] Timeout path: stop then optional shutdown; UI combo in `param_form.py` / `service.py`
- [x] T012 [US3] Tests: none does not call executor; shutdown calls once after stop in `tests/integration/test_runner.py`

## Phase 6: Polish

- [x] T013 Run pytest + ruff; mark tasks done
