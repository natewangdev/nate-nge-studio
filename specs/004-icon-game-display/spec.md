# Feature Specification: App Icon & Game Display Name

**Feature Branch**: `004-icon-game-display`

**Created**: 2026-09-30

**Status**: Draft

**Input**: User description: "Add a script-themed application icon; add display_name support for game directories (aligned with existing script manifest patterns)."

**Authority**: Extends catalog/UI product requirements in [`../001-nge-studio-mvp/spec.md`](../001-nge-studio-mvp/spec.md) (US1, FR-002–FR-004, Game entity). Does not change script entry protocol or run orchestration. Catalog **display order** of games and scripts is specified in [`../008-catalog-sort-order/spec.md`](../008-catalog-sort-order/spec.md).

## Clarifications

### Session 2026-09-30

- Q: Where must the application icon appear? → A: Main window, taskbar, and packaged Windows executable (one script-themed icon set).
- Q: Where is game-level display name stored? → A: Optional `game_scripts/<game_id>/manifest.json` (game metadata only; distinct from script manifests under `<script_id>/`).
- Q: Is game display_name required? → A: Same as scripts — metadata file optional; `display_name` optional; UI falls back to `game_id` when missing/empty.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Recognize Studio by a script-themed icon (Priority: P1)

An operator launches NGE-STUDIO (from development entry or a packaged Windows executable) and immediately recognizes it via a consistent application icon that fits a “script / automation” theme. The same branding appears on the main window, in the taskbar, and on the packaged executable.

**Why this priority**: Without a product icon, Studio is hard to spot among other windows and looks unfinished when shipped.

**Independent Test**: Launch the app and a packaged build; confirm the same icon on the window chrome, taskbar button, and `.exe` file (or shortcut to it).

**Acceptance Scenarios**:

1. **Given** NGE-STUDIO is running, **When** the operator views the main window and its taskbar button, **Then** both show the product’s script-themed icon (not the OS/default generic application icon).
2. **Given** a packaged Windows build of NGE-STUDIO, **When** the operator inspects the shipped executable in Explorer (or launches it), **Then** the executable uses that same script-themed icon.
3. **Given** the operator has several applications open, **When** they scan the taskbar, **Then** NGE-STUDIO is distinguishable by its script-themed icon without reading the window title first.

---

### User Story 2 - Browse games by human-readable display names (Priority: P1)

An operator opens the catalog and sees each game grouped with a readable display name when the maintainer provided one. Script rows continue to use script `manifest.display_name` as today. Maintainers may add an optional game-level `manifest.json` under the game folder; missing game metadata still shows the folder `game_id`.

**Why this priority**: Game folders today are often opaque IDs (`demo`, `diablo4`); mirroring script display names makes the catalog readable without renaming stable IDs.

**Independent Test**: Catalog with (a) a game that has valid game `manifest.json` + `display_name`, (b) a game with no game manifest, (c) a game with empty/missing `display_name`; verify UI labels and that catalog validation still passes for (b)/(c).

**Acceptance Scenarios**:

1. **Given** `game_scripts/<game_id>/manifest.json` exists with a non-empty `display_name`, **When** the operator opens the catalog, **Then** that game’s group label shows `display_name` (not only the raw `game_id`).
2. **Given** a game folder has no `manifest.json`, **When** the operator opens the catalog, **Then** the game group label is `game_id`, and catalog validation does **not** fail solely because the game manifest is absent.
3. **Given** a game `manifest.json` is present but `display_name` is missing or empty/whitespace, **When** the operator opens the catalog, **Then** the game group label falls back to `game_id`.
4. **Given** a game `manifest.json` is present but is not valid JSON or violates the documented game-manifest field rules, **When** packaging/catalog validation runs, **Then** the entire build/validation fails with a clear error that identifies the offending game path.
5. **Given** both a game-level `manifest.json` and script-level `manifest.json` files exist, **When** discovery runs, **Then** game metadata is read only from the game folder’s `manifest.json`, and script metadata continues to come only from each script folder’s `manifest.json`; catalog discovery MUST NOT treat the game-level file as a script entry.

---

### Edge Cases

