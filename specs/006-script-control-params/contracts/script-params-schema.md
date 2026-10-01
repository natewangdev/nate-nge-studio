# Contract: Script Params Schema

**Feature**: `006-script-control-params` | **Date**: 2026-10-02

Extends script `manifest.json` (see 001 manifest-schema). Additive top-level key `script_params`.

## Manifest shape (conceptual)

```json
{
  "display_name": "红门",
  "defaults": { "resource_dir": ".", "run_duration_sec": null },
  "script_params": [
    {
      "id": "friend_name",
      "type": "string",
      "label": "好友名称",
      "default": "路西法"
    },
    {
      "id": "loop_count",
      "type": "int",
      "label": "循环次数",
      "default": 1
    },
    {
      "id": "difficulty",
      "type": "choice",
      "label": "难度",
      "default": "normal",
      "choices": ["normal", "hard"]
    }
  ]
}
```

## Field rules

| Field | Required | Notes |
|-------|----------|-------|
| `script_params` | no | If present: non-empty JSON **array** of field objects (empty array allowed → no UI fields) |
| `id` | yes | Unique within the script; pattern `[a-zA-Z_][a-zA-Z0-9_]*` |
| `type` | yes | One of: `string`, `int`, `number`, `bool`, `choice` |
| `label` | no | UI label; fallback `id` |
| `default` | no | Must match type; for `choice` must be in `choices` if both set |
| `choices` | yes if `type=choice` | Non-empty array of strings |

Unknown keys on a field object → catalog validation **fail** (strict).

`defaults` (NGE2 + Studio duration) MUST NOT be mixed into `script_params`.

## Runtime

- Resolved values exposed as `ctx.script_params: Mapping[str, Any]` for the active run.
- Persistence: under settings launch overlay per script key, e.g. `script_params: { "friend_name": "..." }` alongside existing `parameters` (exact JSON nesting is an implement detail; MUST round-trip).

## Validation outcomes

- Malformed `script_params` → **entire catalog validation fails** with path + reason.
