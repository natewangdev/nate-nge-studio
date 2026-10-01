# Feature Specification: Three-Column Main Layout

**Feature Branch**: `005-three-column-layout`

**Created**: 2026-10-01

**Status**: Draft

**Input**: User description: "Adjust the main UI to a left–center–right layout: left = game/script catalog, center = launch parameters, right = live logs; choose appropriate default column width ratios."

**Authority**: Extends shell UI requirements in [`../001-nge-studio-mvp/spec.md`](../001-nge-studio-mvp/spec.md) (FR-001, FR-005 surface, FR-008 controls, FR-013 live logs). Does not change catalog discovery, launch semantics, or runner protocol. Center-column parameter **GroupBox** chrome is owned by [`../007-param-form-sections/spec.md`](../007-param-form-sections/spec.md); this feature owns left/right column chrome, column top alignment, and main splitter visibility.

## Clarifications

### Session 2026-10-01

- Q: Where do Start / Pause / Stop (and run status) live after the three-column split? → A: Remain at the **bottom of the center column**, below the launch-parameter form (Option A).
- Q: Default column width ratio? → A: Left : Center : Right ≈ **2 : 3 : 3** (catalog : parameters : live logs).
- Q: Persist splitter sizes across restarts? → A: **Yes** — persist in the existing local settings store (Option B).

### Session 2026-10-02

- Q: After removing left-rail brand text, how should the left and right columns present? → A: Left column shows **only** the catalog (no brand title, no subtitle, no extra GroupBox). *(Right-column GroupBox choice from this answer was later superseded — see below.)*
- Q: Where should left-rail brand removal be recorded? → A: Amend this `005` feature specification in place (Option A).
- Q: How should left/center/right **tops** align? → A: Align the **top edges of the three columns’ primary content** (catalog top, launch-parameter GroupBox outer top, log panel top) on one horizontal line; do not force a log GroupBox solely for alignment (Option A).
- Q: How should splitter handles look so they are discoverable? → A: **Thin contrasting vertical line** (slightly lighter than the window background / near border tone) with **brighter hover/drag** state; about 1–2px visible width (Option B).
- Q: Revert live-log chrome and where to record splitter/alignment? → A: Live logs return to the **pre-GroupBox** right-column style (heading label **实时日志** + log panel, **not** a GroupBox); continue amending `005` in place (Option A).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Work in a three-column shell (Priority: P1)

An operator opens NGE-STUDIO and sees three side-by-side work areas: game/script catalog on the left (no product title or tagline above it), launch parameters (with Start/Pause/Stop and status under the form) in the center, and live logs on the right with a simple **实时日志** heading (not a GroupBox). The tops of the three columns’ primary content align. Splitter handles are visible as thin contrasting lines (brighter on hover). Default widths follow a 2:3:3 visual ratio. The operator can drag the splitters; after restart, those widths are restored from local settings.

**Why this priority**: Separating monitoring from configuration is the core UX change; without it the feature has no deliverable.

**Independent Test**: Launch the app; confirm three columns; left has no brand/tagline; right uses非 GroupBox log chrome; content tops align; splitters visible at rest and brighter on hover; resize; restart; run smoke with logs on the right.

**Acceptance Scenarios**:

1. **Given** NGE-STUDIO is open at a normal desktop size, **When** the operator views the main window, **Then** they see three horizontal regions: left catalog, center launch parameters, right live logs (not logs stacked under parameters in the same column as today).
2. **Given** the main window is visible, **When** the operator looks at the center column, **Then** Start / Pause / Stop and the run-status label appear below the launch-parameter form in that column (not in a window-wide footer and not above the log panel in the right column).
3. **Given** a first launch with no saved layout (or after layout settings were cleared), **When** the main splitter initializes, **Then** the three columns use a default stretch/width ratio of **2 : 3 : 3** (left : center : right).
4. **Given** the operator drags the column splitters to new widths and then quits the app, **When** they reopen NGE-STUDIO on the same machine/user settings store, **Then** the splitter sizes match the last saved layout (within normal widget rounding).
5. **Given** a script is running and emitting logs, **When** the operator watches the UI, **Then** new live-log lines appear in the **right** column panel, and catalog/parameter interaction in the left/center columns remains available (same FR-013 retention rules as 001).
6. **Given** corrupted or incomplete saved splitter sizes, **When** the app loads settings, **Then** it falls back to the default 2:3:3 ratio without crashing.
7. **Given** the main window is visible, **When** the operator looks at the left column, **Then** they see the game/script catalog without the in-column product title **NGE-STUDIO** and without the tagline **游戏脚本管理 · 基于 NGE2** (window title bar / icon branding elsewhere MAY remain).
8. **Given** the main window is visible, **When** the operator looks at the right column, **Then** live logs use the non-GroupBox presentation: a **实时日志** heading plus the log panel (not a bordered titled group like center **启动参数**).
9. **Given** the main window is visible at a normal desktop size, **When** the operator compares the three columns, **Then** the top edges of left catalog content, center launch-parameter section (GroupBox outer top), and right log content align on one horizontal line (within normal layout rounding).
10. **Given** the main window is visible, **When** the operator views a column boundary at rest, **Then** they can see a thin contrasting splitter line (not blending into the background); **When** they hover or drag that boundary, **Then** the handle appears brighter / more emphasized.

