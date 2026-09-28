# Tasks: NGE-STUDIO MVP Shell

**Input**: Design documents from `/specs/001-nge-studio-mvp/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Included — plan Definition of Done requires automated tests for catalog, runner, and settings (fake engine; no HID in CI).

**Organization**: Tasks grouped by user story for independent implementation and testing.

Chinese companion (human-readable only): [`tasks.zh-CN.md`](./tasks.zh-CN.md).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete work)
- **[Story]**: User story label (`[US1]`…`[US5]`)
- Descriptions include exact file paths

## Path Conventions

- App: `src/nge_studio/`, scripts: `game_scripts/`, tests: `tests/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize Python desktop project layout and tooling

- [x] T001 Create package directories per plan under `src/nge_studio/` (`catalog/`, `runner/`, `settings/`, `hotkeys/`, `window_pick/`, `logging_bridge/`, `ui/widgets/`) with `__init__.py` placeholders
- [x] T002 [P] Create `tests/unit/`, `tests/contract/`, `tests/integration/` with `__init__.py` files
- [x] T003 Create `pyproject.toml` for distribution `nate-nge-studio`, import package `nge_studio`, Python `>=3.11`, deps `PySide6` + `nate-game-engine`, dev deps `pytest`/`pytest-qt`/`ruff`/`pyinstaller`, entry points `nge-studio` and `nge-studio-validate`
- [x] T004 [P] Add Python `.gitignore` (`.venv/`, `__pycache__/`, `dist/`, `build/`, `*.egg-info/`, `.pytest_cache/`, etc.) at repository root
- [x] T005 [P] Write operator/dev `README.md` (Chinese primary) covering run, validate, package paths without claiming unfinished APIs

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared models, settings, run context, logging bridge, app bootstrap — MUST complete before user stories

**⚠️ CRITICAL**: No user story work begins until this phase is complete

- [x] T006 Implement `LaunchParameters`, `Manifest`, `Script`, `Game` dataclasses and merge rules in `src/nge_studio/catalog/models.py` per `data-model.md` (constraints: `game_id`/`script_id` non-empty folder names; `hwnd` int|null; `capture` only `dxcam`|`mss`; `run_duration_sec` null or &gt;0)
- [x] T007 [P] Implement `ScriptStopped` and `RunContext` (`is_paused`, `should_stop`, `wait_if_paused`, `checkpoint`) in `src/nge_studio/runner/context.py` per `contracts/script-protocol.md`
- [x] T008 [P] Implement JSON settings load/save for `%LOCALAPPDATA%/NGE-STUDIO/settings.json` in `src/nge_studio/settings/store.py` per `contracts/settings-store.md` (version 1; defaults F9/F10/F11; corrupt → backup + defaults)
- [x] T009 [P] Implement Qt log handler bridging logger `nge` (cap 5000 lines API) in `src/nge_studio/logging_bridge/qt_handler.py`
- [x] T010 Implement injectable engine factory seam and `ScriptRunner` skeleton (idle state, single-flight lock) in `src/nge_studio/runner/service.py` and `src/nge_studio/runner/loader.py`
- [x] T011 Implement `src/nge_studio/__init__.py` (`__version__`), `src/nge_studio/__main__.py`, and `src/nge_studio/app.py` QApplication bootstrap stub that can show an empty main window shell
- [x] T012 [P] Add unit tests for `RunContext` pause/stop/checkpoint in `tests/unit/test_run_context.py`
- [x] T013 [P] Add unit tests for settings round-trip and corrupt recovery in `tests/unit/test_settings_store.py`

**Checkpoint**: Foundation ready — story implementation can begin

---

## Phase 3: User Story 1 — Browse packaged games and scripts (Priority: P1) 🎯 MVP

**Goal**: Discover `game_scripts/<game_id>/<script_id>/` with required `manifest.json` + `main.py`/`run`; validate hard-fails; UI catalog grouped by game

**Independent Test**: Sample tree appears in UI; broken script makes `validate_catalog` exit non-zero with path

### Tests for User Story 1

