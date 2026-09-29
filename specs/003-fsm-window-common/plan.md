# Implementation Plan: FSM / Window Title / Game Commons

**Branch**: `003-fsm-window-common` | **Date**: 2026-09-30  
**Spec**: [spec.md](./spec.md) (implements 001 FR-005f/g/017 + 002 FR-008+)

## Summary

1. `RuleLoop.run(..., state=dataclass)` required; type `RuleContext.state` accordingly.  
2. `window_title` on LaunchParameters/UI/settings; resolve via `Window(None).find_by_title`; activate after NGE2 construct.  
3. Loader adds game directory to `sys.path`; add `demo/common.py` + `rules.py`; rewrite smoke to use FSM + shared imports.

## Technical Context

Python 3.11+, existing Studio/NGE2 stack, pytest without HID.

## Constitution Check

PASS — NGE2 sole engine; cooperative single runner; catalog dirs unchanged; bilingual 001/002 already updated.

## Project Structure

```text
src/nge_studio/rules/loop.py, models.py
src/nge_studio/catalog/models.py
src/nge_studio/runner/engine_factory.py, loader.py, window_resolve.py (new)
src/nge_studio/ui/widgets/param_form.py
game_scripts/demo/common.py, rules.py, smoke/main.py
tests/unit/test_rule_loop.py, test_window_resolve.py
```
