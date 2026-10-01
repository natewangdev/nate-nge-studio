# Feature Specification: Script Self-Stop, Script Params, Duration End Action

**Feature Branch**: `006-script-control-params`

**Created**: 2026-10-02

**Status**: Draft

**Input**: User description: "(1) Scripts may actively end their own run; (2) each script may declare launch parameters distinct from NGE2 engine construction params; (3) when run duration is set, add an end action choice: none | shutdown (default none); shutdown forces OS power-off after Studio timeout stop."

**Authority**: Extends [`../001-nge-studio-mvp/spec.md`](../001-nge-studio-mvp/spec.md) (RunContext / FR-010–012, launch form / FR-005d, manifest) and [`../001-nge-studio-mvp/contracts/script-protocol.md`](../001-nge-studio-mvp/contracts/script-protocol.md). Does not change NGE2 construction field set ownership.

## Clarifications

### Session 2026-10-02

- Q: How does a script request its own end? → A: `ctx.request_stop()`; script SHOULD return promptly; same lifecycle as UI Stop (Option A).
- Q: How are per-script params declared and injected? → A: Manifest `script_params` schema; UI builds dynamic fields; values available as **`ctx.script_params`** (dict); `run(engine, ctx)` signature unchanged (Option A).
- Q: When does “关机” run? → A: **Only** after Studio run-duration timeout with end action = shutdown: stop script + close engine first, then force OS shutdown. Manual Stop and script `request_stop` do **not** shut down (Option A).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Script requests its own stop (Priority: P1)

A script author decides the run is finished (e.g. dungeon complete) and calls `ctx.request_stop()`. Studio treats this like an operator Stop: cooperative cancel is already signaled, `run` returns, engine closes, UI returns to idle. Live logs for that run are retained until the next Start (001 FR-013).

**Why this priority**: Without a supported self-stop API, authors must busy-wait on flags or hang until external Stop.

**Independent Test**: Sample script calls `ctx.request_stop()` after a short delay; verify UI becomes idle, engine closed, no hung warning under normal return; RuleLoop/`should_stop` loops exit.

**Acceptance Scenarios**:

1. **Given** a running script, **When** it calls `ctx.request_stop()` and returns from `run` promptly, **Then** Studio reaches idle with the NGE2 engine closed, using the same post-run cleanup as manual Stop.
2. **Given** a running script calls `ctx.request_stop()`, **When** `should_stop()` / `checkpoint()` are polled afterward, **Then** stop is observed as true (same as after UI Stop).
3. **Given** a script called `request_stop` (not a duration timeout), **When** the run ends, **Then** Studio does **not** initiate OS shutdown even if duration end action is set to shutdown.
4. **Given** `request_stop` was called but `run` does not return within the existing grace period, **When** the grace period elapses, **Then** hung-script behavior follows 001 (warning; no force-kill requirement beyond 001).

---

### User Story 2 - Per-script parameters (not NGE2) (Priority: P1)

A script author declares custom parameters in the script manifest (`script_params`), separate from NGE2 construction `defaults`. The operator sees those fields in the launch UI when the script is selected, can edit them, and last-used values persist per script. Inside `run`, the script reads **`ctx.script_params`** (a dict of current values). NGE2 fields remain on the existing engine/Studio form surface.

**Why this priority**: Game scripts need author-defined knobs (friend name, thresholds, etc.) without overloading NGE2 ctor params.

**Independent Test**: Manifest with at least one string and one bool script param; select script; edit values; Start; script logs `ctx.script_params`; reselect restores last-used; invalid manifest schema fails catalog validation.

**Acceptance Scenarios**:

1. **Given** a script manifest declares `script_params` with typed fields and defaults, **When** the operator selects that script, **Then** the UI shows those fields distinct from NGE2 construction parameters.
2. **Given** the operator edits script params and starts a run, **When** the script reads `ctx.script_params`, **Then** values match the form at Start (types coerced per schema).
3. **Given** a script with no `script_params` key, **When** the operator selects it, **Then** no extra script-param fields appear and `ctx.script_params` is an empty dict (or equivalent empty mapping).
4. **Given** last-used script param values were saved for `game_id/script_id`, **When** the operator re-selects that script, **Then** those values are restored (merged over manifest defaults).
5. **Given** `script_params` schema is malformed or uses unsupported types/keys, **When** catalog validation runs, **Then** validation fails with a clear path + reason (same hard-fail spirit as 001 manifests).
6. **Given** a running script, **When** it accesses parameters, **Then** it MUST use `ctx.script_params` for script-owned params and MUST NOT require changing the `run(engine, ctx)` signature.

---

### User Story 3 - Duration end action: none or shutdown (Priority: P1)

When the operator sets a positive Studio run duration, they can also choose a duration end action: **无** (default) or **关机**. If **无**, timeout only stops the script as today (FR-012). If **关机**, after the timeout stop path completes (cancel + engine close / join per 001), Studio issues a **forced OS shutdown** command. Manual Stop and script `request_stop` never trigger shutdown from this setting.

**Why this priority**: Unattended overnight runs need a safe, explicit power-off option tied only to the timer.

**Independent Test**: With duration set and action=无, confirm timeout stops without shutdown (or dry-run stub); with action=关机, confirm shutdown command is invoked only after stop path (use injectable/mock shutdown in tests; do not require real power-off in CI).

