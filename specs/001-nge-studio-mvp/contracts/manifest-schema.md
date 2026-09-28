# Contract: Manifest Schema

**Feature**: `001-nge-studio-mvp` | **Date**: 2026-09-28

Chinese companion: [`manifest-schema.zh-CN.md`](./manifest-schema.zh-CN.md).

File: `game_scripts/<game_id>/<script_id>/manifest.json` (UTF-8 JSON object).

## Schema (conceptual)

```json
{
  "display_name": "string (optional)",
  "description": "string (optional)",
  "defaults": {
    "resource_dir": "string (optional)",
    "hwnd": null,
    "capture": "dxcam",
    "humanize": true,
    "control_mode": 2,
    "log_dir": null,
    "yolo_model": "models/yolo.onnx",
    "yolo_names": "models/yolo.names",
    "ocr_kwargs": null,
    "run_duration_sec": null
  }
}
```

## Field rules

| Field | Required | Notes |
|-------|----------|-------|
| `display_name` | no | Empty/missing → UI shows `script_id` |
| `description` | no | Free text |
| `defaults` | no | Object; unknown keys → validate **fail** (strict) |
| `defaults.capture` | no | Only `"dxcam"` or `"mss"` if present |
| `defaults.hwnd` | no | `null` or non-negative int |
| `defaults.ocr_kwargs` | no | `null` or JSON object (not a string) |
| `defaults.run_duration_sec` | no | `null` or number &gt; 0 |

## Validation outcomes

- File missing, not JSON object, or rule violation → **catalog validate fails the entire build** with path + reason.
- Relative paths in defaults are interpreted relative to the **script directory** at Start unless absolute.

## Example (sample smoke script)

```json
{
  "display_name": "冒烟示例",
  "description": "合规样例：尊重暂停/结束并周期性打日志",
  "defaults": {
    "resource_dir": ".",
    "capture": "dxcam",
    "humanize": true,
    "control_mode": 2,
    "run_duration_sec": null
  }
}
```