---

### Edge Cases

- Very narrow window: columns remain three-way; content MAY scroll inside a column; the layout MUST NOT collapse back to the old two-column stack of params+logs.
- Only one script selected / none selected: layout unchanged; empty states for params/logs follow existing 001 behavior.
- Multi-monitor / DPI scaling: persisted sizes remain usable; if restoring would make a pane unusably small, clamp to a small minimum width then keep three columns.
- Left column: catalog fills the pane; MUST NOT reintroduce left-rail brand/tagline chrome. Product identity MAY remain via window title, taskbar icon (004), etc.
- Top alignment: center may still use GroupBox titles (007); right MUST NOT reintroduce a log GroupBox solely to match center chrome — adjust margins/padding instead.
- Splitter: MUST remain discoverable at rest; MUST NOT rely on hover-only visibility (rejected Option C).

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
- **FR-009**: The left column MUST present the catalog **without** in-column product title text **NGE-STUDIO** and **without** the subtitle **游戏脚本管理 · 基于 NGE2** (or equivalent left-rail brand chrome). It MUST NOT wrap the catalog in an extra section GroupBox solely for branding parity.
- **FR-010**: The right column MUST present live logs in the **non-GroupBox** style: a **实时日志** heading label plus the log panel (the presentation used before the brief GroupBox experiment). It MUST NOT wrap the log panel in a bordered titled GroupBox like center **启动参数** / **脚本参数**.
- **FR-011**: At a normal desktop window size, the top edges of the left catalog content, the center launch-parameter section’s outer top, and the right log content MUST align horizontally (within normal layout rounding).
- **FR-012**: Main column splitter handles MUST be visually distinguishable from the window background at rest (thin contrasting vertical line, ~1–2px), and MUST become brighter / more emphasized on hover and while dragging.

### Key Entities

- **MainLayout**: Three-column shell composition (catalog | parameters+controls | live logs) with default ratio 2:3:3.
- **LayoutSettings**: Persisted splitter sizes (or equivalent stretch factors) in the app settings document.
- **LiveLogColumn**: Right-column UI: **实时日志** heading + log panel (not a GroupBox).
- **MainSplitterHandle**: Visible thin contrasting splitter grip between columns.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On first open at ≥1280×720, an observer can identify three distinct columns (catalog / parameters / logs) within 3 seconds without reading documentation.
- **SC-002**: After resizing columns and restarting once, restored widths differ from the last session by at most a small UI rounding tolerance (no reset to factory 2:3:3 unless settings were cleared or invalid).
- **SC-003**: During a sample run that logs ≥1 line/sec, log lines appear in the right column with the same perceived lag expectation as 001 SC-004 (<1s on a typical developer machine).
- **SC-004**: Center-column Start/Pause/Stop remain reachable without scrolling the log panel away (controls are not buried under a tall log stack in the same column).
- **SC-005**: On open, the left column shows no in-column **NGE-STUDIO** / tagline brand block; the right column is not a log GroupBox.
- **SC-006**: At ≥1280×720, an observer can see that the three columns’ content tops share one horizontal line within a few pixels.
- **SC-007**: At rest, an observer can locate both column splitters within 3 seconds without hovering; on hover the handle contrast increases.

## Assumptions

- Window title bar text (e.g. `NGE-STUDIO`) and product icon (004) remain; only left-rail brand labels are removed.
- Exact pixel widths are derived from the 2:3:3 ratio and window size; stretch factors or saved pixel sizes are both acceptable if the ratio holds on first layout.
- Settings schema gains an additive layout field; unknown older settings files without that field use defaults (backward compatible).
- Hotkey editing UI location is unchanged unless already elsewhere; this feature does not redesign settings dialogs.
- Mobile / non-Windows layouts remain out of scope.
- Center-column **启动参数** / **脚本参数** GroupBoxes remain specified by 007; this amendment does not relocate Start/Pause/Stop.
- Exact splitter hex colors are implementation detail as long as FR-012 / SC-007 hold against the current dark theme.
