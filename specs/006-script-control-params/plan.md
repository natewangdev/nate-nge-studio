# Implementation Plan: Script Self-Stop, Script Params, Duration End Action

**Branch**: `006-script-control-params` | **Date**: 2026-10-02 | **Spec**: [spec.md](./spec.md)

## Summary

1. Expose/document `RunContext.request_stop()` for scripts (already used by Studio Stop); attach `ctx.script_params`.
2. Manifest `script_params` schema + validation; dynamic UI; persist values; inject at Start.
3. Studio field `duration_end_action` (`none`|`shutdown`); on duration timeout only: stop then optional forced Windows shutdown (injectable).

## Technical Context

Python 3.11+, PySide6, existing runner/settings/catalog. Tests: pytest with fake engine; mock shutdown executor.

## Constitution Check

PASS — NGE2 still sole engine; cooperative stop; catalog manifests extended additively; shutdown behind injectable boundary for tests.

## Project Structure

```text
src/nge_studio/runner/context.py, service.py, shutdown.py (new)
src/nge_studio/catalog/models.py, validate.py
src/nge_studio/settings/store.py
src/nge_studio/ui/widgets/param_form.py, main_window.py
tests/unit/test_run_context.py, test_script_params.py, test_catalog.py
tests/integration/test_runner.py
```
