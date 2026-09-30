# Contract: Game Manifest Schema

**Feature**: `004-icon-game-display` | **Date**: 2026-09-30

File: `game_scripts/<game_id>/manifest.json` (UTF-8 JSON object). **Optional.**

Distinct from script manifests at `game_scripts/<game_id>/<script_id>/manifest.json`.

## Schema (conceptual)

```json
{
  "display_name": "string (optional)",
  "description": "string (optional)"
}
```

## Field rules

| Field | Required | Notes |
|-------|----------|-------|
| `display_name` | No | Empty/missing → UI shows `game_id` |
| `description` | No | Free text; catalog may ignore for v1 label |
| `defaults` | **Forbidden** | Launch defaults belong on script manifests only |
| Other keys | **Forbidden** | Strict: unknown key → catalog validation fails |

## Validation outcomes

- File absent → OK (not an error).
- File present + invalid JSON / non-object / rule violation → **entire catalog validation fails**, error includes path + reason.
- Catalog discovery MUST NOT treat this file as a script entry.

## Example

```json
{
  "display_name": "演示游戏",
  "description": "样例与冒烟脚本所在游戏"
}
```
