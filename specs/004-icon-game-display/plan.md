# Implementation Plan: App Icon & Game Display Name

**Branch**: `004-icon-game-display` | **Date**: 2026-09-30 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/004-icon-game-display/spec.md`

## Summary

1. Ship a script-themed product icon and wire it to the Qt main window/taskbar and PyInstaller Windows exe.
2. Support optional `game_scripts/<game_id>/manifest.json` with optional `display_name` (fallback `game_id`); harden catalog validation; show resolved names in the catalog tree without changing `game_id` identity keys.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: PySide6 (QIcon / window icon), existing catalog stack, PyInstaller (`EXE(icon=...)`)

**Storage**: N/A (filesystem catalog + packaged icon asset under repo `assets/`)

**Testing**: pytest (catalog validation / discovery / display_name resolution); manual visual checks for icon (quickstart)

**Target Platform**: Windows desktop (dev + packaged onedir)

**Project Type**: Desktop application (NGE-STUDIO shell)

**Performance Goals**: Catalog load unchanged; icon resolve once at startup

**Constraints**: Stable IDs remain folder names; game manifest must not carry launch `defaults`; bad game manifest hard-fails catalog validation; packaged/release path must not silently ship without the icon asset

**Scale/Scope**: Existing games (`demo`, `diablo4`); one product icon set; optional game manifests

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status |
|------|--------|
| I Desktop Product First | PASS — icon branding + catalog readability are shell UX |
| II NGE2 sole engine | PASS — no engine API changes |
| III Packaged script catalog | PASS — game metadata stays in packaged `game_scripts/` tree; rebuild still required for new content |
| IV Cooperative single runner | PASS — untouched |
| V Observability / hotkeys | PASS — untouched |
| VI Tests & quality | PASS — unit tests for game manifest/discovery; icon covered by packaging path + quickstart visual check |
| VII Spec Kit bilingual | PASS — `spec.md` + `spec.zh-CN.md` present |

**Post-design re-check**: PASS — contracts extend catalog only; no new projects or engine vendoring.

## Project Structure

### Documentation (this feature)

```text
specs/004-icon-game-display/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── game-manifest-schema.md
└── tasks.md
```

### Source Code (repository root)

```text
assets/icons/
  app.ico                 # Windows exe + Qt (multi-size)
  app.png                 # source / Qt fallback if needed
src/nge_studio/
  app.py                  # setApplication/window icon
  resources.py            # resolve icon path (dev + frozen)
  catalog/
    models.py             # Game.display_name; GameManifest
    validate.py           # parse/validate game manifest
    discover.py           # load optional game manifest
  ui/widgets/catalog_panel.py  # show game.display_name
packaging/nge-studio.spec # EXE icon=
game_scripts/demo/manifest.json
game_scripts/diablo4/manifest.json
tests/unit/test_catalog.py  # extend game display_name cases
```

**Structure Decision**: Extend existing single-project Studio layout; add `assets/icons/` for branding; no new packages.

## Complexity Tracking

> No constitution violations requiring justification.
