# Contract: Settings Store

**Feature**: `001-nge-studio-mvp` | **Date**: 2026-09-28

Chinese companion: [`settings-store.zh-CN.md`](./settings-store.zh-CN.md).

## Location

```text
%LOCALAPPDATA%/NGE-STUDIO/settings.json
```

Create parent directory on first save. If the file is missing, use built-in defaults (hotkeys F9/F10/F11; empty launch overlays).

## Document shape

```json
{
  "version": 1,
  "hotkeys": {
    "start": { "key": "F9", "modifiers": [] },
    "pause": { "key": "F10", "modifiers": [] },
    "stop": { "key": "F11", "modifiers": [] }
  },
  "launch_configs": {
    "demo/smoke": {
      "updated_at": "2026-09-28T12:00:00",
      "parameters": {
        "resource_dir": ".",
        "hwnd": 123456,
        "window_title": "Diablo",
        "capture": "dxcam",
        "humanize": true,
        "control_mode": 2,
        "log_dir": null,
        "yolo_model": "models/yolo.onnx",
        "yolo_names": "models/yolo.names",
        "ocr_kwargs": null,
        "run_duration_sec": 3600
      }
    }
  }
}
```

## Rules

- `version`: positive int; unknown future version → load best-effort or reset with backup rename (implement MUST not crash the app).
- Hotkey actions MUST remain the three keys `start` / `pause` / `stop`. Duplicate physical keys across actions → refuse save with UI error.
- `launch_configs` keys MUST be `game_id/script_id`.
- Persist last-used parameters on successful field edit debounce and/or on Start (implement may choose; MUST persist across restart per FR-007).
- Corrupt JSON on load → backup file aside, start with defaults, show warning once.

## Non-goals

- Roaming profiles, cloud sync, encryption at rest for MVP
