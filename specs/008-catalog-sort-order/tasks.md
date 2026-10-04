# Tasks: Catalog Sort Order

**Input**: Design documents from `/specs/008-catalog-sort-order/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/sort-order.md

**Tests**: Included — constitution quality gate for catalog logic (pytest in `tests/unit/test_catalog.py`).

## Phase 1: Setup

**Purpose**: Confirm feature artifacts and existing catalog modules.

- [x] T001 Confirm feature docs under `specs/008-catalog-sort-order/` and existing catalog modules `src/nge_studio/catalog/models.py`, `validate.py`, `discover.py`

---

## Phase 2: Foundational

**Purpose**: Shared parse helper and model field used by discovery and validation.

- [x] T002 Add optional `sort_order: int | None = None` on `Manifest` and `GameManifest` in `src/nge_studio/catalog/models.py` (`sort_order` optional; if present must be JSON integer; zero and negatives allowed)
- [x] T003 Add `sort_order` to `_MANIFEST_TOP` and `_GAME_MANIFEST_TOP`; parse with `isinstance(value, int) and not isinstance(value, bool)` (reject float, bool, string, null, array, object) in `src/nge_studio/catalog/validate.py`; unknown keys still fail

---

## Phase 3: User Story 1 - Maintainer-authored catalog order (P1) 🎯 MVP

**Goal**: Games and scripts in the left-column catalog follow explicit `sort_order` then omitted items then folder-id ties; no operator reorder.

**Independent Test**: `pytest tests/unit/test_catalog.py -q`; open Studio and confirm tree order matches discovery with no drag/up-down controls.

- [x] T004 [US1] Sort games and scripts in `discover_catalog` in `src/nge_studio/catalog/discover.py`: explicit `sort_order` first ascending; omitted after; ties lexicographic `game_id`/`script_id`; script order per game only
- [x] T005 [US1] Confirm `CatalogPanel.set_games` in `src/nge_studio/ui/widgets/catalog_panel.py` inserts in list order and has no reorder controls
- [x] T006 [US1] Unit tests in `tests/unit/test_catalog.py`: mixed explicit/omitted; equal `sort_order` ties by id; missing field OK; float/bool/`null` fail whole validate with path; unknown keys still fail
- [x] T007 [P] [US1] Document `sort_order` on script manifests in `specs/001-nge-studio-mvp/contracts/manifest-schema.md` and `specs/001-nge-studio-mvp/contracts/manifest-schema.zh-CN.md`
- [x] T008 [P] [US1] Document `sort_order` on game manifests in `specs/004-icon-game-display/contracts/game-manifest-schema.md` (add bilingual `game-manifest-schema.zh-CN.md` if missing)
- [x] T009 [P] [US1] Optionally set sample `sort_order` on in-repo `game_scripts/**/manifest.json` so folder-name order and authored order can differ

---

## Phase 4: Polish

**Purpose**: Cross-cutting validation.

- [x] T010 Run `pytest tests/unit/test_catalog.py` and ruff if configured; run [quickstart.md](./quickstart.md) automated check

---

## Dependencies & Execution Order

- Phase 1 → Phase 2 (T002–T003) → Phase 3 US1 (T004–T009; T007–T009 parallel after T006) → Phase 4
- Single story; MVP is US1

## Parallel Example: User Story 1

```text
After T006: T007, T008, T009 in parallel (different contract/content files)
```

## Implementation Strategy

1. Model + validate field
2. Discover sort
3. Tests
4. Contracts + optional sample content
5. pytest
