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

## Phase 4: Polish (original)

- [x] T007 Run `uv run pytest tests/unit/test_settings_store.py -q` and `uv run ruff check src/nge_studio/ui/main_window.py src/nge_studio/settings/store.py tests/unit/test_settings_store.py`

---

## Phase 5: Amendment 2026-10-02 — Shell chrome (FR-009–FR-012)

**Goal**: Catalog-only left; non-GroupBox right logs; column content tops aligned; visible thin splitter handles.

**Independent Test**: Open app — no left brand; right =「实时日志」heading + panel (not GroupBox); tops align; splitters visible at rest / brighter on hover.

- [x] T008 [US1] Remove left-column brand and tagline labels from `src/nge_studio/ui/main_window.py` (FR-009)
- [x] T009 [US1] Present right column as `QLabel("实时日志")` + `LogPanel` (no log GroupBox) in `src/nge_studio/ui/main_window.py` (FR-010)
- [x] T010 [US1] Equalize left/center/right top margins so primary content tops align in `src/nge_studio/ui/main_window.py` (FR-011)
- [x] T011 [US1] Style `QSplitter::handle` thin contrasting line + hover brighten in `src/nge_studio/ui/styles.py` (FR-012)
- [x] T012 Run unit tests + ruff on touched UI files; mark amendment tasks done

---

## Dependencies

Setup → Foundational (T002–T003) → US1 (T004–T006) → Polish (T007) → Amendment (T008–T012)

## MVP

T001–T006 deliver the original feature; T007 validates; T008–T012 deliver Session 2026-10-02 chrome amendments.