- [x] T014 [P] [US1] Add catalog discover/validate unit tests (valid tree + missing manifest fails hard) in `tests/unit/test_catalog.py`

### Implementation for User Story 1

- [x] T015 [US1] Implement manifest parse/validate (strict unknown keys fail) in `src/nge_studio/catalog/validate.py` per `contracts/manifest-schema.md`
- [x] T016 [US1] Implement tree discover in `src/nge_studio/catalog/discover.py` (two-level walk; resolve catalog root for dev vs frozen)
- [x] T017 [US1] Implement CLI `scripts/validate_catalog.py` (and console script) that exits non-zero on any invalid script with path+reason
- [x] T018 [US1] Add sample `game_scripts/demo/smoke/manifest.json` and placeholder `main.py` (minimal compliant `run`)
- [x] T019 [US1] Implement catalog panel (group by game, show display_name fallback to script_id) in `src/nge_studio/ui/main_window.py` / `src/nge_studio/ui/widgets/catalog_panel.py`
- [x] T020 [US1] Wire catalog load on startup in `src/nge_studio/app.py` and modern tech QSS baseline in `src/nge_studio/ui/styles.py` (Simplified Chinese labels)

**Checkpoint**: US1 independently testable (validate CLI + catalog UI)

---

## Phase 4: User Story 2 — Configure launch parameters and pick window (Priority: P1)

**Goal**: Full NGE2 param form + Studio timeout; manifest defaults + last-used persistence; window point-and-pick rejecting Studio hwnd

**Independent Test**: Edit params, pick non-Studio window, restart app restores last-used; picking Studio rejected

### Tests for User Story 2

- [x] T021 [P] [US2] Add unit tests for launch param merge (manifest defaults ← last-used) in `tests/unit/test_launch_merge.py`
- [x] T022 [P] [US2] Add unit tests for window-pick self-PID rejection helper in `tests/unit/test_window_pick.py`

### Implementation for User Story 2

- [x] T023 [US2] Implement launch parameter form widget (all author-facing fields + `run_duration_sec` + JSON `ocr_kwargs`) in `src/nge_studio/ui/widgets/param_form.py`
- [x] T024 [US2] Implement Win32 point-and-pick picker rejecting Studio PID in `src/nge_studio/window_pick/picker.py`
- [x] T025 [US2] Wire form load/save with settings store on script select / edit / reset-defaults in `src/nge_studio/ui/main_window.py`
- [x] T026 [US2] Validate `resource_dir` non-empty and `ocr_kwargs` JSON object-or-null before Start in `src/nge_studio/ui/main_window.py` (or runner precheck)

**Checkpoint**: US2 independently testable with UI + unit tests

---

## Phase 5: User Story 3 — Start, pause, and stop a script (Priority: P1)

**Goal**: Single-flight runner with cooperative pause (Start/F9=Resume), stop+engine close, Studio timeout, global hotkeys

**Independent Test**: Fake-engine script respects pause/stop; second Start refused; hotkeys persist; timeout stops like Stop

### Tests for User Story 3

- [x] T027 [P] [US3] Add runner integration tests with fake engine (single-flight, pause/resume, stop closes engine, timeout) in `tests/integration/test_runner.py`

### Implementation for User Story 3

- [x] T028 [US3] Complete script loader importing `main.run` from script dir in `src/nge_studio/runner/loader.py`
- [x] T029 [US3] Complete `ScriptRunner` on QThread: construct engine via factory, call `run`, `finally` close; states idle/running/paused/stopping; 10s hung warning in `src/nge_studio/runner/service.py`
- [x] T030 [US3] Implement real NGE2 engine factory from `LaunchParameters` in `src/nge_studio/runner/engine_factory.py` (hwnd optional)
- [x] T031 [US3] Implement Win32 `RegisterHotKey` bridge emitting Qt signals in `src/nge_studio/hotkeys/win32.py`; wire defaults and settings edits
- [x] T032 [US3] Wire Start/Pause/Stop controls (paused: Start label=恢复) and hotkeys in `src/nge_studio/ui/main_window.py`; refuse second Start with Chinese message
- [x] T033 [US3] Implement Studio `run_duration_sec` timer using same stop path in `src/nge_studio/runner/service.py`
- [x] T034 [US3] Flesh out `game_scripts/demo/smoke/main.py` to honor pause/stop and emit periodic logs

