# Contract: Manifest Schema

**Feature**: `001-nge-studio-mvp` | **Date**: 2026-09-28

Chinese companion: [`manifest-schema.zh-CN.md`](./manifest-schema.zh-CN.md).

File: `game_scripts/<game_id>/<script_id>/manifest.json` (UTF-8 JSON object).

## Schema (conceptual)

```json
{
  "display_name": "string (optional)",
  "description": "string (optional)",
  "sort_order": 0,
  "defaults": {
    "resource_dir": "string (optional)",
    "hwnd": null,
    "window_title": null,
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
| `sort_order` | no | JSON integer if present (not bool/float/`null`). Catalog list order: see `specs/008-catalog-sort-order/contracts/sort-order.md`. Missing → omitted group |
| `defaults` | no | Object; unknown keys → validate **fail** (strict) |
| `defaults.capture` | no | Only `"dxcam"` or `"mss"` if present |
| `defaults.hwnd` | no | `null` or non-negative int |
| `defaults.window_title` | no | `null` or string; title substring for resolve-when-hwnd-empty |
| `defaults.ocr_kwargs` | no | `null` or JSON object (not a string) |
| `defaults.run_duration_sec` | no | `null` or number &gt; 0 (seconds). UI edits this as hours (`× 3600`). |

## Validation outcomes

- File missing, not JSON object, or rule violation → **catalog validate fails the entire build** with path + reason.
- Path resolution at Start:
  - Relative `resource_dir` → relative to the **script directory**.
  - Relative `log_dir` → relative to the **resolved `resource_dir`** (same base as UI-relative storage under FR-005c / FR-005h).
  - Relative YOLO paths → per NGE2 against `resource_dir`.
  - Absolute paths unchanged.

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
