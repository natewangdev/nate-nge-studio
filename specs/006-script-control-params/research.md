# Research: 006

**Date**: 2026-10-02

## R1 — request_stop

- **Decision**: Keep existing `RunContext.request_stop()` as the script API (same method Studio Stop uses).
- **Rationale**: Already clears pause and sets stop; no duplicate API.
- **Alternatives**: Separate `script_stop()` — rejected.

## R2 — script_params storage

- **Decision**: Manifest array of field defs; settings `launch_configs[key].script_params` dict beside `parameters`.
- **Rationale**: Keeps NGE2 `LaunchParameters` strict; avoids unknown-key failures.

## R3 — duration_end_action

- **Decision**: Field on `LaunchParameters`: `duration_end_action: "none"|"shutdown"` default `"none"`. Timeout handler calls `stop()` then shutdown executor if action is shutdown and duration was active.
- **Rationale**: Spec Q3 A; manual/script stop cancel timer without shutdown.
- **Shutdown**: `shutdown /s /f /t 0` via injectable callable defaulting to `subprocess.run`.
