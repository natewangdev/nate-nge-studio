# Data Model: NGE-STUDIO MVP Shell

**Feature**: `001-nge-studio-mvp` | **Date**: 2026-09-28

Chinese companion: [`data-model.zh-CN.md`](./data-model.zh-CN.md).

Persistence: JSON settings file only. Catalog entities are filesystem-derived at discover time.

## Entities

### Game

| Field | Type | Rules |
|-------|------|-------|
| game_id | str | Folder name under `game_scripts/`; non-empty; stable ID |
| path | path | Absolute path to game folder |
| scripts | list[Script] | Child script folders that pass validation |

### Script

| Field | Type | Rules |
|-------|------|-------|
| game_id | str | Parent game |
| script_id | str | Folder name under game; non-empty; stable ID |
| path | path | Absolute path to script folder |
| entry_module | path | MUST be `main.py` in script folder |
| manifest | Manifest | Parsed from `manifest.json` |
| display_name | str | `manifest.display_name` or fallback `script_id` |

**Identity**: Unique key `game_id/script_id` within a catalog.

### Manifest

| Field | Type | Rules |
|-------|------|-------|
| display_name | str | Optional; if missing/empty → UI uses `script_id` |
| description | str | Optional |
| defaults | LaunchParameters | Optional partial defaults for form |

See [manifest-schema.md](./contracts/manifest-schema.md).

### LaunchParameters

Author-facing NGE2 construction fields + Studio timeout.

| Field | Type | Rules |
|-------|------|-------|
| resource_dir | str/path | Required at Start (non-empty after resolve) |
| hwnd | int \| null | Optional; null/empty → unbound window |
| capture | `"dxcam"` \| `"mss"` | Default `"dxcam"` |
| humanize | bool | Default `true` |
| control_mode | int | Default `2`; UI may still expose; invalid values fail at engine construct |
| log_dir | str/path \| null | Optional |
| yolo_model | str/path | Default per NGE2 (`models/yolo.onnx`) |
| yolo_names | str/path \| null | Default per NGE2 |
| ocr_kwargs | object \| null | JSON object; invalid JSON fails Start validation |
| run_duration_sec | number \| null | Studio-only; null/omitted/≤0 → no timeout; &gt;0 → stop after seconds |

### LaunchConfiguration (persisted overlay)

| Field | Type | Rules |
|-------|------|-------|
| script_key | str | `game_id/script_id` |
| parameters | LaunchParameters | Last-used values (may be partial) |
| updated_at | datetime | Optional ISO timestamp |

**Merge on select**: manifest `defaults` ← overwritten by last-used fields that are present.

### RunContext

| Field | Type | Rules |
|-------|------|-------|
| paused | bool | Set by Pause; cleared by Resume (Start while paused) |
| stop_requested | bool | Set by Stop or Studio timeout |
| started_at | datetime | Set when run begins |

**Operations** (see [script-protocol.md](./contracts/script-protocol.md)): `is_paused`, `should_stop`, `wait_if_paused`, `checkpoint`.

### RunSession

| Field | Type | Rules |
|-------|------|-------|
| script_key | str | Active script identity |
| state | enum | `idle` \| `running` \| `paused` \| `stopping` |
| engine | NGE2 \| null | Owned while not idle; closed on exit |
| log_lines | list[str] | Cap 5000; retained after idle until next Start |
| hung_warning | bool | True if stop grace (10s) elapsed without join |

**Transitions**:

```text
idle --Start--> running
running --Pause--> paused
paused --Start/F9 (Resume)--> running
running|paused --Stop|timeout--> stopping --join+close--> idle
idle --Start (while not idle)--> refused (stay prior state)
```

At most one non-idle session process-wide.

### HotkeyBinding

| Field | Type | Rules |
|-------|------|-------|
| action | `"start"` \| `"pause"` \| `"stop"` | Exactly one binding each |
| key | str | Canonical key name (e.g. `F9`); defaults F9/F10/F11 |
| modifiers | set | Optional; MVP defaults none |

### AppSettings (file root)

| Field | Type | Rules |
|-------|------|-------|
| hotkeys | list[HotkeyBinding] | Three actions |
| launch_configs | map[script_key → LaunchConfiguration] | Per-script overlays |

See [settings-store.md](./contracts/settings-store.md).

### WindowPickResult

| Field | Type | Rules |
|-------|------|-------|
| hwnd | int | Top-level window handle |
| title | str | Display label |
| pid | int | Owning process; MUST NOT equal Studio PID |

## Validation Rules

- Missing `manifest.json` or `main.py` / missing `run` → catalog validate **fails build**
- Malformed manifest JSON or schema violation → **fails build**
- Start with empty `resource_dir` → refuse Start with UI error
- Invalid `ocr_kwargs` JSON → refuse Start
- Second Start while session not idle → refuse with clear message
- Window pick targeting Studio PID → reject; hwnd unchanged
- Closed/invalid hwnd at engine construct → Start fails; session returns idle; no zombie run

## Non-goals

- Multi-run sessions, remote settings sync, script marketplace metadata