**Checkpoint**: US3 independently testable with fake engine + manual UI

---

## Phase 6: User Story 4 — Watch live logs (Priority: P2)

**Goal**: Near-real-time log panel; retain after stop until next Start; trim at 5000 lines

**Independent Test**: Running script logs appear without refresh; after stop lines remain; next Start clears/replaces

### Implementation for User Story 4

- [x] T035 [US4] Implement log panel widget with append/trim/clear in `src/nge_studio/ui/widgets/log_panel.py`
- [x] T036 [US4] Attach Qt log handler on run start and detach/retain policy on stop/next start in `src/nge_studio/ui/main_window.py`
- [x] T037 [P] [US4] Add unit test for log buffer cap 5000 in `tests/unit/test_log_buffer.py`

**Checkpoint**: US4 independently testable

---

## Phase 7: User Story 5 — Ship Windows executable (Priority: P2)

**Goal**: PyInstaller onedir recipe embedding `game_scripts/`; validate as package pre-step

**Independent Test**: Documented build produces exe that shows packaged catalog

### Implementation for User Story 5

- [x] T038 [US5] Add `packaging/nge-studio.spec` (or equivalent) bundling `nge_studio` + `game_scripts/` as onedir
- [x] T039 [US5] Document validate-then-pyinstaller commands in `README.md` and ensure frozen catalog root resolution works in `src/nge_studio/catalog/discover.py`
- [x] T040 [US5] Add optional CI-friendly note/script hook that fails package when validate fails (document in `README.md`)

**Checkpoint**: US5 packaging path documented and reproducible

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Harden, document, and validate quickstart

- [x] T041 [P] Expand README with hotkey defaults, settings path, script author protocol summary
- [x] T042 Run `uv run pytest` and `uv run ruff check src tests`; fix failures
- [x] T043 Run `uv run python scripts/validate_catalog.py` and smoke `python -m nge_studio` per `quickstart.md`
- [x] T044 [P] Keep `tasks.zh-CN.md` information-equivalent with this file after task checkbox updates during implement

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Start immediately
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all stories
- **US1 → US2 → US3**: Sequential recommended (UI shell grows); US2/US3 need catalog selection from US1
- **US4**: Depends on US3 runner signals (can partially parallelize log widget)
- **US5**: Depends on catalog root resolution (US1) + app entry
- **Polish**: After desired stories complete

### User Story Dependencies

- **US1**: After Foundational
- **US2**: After US1 catalog selection UI
- **US3**: After US2 params (Start needs form values); uses Foundational runner skeleton
- **US4**: After US3 run lifecycle
- **US5**: After US1 catalog + app entry; independent of live run if dry UI works

### Parallel Opportunities

- T002/T004/T005 after T001 structure
- T007/T008/T009 in Foundational
- T014 before/with T015–T017
- T021/T022 with US2 implementation start
- T037 with US4 UI

---

## Parallel Example: User Story 1

```bash
Task: "Add catalog discover/validate unit tests in tests/unit/test_catalog.py"
Task: "Implement manifest parse/validate in src/nge_studio/catalog/validate.py"
Task: "Implement tree discover in src/nge_studio/catalog/discover.py"
```

---

## Implementation Strategy

### MVP First (US1 + Foundational)

1. Phase 1 Setup
2. Phase 2 Foundational
3. Phase 3 US1 (catalog + validate)
4. Validate independently

### Incremental Delivery

1. US2 params + window pick
2. US3 runner + hotkeys
3. US4 live logs
4. US5 packaging
5. Polish / quickstart

---

## Notes

- Prefer fake engine factory in tests; do not require HID for CI
- Mark tasks `[X]` in both EN and zh-CN task files during `/speckit-implement`
- Operator UI strings: Simplified Chinese
