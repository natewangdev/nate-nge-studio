# Tasks: Three-Column Main Layout

**Input**: Design documents from `/specs/005-three-column-layout/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

## Phase 1: Setup

- [x] T001 Confirm feature branch `005-three-column-layout` and design docs present under `specs/005-three-column-layout/`

---

## Phase 2: Foundational — settings persistence

- [x] T002 Extend `AppSettings` with optional `ui` dict and load/save `ui.main_splitter_sizes` in `src/nge_studio/settings/store.py` (validate three positive numbers; invalid → omit/default)
- [x] T003 [P] Extend `tests/unit/test_settings_store.py` for valid round-trip and invalid/missing splitter sizes fallback

**Checkpoint**: Settings can persist layout sizes

---

## Phase 3: User Story 1 — Three-column shell (P1) 🎯 MVP

**Goal**: Left catalog | center params+controls | right logs; 2:3:3 default; restore/save splitter sizes.

**Independent Test**: Launch app; verify layout; resize; restart; run smoke logs on right.

- [x] T004 [US1] Rebuild `src/nge_studio/ui/main_window.py` central layout as three-pane `QSplitter` (brand+catalog | params+controls+status | logs); default stretch 2:3:3
- [x] T005 [US1] Restore `main_splitter_sizes` from settings after show; save on splitter move (debounce) and `closeEvent` via `SettingsStore`
- [x] T006 [US1] Ensure minimum pane widths so three columns remain usable when window is narrow

**Checkpoint**: US1 independently verifiable

---

## Phase 4: Polish

- [x] T007 Run `uv run pytest tests/unit/test_settings_store.py -q` and `uv run ruff check src/nge_studio/ui/main_window.py src/nge_studio/settings/store.py tests/unit/test_settings_store.py`

---

## Dependencies

Setup → Foundational (T002–T003) → US1 (T004–T006) → Polish

## MVP

T001–T006 deliver the feature; T007 validates.

