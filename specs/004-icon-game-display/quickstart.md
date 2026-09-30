# Quickstart Validation: App Icon & Game Display Name

**Feature**: `004-icon-game-display` | **Date**: 2026-09-30

## Prerequisites

- Repo checkout with `uv` env installed (`uv sync`).
- Windows machine for icon visual checks.

## 1. Catalog / game display names

```powershell
uv run pytest tests/unit/test_catalog.py -q
uv run python scripts/validate_catalog.py
uv run nge-studio
```

**Expected**:

- Tests covering optional/missing/invalid game manifests pass; invalid cases raise with game path.
- Catalog validation succeeds for in-repo trees with sample game manifests.
- UI game group labels show game `display_name` where provided (e.g. demo / diablo4), else `game_id`.
- Selecting scripts and starting a run still uses `game_id/script_id` identity (prior settings still apply).

## 2. Application icon (dev)

```powershell
uv run nge-studio
```

**Expected**: Main window and taskbar show the script-themed product icon (not the default generic app glyph).

## 3. Packaged exe icon

```powershell
uv run pyinstaller --noconfirm packaging/nge-studio.spec
```

**Expected**:

- Build fails clearly if `assets/icons/app.ico` is missing.
- `dist/NGE-STUDIO/NGE-STUDIO.exe` shows the product icon in Explorer.
- Launching the exe shows the same icon on window/taskbar.

## Contracts / model refs

- [game-manifest-schema.md](./contracts/game-manifest-schema.md)
- [data-model.md](./data-model.md)
