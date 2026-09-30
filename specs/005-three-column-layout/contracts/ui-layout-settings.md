# Contract: Main Layout & Persisted Splitter Sizes

**Feature**: `005-three-column-layout` | **Date**: 2026-10-01

Extends [`../../001-nge-studio-mvp/contracts/settings-store.md`](../../001-nge-studio-mvp/contracts/settings-store.md).

## UI composition

Horizontal three panes (left → right):

1. Catalog (games / scripts)
2. Launch parameters + Start / Pause / Stop + status
3. Live log panel

Default stretch / width weights: **2 : 3 : 3**.

## Settings addition (conceptual)

Additive object on the existing `settings.json` (field name may be `ui` or `layout`; implement MUST document the chosen key):

```json
{
  "version": 1,
  "hotkeys": { "...": "..." },
  "launch_configs": { "...": "..." },
  "ui": {
    "main_splitter_sizes": [280, 420, 420]
  }
}
```

## Rules

- `main_splitter_sizes`: optional array of three positive integers (pixel widths) **or** three positive stretch weights that preserve 2:3:3 on first layout when absent.
- Missing / wrong length / non-positive values → ignore and use default 2:3:3.
- Persist on splitter move (debounced) or on window close; restore after widgets are built.
- MUST NOT remove or break existing `hotkeys` / `launch_configs` loading.