- Game `manifest.json` contains unknown top-level keys: catalog validation fails (strict), with path + reason (same strictness spirit as script manifests).
- Game `manifest.json` is an empty object `{}`: valid; UI uses `game_id`.
- Game folder contains only `manifest.json` and no scripts: existing empty-game behavior from MVP still applies (no selectable scripts); display name still shown if present.
- Icon asset missing from the build that claims to ship branding: packaging or app startup MUST fail in a way maintainers can detect before shipping a generic-icon build (no silent fallback to default OS icon for packaged/release path once the feature is implemented).
- Script directories under a game remain unaffected: a game without game manifest must not change script discovery or script display names.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST present a single script-/automation-themed product icon for NGE-STUDIO.
- **FR-002**: When the application is running, the main window and its taskbar representation MUST use that product icon.
- **FR-003**: The packaged Windows executable MUST embed/use that same product icon so Explorer and launch surfaces show it.
- **FR-004**: The icon theme MUST communicate “script” / scripted automation (not a generic blank app mark). Exact artwork is an implementation/asset decision so long as the theme is recognizable in the window, taskbar, and exe.
- **FR-005**: Catalog discovery MUST support an optional game-level metadata file at `game_scripts/<game_id>/manifest.json`.
- **FR-006**: Game-level `manifest.json`, when present, MUST allow optional `display_name` (string). Empty or missing `display_name` MUST cause the UI to show `game_id`. Additional optional fields MUST be limited to those documented for game manifests (`display_name`; optional `description` for parity with script manifests; optional `sort_order` per [`../008-catalog-sort-order/spec.md`](../008-catalog-sort-order/spec.md)). Other keys remain forbidden.
- **FR-007**: Absence of game-level `manifest.json` MUST NOT fail catalog validation by itself; the UI MUST show `game_id` for that game.
- **FR-008**: If game-level `manifest.json` exists but is malformed or violates the documented game-manifest rules, packaging/catalog validation MUST fail the entire build with a clear error naming the path (consistent with script manifest failure policy in 001).
- **FR-009**: Catalog UI MUST show each game group using the resolved game display name (`display_name` or fallback `game_id`). Script row labels remain driven by script manifests as in 001.
- **FR-010**: Stable identifiers remain folder names: `game_id` and `script_id` MUST NOT be replaced by display names in settings keys, runner identity, or persistence.
- **FR-011**: Catalog discovery MUST NOT treat game-level `manifest.json`, `common.py`, or `rules.py` as script directories (extends 001 FR-017 file exclusions).

### Key Entities

- **Game**: Folder under `game_scripts` identified by `game_id`; optional game-level `manifest.json`; groups scripts; exposes resolved `display_name` for UI.
- **Game Manifest**: Optional metadata for a game (`display_name`, optional `description`, optional `sort_order` per 008); no launch `defaults` (those remain script-only).
- **Script Manifest**: Unchanged — lives under `game_scripts/<game_id>/<script_id>/manifest.json`.
- **Product Icon**: The branded script-themed visual identity of NGE-STUDIO used for window, taskbar, and packaged executable.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On a typical operator machine, an observer can identify the running NGE-STUDIO window from the taskbar icon alone within 3 seconds without reading the title text.
- **SC-002**: A packaged Windows build’s executable shows the product icon in Explorer before launch (visual check: not the generic application glyph).
- **SC-003**: For a catalog containing at least one game with `display_name` and one without a game manifest, the operator sees the intended labels for both game groups on first open with no extra configuration.
- **SC-004**: Catalog validation reports 100% of invalid game `manifest.json` cases (bad JSON / illegal fields) as build failures with a path that points at the offending game folder.
- **SC-005**: Existing script selection, launch, and settings keys keyed by `game_id/script_id` continue to work unchanged after game display names are introduced (no reconfiguration required for prior settings).

## Assumptions

- Icon artwork is provided/produced as part of implementing this feature and stored in the repository; operators do not upload custom icons.
- “Script theme” means a clear visual cue of scripts/automation suitable for a desktop tool; detailed art direction is left to implementation as long as FR-001–FR-004 are met.
- Game `manifest.json` does not carry launch defaults; launch defaults remain on script manifests only. Optional `sort_order` is specified in feature `008`, not by this feature’s display-name rules.
- Sample games in-repo MAY gain game manifests with Chinese or English display names for readability; that is content, not a new localization system.
- Per-game or per-script icons inside the catalog tree are out of scope.
- Tray/notification-area icons, installer branding, and website favicons are out of scope unless already implied by the Windows exe/window/taskbar surfaces above.
- This feature does not change NGE2 engine APIs or script `run` protocol.
