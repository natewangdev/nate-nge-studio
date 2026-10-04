# Quickstart: Catalog Sort Order

**Feature**: `008-catalog-sort-order`

## Prerequisites

- Repo checkout with `game_scripts/` and pytest environment used by this project.

## Automated check

From repo root:

```text
pytest tests/unit/test_catalog.py -q
```

Expect: validation still hard-fails unknown keys; `sort_order` accepted as integer; floats/bools fail; `discover_catalog` order matches [data-model.md](./data-model.md) (explicit first, omitted after, ties by folder id).

## Manual UI check (optional)

1. Give two games different `sort_order` values that disagree with folder-name order; rebuild/run Studio.
2. Left column game groups follow `sort_order`, not folder-name order.
3. Confirm no drag handles or up/down buttons on the catalog tree.
4. Select a script; launch settings key remains `game_id/script_id`.

## Sample tree for order (conceptual)

- Game `z_game` `sort_order`: 1  
- Game `a_game` omitted  
→ `z_game` appears before `a_game`.

- Under one game: script `b` `sort_order`: 2, script `a` `sort_order`: 2  
→ `a` then `b` (tie by id).
