# Quickstart Validation: Three-Column Main Layout

**Feature**: `005-three-column-layout` | **Date**: 2026-10-01

## Automated

```powershell
uv run pytest tests/unit/test_settings_store.py -q
uv run ruff check src/nge_studio/ui/main_window.py src/nge_studio/settings/store.py
```

**Expected**: Settings round-trip includes `ui.main_splitter_sizes`; invalid sizes ignored.

## Manual

```powershell
uv run nge-studio
```

1. Confirm three columns: catalog (no left-rail brand/tagline) | params+controls | **实时日志** heading + panel (not GroupBox); content tops aligned; thin visible splitters (brighter on hover); default ≈ 2:3:3.
2. Drag splitters; quit; reopen — widths restored.
3. Start `demo/smoke` — logs stream on the **right**.

## Refs

- [ui-layout-settings.md](./contracts/ui-layout-settings.md)
- [spec.md](./spec.md)
