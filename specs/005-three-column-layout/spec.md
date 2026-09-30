# Feature Specification: Three-Column Main Layout

**Feature Branch**: `005-three-column-layout`

**Created**: 2026-10-01

**Status**: Draft

**Input**: User description: "Adjust the main UI to a left–center–right layout: left = game/script catalog, center = launch parameters, right = live logs; choose appropriate default column width ratios."

**Authority**: Extends shell UI requirements in [`../001-nge-studio-mvp/spec.md`](../001-nge-studio-mvp/spec.md) (FR-001, FR-005 surface, FR-008 controls, FR-013 live logs). Does not change catalog discovery, launch semantics, or runner protocol.

## Clarifications

### Session 2026-10-01

- Q: Where do Start / Pause / Stop (and run status) live after the three-column split? → A: Remain at the **bottom of the center column**, below the launch-parameter form (Option A).
- Q: Default column width ratio? → A: Left : Center : Right ≈ **2 : 3 : 3** (catalog : parameters : live logs).
- Q: Persist splitter sizes across restarts? → A: **Yes** — persist in the existing local settings store (Option B).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Work in a three-column shell (Priority: P1)

An operator opens NGE-STUDIO and sees three side-by-side work areas: game/script catalog on the left, launch parameters (with Start/Pause/Stop and status under the form) in the center, and the live log panel on the right. Default widths follow a 2:3:3 visual ratio. The operator can drag the splitters; after restart, those widths are restored from local settings.

**Why this priority**: Separating monitoring from configuration is the core UX change; without it the feature has no deliverable.

**Independent Test**: Launch the app on a typical desktop resolution; confirm three columns and control placement; resize splitters; restart and confirm sizes restored; start a sample run and confirm logs appear in the right column only.

**Acceptance Scenarios**:

1. **Given** NGE-STUDIO is open at a normal desktop size, **When** the operator views the main window, **Then** they see three horizontal regions: left catalog, center launch parameters, right live logs (not logs stacked under parameters in the same column as today).
2. **Given** the main window is visible, **When** the operator looks at the center column, **Then** Start / Pause / Stop and the run-status label appear below the launch-parameter form in that column (not in a window-wide footer and not above the log panel in the right column).
3. **Given** a first launch with no saved layout (or after layout settings were cleared), **When** the main splitter initializes, **Then** the three columns use a default stretch/width ratio of **2 : 3 : 3** (left : center : right).
4. **Given** the operator drags the column splitters to new widths and then quits the app, **When** they reopen NGE-STUDIO on the same machine/user settings store, **Then** the splitter sizes match the last saved layout (within normal widget rounding).
5. **Given** a script is running and emitting logs, **When** the operator watches the UI, **Then** new live-log lines appear in the **right** column panel, and catalog/parameter interaction in the left/center columns remains available (same FR-013 retention rules as 001).
6. **Given** corrupted or incomplete saved splitter sizes, **When** the app loads settings, **Then** it falls back to the default 2:3:3 ratio without crashing.

---

### Edge Cases

- Very narrow window: columns remain three-way; content MAY scroll inside a column; the layout MUST NOT collapse back to the old two-column stack of params+logs.
- Only one script selected / none selected: layout unchanged; empty states for params/logs follow existing 001 behavior.
- Multi-monitor / DPI scaling: persisted sizes remain usable; if restoring would make a pane unusably small, clamp to a small minimum width then keep three columns.
- Brand / product title: MAY remain above the catalog in the left column (or equivalent chrome); MUST NOT push logs back under parameters.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The main working area MUST use a **three-column** horizontal layout: left = game/script catalog; center = launch parameters; right = live log panel.
- **FR-002**: Start, Pause, Stop, and the run-status indicator MUST appear in the **center** column below the launch-parameter form.
- **FR-003**: Default column width ratio MUST be left : center : right = **2 : 3 : 3** when no persisted layout exists.
- **FR-004**: Column boundaries MUST be user-resizable (splitters) during a session.
- **FR-005**: Resized splitter sizes MUST be persisted in the existing local settings store and restored on subsequent launches for the same machine/user profile.
- **FR-006**: Invalid/missing persisted layout data MUST fall back to the default 2:3:3 ratio without failing app startup.
- **FR-007**: Live-log behavior (near-real-time updates, retain until next Start) MUST remain as in 001 FR-013; only placement moves to the right column.
- **FR-008**: Catalog selection and launch-parameter editing semantics MUST remain as in 001; this feature changes layout, not protocols.

### Key Entities

- **MainLayout**: Three-column shell composition (catalog | parameters+controls | live logs) with default ratio 2:3:3.
- **LayoutSettings**: Persisted splitter sizes (or equivalent stretch factors) in the app settings document.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On first open at ≥1280×720, an observer can identify three distinct columns (catalog / parameters / logs) within 3 seconds without reading documentation.
- **SC-002**: After resizing columns and restarting once, restored widths differ from the last session by at most a small UI rounding tolerance (no reset to factory 2:3:3 unless settings were cleared or invalid).
- **SC-003**: During a sample run that logs ≥1 line/sec, log lines appear in the right column with the same perceived lag expectation as 001 SC-004 (<1s on a typical developer machine).
- **SC-004**: Center-column Start/Pause/Stop remain reachable without scrolling the log panel away (controls are not buried under a tall log stack in the same column).

## Assumptions

- Branding text may stay in the left column above the catalog; exact chrome polish is implementation detail.
- Exact pixel widths are derived from the 2:3:3 ratio and window size; stretch factors or saved pixel sizes are both acceptable if the ratio holds on first layout.
- Settings schema gains an additive layout field; unknown older settings files without that field use defaults (backward compatible).
- Hotkey editing UI location is unchanged unless already elsewhere; this feature does not redesign settings dialogs.
- Mobile / non-Windows layouts remain out of scope.
