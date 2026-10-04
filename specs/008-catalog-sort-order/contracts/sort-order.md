# Contract: Catalog `sort_order`

**Feature**: `008-catalog-sort-order` | **Date**: 2026-10-04

Extends:

- Script manifest: `specs/001-nge-studio-mvp/contracts/manifest-schema.md`
- Game manifest: `specs/004-icon-game-display/contracts/game-manifest-schema.md`

## Field

| Location | Field | Required | Type |
|----------|--------|----------|------|
| `game_scripts/<game_id>/manifest.json` | `sort_order` | no | JSON integer |
| `game_scripts/<game_id>/<script_id>/manifest.json` | `sort_order` | no | JSON integer |

## Rules

- Allowed when present: JSON integer (negative, zero, positive).
- Forbidden when present: boolean, float, string, array, object, `null`.
- Missing key: valid; item is in the **omitted** group for that list.
- Unknown other keys: still fail catalog validation (strict).
- `defaults` remains **forbidden** on game manifests.

## List order (normative)

For games (among discovered games) and for scripts (within one game):

1. Explicit `sort_order` items first, ascending.
2. Then omitted `sort_order`.
3. Ties (same integer, or both omitted): lexicographic folder id.

## UI

- Left-column tree MUST follow discovery order.
- MUST NOT expose reorder controls or persist order in operator settings.

## Error

Invalid `sort_order` → entire catalog validation fails; message includes file path and that `sort_order` must be an integer.
