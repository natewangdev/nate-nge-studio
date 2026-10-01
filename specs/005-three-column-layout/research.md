# Research: Three-Column Main Layout

**Feature**: `005-three-column-layout` | **Date**: 2026-10-01

## R1 — Splitter composition

- **Decision**: One horizontal `QSplitter` with three widgets: left (brand + catalog), center (params + controls + status), right (log label + `LogPanel`).
- **Rationale**: Matches FR-001/002; single splitter simplifies persist API (`sizes()` / `setSizes()`).
- **Alternatives**: Nested splitters; fixed layouts without drag — rejected (FR-004 requires resize).

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
