# Tasks: App Icon & Game Display Name

**Input**: Design documents from `/specs/004-icon-game-display/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Extend unit catalog tests for game manifests (plan/quickstart). Icon primarily validated via packaging path + manual quickstart.

**Organization**: US1 = product icon; US2 = game display_name (both P1; US1 first as MVP branding).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1 / US2
- Include exact file paths in descriptions

## Phase 1: Setup

**Purpose**: Asset location and feature branch scaffolding

- [x] T001 Create `assets/icons/` directory for product icon assets per plan.md

---

## Phase 2: Foundational

**Purpose**: Shared icon path helper used by app and packaging consumers

- [x] T002 Add icon path resolver in `src/nge_studio/resources.py` (dev repo path + frozen `_MEIPASS`/beside-exe; hard-fail if missing when required)

**Checkpoint**: Foundation ready — US1/US2 can proceed

---

## Phase 3: User Story 1 — Script-themed product icon (P1) 🎯 MVP

**Goal**: Window, taskbar, and packaged exe share one script-themed product icon.

**Independent Test**: Launch `uv run nge-studio` and inspect window/taskbar; build with PyInstaller and inspect `dist/NGE-STUDIO/NGE-STUDIO.exe`.

### Implementation for User Story 1

- [x] T003 [US1] Create script-themed `assets/icons/app.png` and multi-size `assets/icons/app.ico`
- [x] T004 [US1] Apply product icon on `QApplication` / main window in `src/nge_studio/app.py` via `resources.py`
- [x] T005 [US1] Wire `icon=` and bundle `assets/icons/app.ico` in `packaging/nge-studio.spec` (fail build if ico missing)

**Checkpoint**: US1 independently verifiable (dev + packaged icon)

---

## Phase 4: User Story 2 — Game display_name (P1)

**Goal**: Optional game `manifest.json` with optional `display_name`; catalog UI shows resolved names; bad files hard-fail validation.

**Independent Test**: `uv run pytest tests/unit/test_catalog.py -q` and `uv run python scripts/validate_catalog.py`; open catalog UI labels.

### Implementation for User Story 2

- [x] T006 [US2] Add `GameManifest` and `Game.display_name` (fallback `game_id`; empty/whitespace → `game_id`) in `src/nge_studio/catalog/models.py`
- [x] T007 [US2] Parse/validate optional game manifest (allowed keys only `display_name`, `description`; forbid `defaults`/unknown; absent file OK) in `src/nge_studio/catalog/validate.py` and call from `validate_catalog_tree`
- [x] T008 [US2] Load optional game manifest into `Game` in `src/nge_studio/catalog/discover.py`
- [x] T009 [US2] Show `game.display_name` for game group rows in `src/nge_studio/ui/widgets/catalog_panel.py`
- [x] T010 [P] [US2] Add sample `game_scripts/demo/manifest.json` and `game_scripts/diablo4/manifest.json` with readable `display_name`
- [x] T011 [US2] Extend `tests/unit/test_catalog.py` for absent/empty/valid/invalid game manifests and discovery display names

**Checkpoint**: US2 independently verifiable via tests + UI

---

## Phase 5: Polish & Cross-Cutting

- [x] T012 [P] Mention icon asset and game-level manifest in `README.md` if catalog/packaging docs exist there
- [x] T013 Run `uv run pytest tests/unit/test_catalog.py -q`, `uv run python scripts/validate_catalog.py`, and `uv run ruff check src tests` per quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup → Foundational → US1 and/or US2 → Polish
- US1 and US2 are independent after T002 (different files except polish)

### User Story Dependencies

- **US1**: After T002
- **US2**: After T002 (no dependency on US1)

### Parallel Opportunities

- After T002: US1 (T003–T005) and US2 (T006–T011) can proceed in parallel by different owners
- T010 can run parallel with T006–T009 once paths agreed

### Parallel Example

```text
# After T002:
T003 icon assets | T006 GameManifest model
T004 app.py icon | T007 validate game manifest
T005 pyinstaller | T008–T009 discover + UI
```

---

## Implementation Strategy

### MVP First

1. T001–T002
2. US1 (T003–T005) — branded shell
3. Validate icon surfaces
4. US2 (T006–T011) — catalog names
5. Polish T012–T013

### Notes

- Do not change settings keys away from `game_id/script_id`
- Script manifests and `defaults` remain script-only
