# Implementation Plan: Catalog Sort Order

**Branch**: `008-catalog-sort-order` | **Date**: 2026-10-04 | **Spec**: [spec.md](./spec.md)

## Summary

Add optional integer `sort_order` on game-level and script manifests. Discovery lists games and scripts with explicit orders first (ascending), then omitted items; ties and omitted groups use folder-name lexicographic order. Validation stays strict (unknown keys fail; non-integer `sort_order` fails the whole catalog). UI catalog tree consumes discovery order; no operator reorder or settings persistence.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: existing `nge_studio.catalog` (no UI toolkit change)  
**Storage**: authored JSON manifests under `game_scripts/` (packaged catalog); not local settings  
**Testing**: pytest unit tests on validate + discover order  
**Target Platform**: Windows desktop (NGE-STUDIO)  
**Project Type**: desktop-app  
**Performance Goals**: catalog trees remain tiny (tens of games/scripts); sort cost negligible  
**Constraints**: Folder IDs remain identity; no UI reorder; packaged-catalog rebuild rule unchanged  
**Scale/Scope**: `catalog/models.py`, `validate.py`, `discover.py`, unit tests, manifest contracts, optional sample `sort_order` on in-repo scripts  

## Constitution Check

PASS — Desktop Product First (catalog UX); Packaged Script Catalog (order in manifests, rebuild to ship); no NGE2 API change; bilingual plan/research/data-model/contracts/quickstart; catalog logic covered by automated tests.

Post-design: PASS unchanged.

## Project Structure

### Documentation (this feature)

```text
specs/008-catalog-sort-order/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

Also update existing contracts:

```text
specs/001-nge-studio-mvp/contracts/manifest-schema.md
specs/001-nge-studio-mvp/contracts/manifest-schema.zh-CN.md
specs/004-icon-game-display/contracts/game-manifest-schema.md
```

### Source Code

```text
src/nge_studio/catalog/models.py
src/nge_studio/catalog/validate.py
src/nge_studio/catalog/discover.py
tests/unit/test_catalog.py
src/nge_studio/ui/widgets/catalog_panel.py  # consume list order only; no reorder UI
game_scripts/**/manifest.json               # optional content sort_order
```

## Complexity Tracking

N/A
