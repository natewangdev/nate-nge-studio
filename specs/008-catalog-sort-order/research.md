# Research: 008 Catalog Sort Order

**Date**: 2026-10-04

## R1 — Where to sort

- **Decision**: Sort in `discover_catalog` after building each game’s script list and after collecting games. `catalog_panel` keeps inserting items in list order (no extra UI sort).
- **Rationale**: One source of truth for UI, CLI, and tests; matches packaged catalog identity.
- **Alternatives**: Sort only in the tree widget — rejected (CLI/tests would diverge; easier to add accidental reorder UI).

## R2 — Sort key

- **Decision**: Tuple `(0, sort_order, folder_id)` for explicit integers; `(1, 0, folder_id)` when `sort_order` is missing. Python tuple order yields: all explicit (by number then id), then all omitted (by id).
- **Rationale**: Matches FR-005 without sentinel integers colliding with author values.
- **Alternatives**: Treat missing as `0` — rejected (clarification Option A). Use `float('inf')` for missing — works but less explicit than a group flag.

## R3 — Integer type

- **Decision**: Accept only JSON integers: `isinstance(value, int) and not isinstance(value, bool)`. Reject floats (`1.0`), strings, null-as-present, booleans.
- **Rationale**: Spec FR-009; Python `bool` is a subclass of `int`.
- **Alternatives**: Coerce `1.0` to `1` — rejected (strict catalog).

## R4 — Sample content

- **Decision**: In-repo `game_scripts` MAY set `sort_order` so demo games/scripts illustrate order; not required for validation of existing trees (field optional).
- **Rationale**: Content, not a new system.
- **Alternatives**: Leave all samples unordered — acceptable; adding values makes the feature visible in the default tree.

## R5 — Empty games

- **Decision**: Do not change current discovery: games with zero script directories are omitted from the returned catalog (existing behavior). Spec empty-game clause only applies if such a game is shown.
- **Rationale**: Out of this feature’s grouping/identity scope.
- **Alternatives**: Start listing empty games solely to sort them — rejected.
