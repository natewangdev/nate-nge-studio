# Research: Three-Column Main Layout

**Feature**: `005-three-column-layout` | **Date**: 2026-10-01

## R1 — Splitter composition

- **Decision**: One horizontal `QSplitter` with three widgets: left (**catalog only**), center (params + controls + status), right (**`QLabel("实时日志")` + `LogPanel`**, not GroupBox).
- **Rationale**: Matches FR-001/002/009/010; single splitter simplifies persist API (`sizes()` / `setSizes()`).
- **Alternatives**: Nested splitters; fixed layouts without drag — rejected (FR-004 requires resize). Left brand + catalog — superseded (remove left-rail brand). Right log GroupBox — tried then **reverted** (FR-010 restore non-GroupBox).

## R2 — Default 2:3:3

- **Decision**: On first show (or invalid saved sizes), call `setStretchFactor(0,2)`, `(1,3)`, `(2,3)` and/or `setSizes` proportional to window width × `[2,3,3]/8`.
- **Rationale**: Spec custom ratio; stretch factors keep proportion on resize before user drags.
- **Alternatives**: Equal thirds — rejected.

## R3 — Persist sizes

- **Decision**: Store `ui.main_splitter_sizes` as three positive ints (pixel widths from `QSplitter.sizes()`). Save on `splitterMoved` (debounced ~300ms) and on window `closeEvent`. Restore after layout built via `QTimer.singleShot(0, ...)`.
- **Rationale**: Contract allows pixel array; debounce avoids disk spam while dragging.
- **Alternatives**: Stretch-only persistence — harder to restore exactly; window-close-only — loses crash mid-session (still OK but weaker).

## R4 — Validation

- **Decision**: Accept only `list`/`tuple` of exactly 3 ints/floats > 0; else treat as missing → defaults.
- **Rationale**: FR-006.

## R5 — Left brand removal (2026-10-02)

- **Decision**: Remove left-rail `NGE-STUDIO` / tagline labels; catalog only.
- **Rationale**: Clarification Option A for left column.
- **Alternatives**: Catalog GroupBox for symmetry — rejected.

## R6 — Top alignment (2026-10-02)

- **Decision**: Align tops of left catalog, center launch GroupBox outer frame, and right log column content via equalized layout margins/padding (not by wrapping logs in a GroupBox).
- **Rationale**: Clarification Option A.
- **Alternatives**: Uniform title bars across all three columns — rejected (Option B).

## R7 — Splitter handle chrome (2026-10-02)

- **Decision**: Style `QSplitter::handle` as a thin (~1–2px) contrasting vertical line using theme border-adjacent color; brighter on `:hover` / active drag.
- **Rationale**: Clarification Option B; FR-012 / SC-007.
- **Alternatives**: Wide always-on grip (A); hover-only visibility (C) — rejected.

## R8 — Live log chrome revert (2026-10-02)

- **Decision**: Restore right column to heading label + `LogPanel` (no `QGroupBox`).
- **Rationale**: User request to match original log style; FR-010 supersedes earlier GroupBox FR.
- **Alternatives**: Keep log GroupBox for parity with center — rejected.
