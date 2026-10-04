# Data Model: Catalog Sort Order

**Feature**: `008-catalog-sort-order` | **Date**: 2026-10-04

## Entities

### GameManifest (extended)

| Field | Type | Required | Rules |
|-------|------|----------|--------|
| `display_name` | string or omit | no | Unchanged (004) |
| `description` | string or omit | no | Unchanged (004) |
| `sort_order` | integer or omit | no | If present: JSON integer, not bool, not float. Zero and negatives allowed. |

Missing game manifest file ⇒ game has `sort_order = None` (omitted group).

### Manifest (script, extended)

| Field | Type | Required | Rules |
|-------|------|----------|--------|
| existing fields | — | — | Unchanged (001/006) |
| `sort_order` | integer or omit | no | Same integer rules as game |

### Game / Script (runtime)

| Attribute | Notes |
|-----------|--------|
| `game_id` / `script_id` | Folder names; identity unchanged |
| `manifest.sort_order` | `int \| None` after parse |
| `scripts` list | Sorted per FR-005 within the game |
| catalog `list[Game]` | Sorted per FR-005 among games |

## Sort comparison (same list)

1. Items with `sort_order is not None` before items with `None`.
2. Among non-`None`, ascending numeric `sort_order`.
3. Equal `sort_order`, or all `None`: lexicographic `game_id` or `script_id` (Python default `str` order on folder names).

## Validation

- Unknown top-level keys still fail.
- Present + not integer → `CatalogValidationError` (path + reason), entire catalog validate fails.
- Absent → OK.

## Relationships

- Script `sort_order` is compared only among scripts of the same game.
- Game `sort_order` is compared only among games returned by discovery.
