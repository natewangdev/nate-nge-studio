# Data Model: App Icon & Game Display Name

**Feature**: `004-icon-game-display` | **Date**: 2026-09-30

## Entities

### Game (extended)

| Field | Type | Rules |
|-------|------|-------|
| game_id | str | Folder name under `game_scripts/`; stable ID |
| path | Path | Game folder absolute path |
| scripts | list[Script] | Validated script children |
| manifest | GameManifest \| None | Parsed from optional `manifest.json`; `None` if file absent |

**Resolved display name**: `strip(manifest.display_name)` if non-empty, else `game_id`.

### GameManifest (new)

| Field | Type | Rules |
|-------|------|-------|
| display_name | str \| None | Optional; empty/whitespace → treat as missing for UI |
| description | str \| None | Optional; not required for catalog label |

**Forbidden**: `defaults` and any other top-level keys (strict unknown-key fail).

### Script / Script Manifest

Unchanged from 001. Still at `game_scripts/<game_id>/<script_id>/manifest.json` with optional `defaults`.

### ProductIcon (asset)

| Aspect | Rule |
|--------|------|
| Canonical path | `assets/icons/app.ico` in repository |
| Consumers | Qt runtime window/taskbar; PyInstaller EXE icon; optionally bundled as data for `QIcon` |
| Identity | Single script-themed mark for all required surfaces |

## Validation

| Case | Result |
|------|--------|
| No game `manifest.json` | Pass; display = `game_id` |
| `{}` or missing `display_name` | Pass; display = `game_id` |
| Non-string `display_name` / `description` | Fail with path |
| Unknown keys (incl. `defaults`) | Fail with path |
| Invalid JSON / non-object root | Fail with path |
| Script dirs still missing `main.py` / script manifest | Fail as today |

## Identity & persistence

- Settings and runner keys remain `game_id/script_id`.
- Display names never rewrite folder IDs.
