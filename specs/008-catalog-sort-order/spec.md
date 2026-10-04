# Feature Specification: Catalog Sort Order

**Feature Branch**: `008-catalog-sort-order`

**Created**: 2026-10-04

**Status**: Draft

**Input**: User description: "Add sort order for games and scripts."

**Authority**: Extends catalog browsing in [`../001-nge-studio-mvp/spec.md`](../001-nge-studio-mvp/spec.md) (US1 grouping) and game/script metadata in [`../004-icon-game-display/spec.md`](../004-icon-game-display/spec.md). Left-column catalog placement remains [`../005-three-column-layout/spec.md`](../005-three-column-layout/spec.md). Does not change stable folder IDs, launch parameters, selection persistence keys, or run orchestration.

## Clarifications

### Session 2026-10-04

- Q: Who decides catalog order, and where is it stored? → A: Maintainers declare order in game and script metadata; every operator sees the same packaged order; the UI MUST NOT let the operator reorder items.
- Q: What if order is omitted or two items share the same order? → A: The field is optional. Items **without** an explicit order appear **after** all items that have one. Equal explicit orders then sort by folder name (`game_id` / `script_id`).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Maintain a stable authored catalog order (Priority: P1)

A maintainer assigns an explicit order to games and to scripts so that frequently used titles appear first in the left-column catalog. After rebuild/repackage, every operator sees that same order. Games remain grouped; scripts stay selectable independently. Operators do not drag, sort, or otherwise change order in the UI.

**Why this priority**: Folder-name order is not the author’s intended product order; authored order is the whole feature.

**Independent Test**: Prepare a catalog with mixed explicit orders, omitted orders, and a tie; open the catalog; confirm game group order and script order within each game match the rules below; confirm selecting a script still uses `game_id`/`script_id`.

**Acceptance Scenarios**:

1. **Given** two or more games with different explicit orders, **When** the operator opens the catalog, **Then** game groups appear in ascending explicit order (smaller number first).
2. **Given** two or more scripts under the same game with different explicit orders, **When** the operator expands/views that game, **Then** those scripts appear in ascending explicit order (smaller number first).
3. **Given** some games (or some scripts in one game) have an explicit order and others omit it, **When** the operator views the catalog, **Then** all explicitly ordered items of that list appear first (by their numbers), then all omitted items.
4. **Given** two games (or two scripts in the same game) share the same explicit order, **When** the operator views that list, **Then** those tied items appear in lexicographic order of `game_id` or `script_id`.
5. **Given** every game and script omits order, **When** the operator opens the catalog, **Then** games and scripts appear in lexicographic folder-name order (same as “all omitted”).
6. **Given** the catalog is visible, **When** the operator looks for a way to reorder games or scripts, **Then** there is no catalog reorder control (no drag-and-drop, up/down, or local sort preference).
7. **Given** a maintainer changes order metadata in source, **When** an operator runs a build packaged **before** that change, **Then** that older build still shows the previously packaged order until rebuild/repackage.

---

### Edge Cases

- A game has no game-level metadata file: that game is treated as **omitted order** among games.
- A game metadata file exists but omits order: treated as omitted order; display name rules from 004 still apply.
- Equal order plus equal folder names cannot occur (folder names are unique at each level).
- Invalid order value (not an integer, or otherwise violating the documented field rules): catalog validation fails the **entire** build, with path + reason (same policy as other strict manifest fields).
- Unknown metadata keys remain forbidden (001/004 strictness); only documented fields including this order field are allowed.
- Empty game (no scripts): if shown, it still participates in **game** order among other games.
- Script order is **per game**; a script’s number is not compared across games.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The left-column catalog MUST list **games** in the authored order defined by this feature (not an operator-chosen order).
- **FR-002**: Within each game, the catalog MUST list **scripts** in the authored order defined by this feature.
- **FR-003**: Maintainers MUST declare order in existing metadata files: optional integer field `sort_order` on the game-level manifest (when that file exists) and on each script manifest.
- **FR-004**: `sort_order` MUST be optional. Absence MUST NOT fail catalog validation by itself.
- **FR-005**: When comparing items in the same list (all games, or all scripts of one game): every item with an explicit `sort_order` MUST appear before every item without one; among explicit values, smaller numbers MUST appear first; among items that share the same explicit value, and among all omitted items, order MUST be lexicographic by `game_id` or `script_id`.
- **FR-006**: The operator-facing catalog MUST NOT provide any control that changes this order. Order MUST NOT be stored in the operator’s local settings.
- **FR-007**: `game_id` and `script_id` MUST remain the stable identifiers for selection, settings keys, and runs. `sort_order` MUST NOT replace them.
- **FR-008**: Changing `sort_order` in source MUST require rebuild/repackage before a packaged build’s catalog order changes (same packaged-catalog rule as 001 FR-016).
- **FR-009**: If `sort_order` is present but is not an integer (including non-numeric types and non-integer numbers), packaging/catalog validation MUST fail the entire build with a clear error naming the offending path.
- **FR-010**: Catalog grouping, display names, and script selectability MUST remain as in 001/004; this feature only constrains **relative order** of already-discovered items.

### Key Entities

- **Game**: Unchanged identity (`game_id`); optional `sort_order` on the game-level manifest when that file exists.
- **Script**: Unchanged identity (`script_id`); optional `sort_order` on the script manifest.
- **Catalog list**: The ordered sequence of game groups, and the ordered sequence of scripts under each game, shown in the left column.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On first open of a catalog that mixes explicit `sort_order`, omitted `sort_order`, and at least one tie, an observer can confirm the on-screen game and script sequences match FR-005 without extra configuration.
- **SC-002**: 100% of invalid `sort_order` values (wrong type / non-integer) fail catalog validation with a path pointing at the offending game or script metadata file.
- **SC-003**: After a `sort_order` change in source, 100% of builds packaged before that change keep the old on-screen order; 100% of rebuilds show the new order.
- **SC-004**: Operators can still select and launch a script using existing `game_id/script_id` identity with no reconfiguration of saved launch settings after this feature.

## Assumptions

- Field name `sort_order` is the author-facing metadata key (same class of contract as `display_name`).
- Integers may be zero or negative; ordering is numeric ascending.
- Lexicographic folder-name order uses the same comparison the catalog already uses for folder names (stable, case-sensitive folder names as on disk).
- Sample in-repo games/scripts MAY receive `sort_order` values as content; that is not a new localization system.
- This feature does not sort logs, parameter fields, or any list other than catalog games and scripts.
- Script-helper rule **priority** (002) is unrelated and MUST NOT be reused as catalog order.
