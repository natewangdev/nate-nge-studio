# Quickstart: Script Rule Helper

**Feature**: `002-script-rules` | **Date**: 2026-09-28

## Prerequisites

- Repo synced; `uv sync --group dev`
- Feature branch `002-script-rules`

## Automated

```powershell
uv run pytest tests/unit/test_rule_loop.py -q
uv run python scripts/validate_catalog.py
```

**Expected**: Helper tests green (priority, cooldown, pause gate, stop); catalog still valid.

## Manual (Studio)

```powershell
uv run python -m nge_studio
```

1. Select **demo / 冒烟示例**.
2. Start → logs show RuleLoop activity; at least one rule attempts `capture.grab` (or logs degrade if capture unavailable).
3. Pause → no further rule actions until Resume.
4. Stop or set a short duration (hours) → returns idle; engine closed by Studio.

## Done when

- [ ] `test_rule_loop` + catalog validate pass
- [ ] Smoke uses `RuleLoop` and includes a real engine I/O rule in source
- [ ] Bilingual Spec Kit docs for `002` paired