**Acceptance Scenarios**:

1. **Given** run duration is empty/disabled, **When** the operator views launch settings, **Then** the duration end-action control is unavailable or ignored (no shutdown path from this feature).
2. **Given** positive duration and end action **无**, **When** duration elapses, **Then** Studio stops the run like FR-012 and does not shut down the OS.
3. **Given** positive duration and end action **关机**, **When** duration elapses, **Then** Studio first performs the normal timeout stop (signal stop, join/close engine per 001), **then** executes a forced Windows shutdown.
4. **Given** end action is **关机**, **When** the operator presses Stop or the script calls `request_stop` before the timer fires, **Then** the OS is not shut down by this setting.
5. **Given** end action **关机** and the stop path is in progress, **When** shutdown is attempted, **Then** Studio uses a forced shutdown mechanism appropriate for Windows (operator-visible log line before issuing the command).
6. **Given** end action is persisted per script with other launch settings, **When** the operator re-selects the script, **Then** the last-used end action is restored (default **无** when never set).

---

### Edge Cases

- `request_stop` while paused: pause clears / stop wins (same as UI Stop clearing pause).
- `script_params` value type mismatch at Start: refuse Start with clear UI error (or coerce only where schema allows).
- Unknown `script_params` keys in persisted settings: ignore unknown keys; do not crash.
- Shutdown command fails (permissions): surface error in UI/log; machine may remain on; script already stopped.
- Duration end action stored when duration later cleared: treat as effectively **无** until duration is set again (or keep stored value but do not apply).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `RunContext` MUST expose `request_stop()` callable from the script worker thread; once called, `should_stop()` MUST be true and pause MUST not block exit (aligned with UI Stop signaling).
- **FR-002**: Script-initiated `request_stop()` MUST use the same run teardown as manual Stop (engine close after `run` returns / grace rules per 001); it MUST NOT by itself trigger OS shutdown.
- **FR-003**: Script manifests MUST support an optional `script_params` declaration (schema in this feature’s contract), separate from NGE2 `defaults`.
- **FR-004**: When a script is selected, the UI MUST render editors for declared `script_params` distinct from the NGE2 construction parameter form.
- **FR-005**: At Start, Studio MUST supply the resolved script param map on the run context as `ctx.script_params` (read-only mapping for the script). The entry signature remains `run(engine, ctx)`.
- **FR-006**: Last-used `script_params` values MUST persist per `game_id/script_id` in the settings store, merged over manifest defaults on select.
- **FR-007**: Catalog validation MUST hard-fail on invalid `script_params` schema (unsupported type, bad structure) with path + reason.
- **FR-008**: Supported script param types for this feature MUST include at least: `string`, `int`, `number`, `bool`, and `choice` (enumerated strings). (Path browse for script params is out of scope unless added later.)
- **FR-009**: When Studio run duration is set (>0), the UI MUST offer duration end action **无** | **关机**, default **无**.
- **FR-010**: Duration end action **无** MUST preserve FR-012 behavior only (stop run; no OS shutdown).
- **FR-011**: Duration end action **关机** MUST run only after Studio duration timeout stop processing; then Studio MUST issue a forced Windows shutdown. Manual Stop and script `request_stop` MUST NOT trigger this shutdown.
- **FR-012**: Duration end action MUST persist with launch settings per script; default when absent is **无**.
- **FR-013**: Implementation MUST allow tests to inject/replace the shutdown command executor so CI never requires a real power-off.

### Key Entities

- **RunContext** (extended): pause/stop signals + `request_stop()` + `script_params` mapping for the active run.
- **ScriptParamField**: Manifest-declared field (id, type, label, default, optional choices).
- **ScriptParams**: Resolved dict of values for one Start.
- **DurationEndAction**: Enum-like Studio setting: `none` | `shutdown` (UI: 无 | 关机).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A sample script that calls `request_stop()` within 2 seconds of Start returns the UI to idle with engine released within 5 seconds under normal conditions (aligned with 001 stop targets).
- **SC-002**: An operator can configure at least two different script_params on a sample script and observe those exact values inside the script on the first Start without editing NGE2 fields.
- **SC-003**: With duration end action **无**, timeout stops the run and leaves the machine powered on (verified via mock: shutdown executor not called).
- **SC-004**: With duration end action **关机**, after timeout the shutdown executor is invoked exactly once and only after stop signaling has begun (ordering verified in tests).
- **SC-005**: Catalog validation rejects 100% of fixtures with illegal `script_params` schema in the feature’s test set, each with a path-identifying error.

## Assumptions

- Forced shutdown on Windows means a force flag equivalent to `shutdown /s /f` with minimal/zero delay (exact argv is an implementation detail behind FR-013).
- No extra confirmation dialog is required at timeout (operator opted in via the setting); a log line before shutdown is required for observability.
- `script_params` ids are stable string keys (`[a-zA-Z_][a-zA-Z0-9_]*`); labels are UI-only.
- NGE2 `defaults` and Studio `run_duration_sec` / duration end action remain on the Studio-owned form; they are not declared inside `script_params`.
- RuleLoop authors check `studio_ctx.should_stop()` as today; after `request_stop`, loops exit the same way.
- Non-Windows packaging remains out of scope for the shutdown action (feature targets Windows Studio builds).
