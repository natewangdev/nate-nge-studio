# Data Model: Three-Column Main Layout

**Feature**: `005-three-column-layout` | **Date**: 2026-10-01

## AppSettings (extended)

| Field | Type | Rules |
|-------|------|-------|
| version | int | Unchanged |
| hotkeys | dict | Unchanged |
| launch_configs | dict | Unchanged |
| ui | dict \| None | Optional; missing → defaults |

### `ui` object

| Field | Type | Rules |
|-------|------|-------|
| main_splitter_sizes | list[int] length 3 | Each value > 0; invalid/missing → use default ratio 2:3:3 at runtime |

## MainLayout (UI, not persisted as entity)

| Pane | Contents |
|------|----------|
| Left | Brand + catalog |
| Center | Launch params + Start/Pause/Stop + status |
| Right | Live log panel |

Default weights: 2 : 3 : 3.
