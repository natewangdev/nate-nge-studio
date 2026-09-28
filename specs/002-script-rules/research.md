# Research: Script Rule Helper

**Feature**: `002-script-rules` | **Date**: 2026-09-28

## 1. Helper location

- **Decision**: `nge_studio.rules` package (Studio), not NGE2 and not copy of `nge.bot`.
- **Rationale**: Clarification Option B; scripts already import Studio `RunContext` concepts via runner; keeps Bot-like API out of engine until a later feature.
- **Alternatives considered**: Port into NGE2 — deferred; inline only in smoke — rejected (not reusable).

## 2. Slim vs full legacy Bot

- **Decision**: Support name, priority, cooldown, `one_action_per_tick` (default True), shared `state`, fixed `tick_interval_sec`. Omit `session_max_seconds`, `tick_jitter`, `break_every` / `break_duration`.
- **Rationale**: Clarification Option A; Studio already owns duration/pause/stop.
- **Alternatives considered**: Full Bot parity — rejected for this feature.

## 3. Pause gating

- **Decision**: Start of each tick calls `ctx.checkpoint()` (or `wait_if_paused` + stop check). While paused, skip rule evaluation entirely.
- **Rationale**: Clarification Option A; matches cooperative SC timing.
- **Alternatives considered**: Finish current rule then pause — rejected.

## 4. Smoke real NGE2 I/O

- **Decision**: Primary I/O rule calls `engine.capture.grab()` when available (perception). Degrade with warning + `False` if missing/failing so fake engines and CI stay safe. Optional light secondary heartbeat rule for logs only is allowed in addition.
- **Rationale**: Clarification Option B (real API); grab is the lightest perception path and stub-friendly.
- **Alternatives considered**: Always `control.move` — needs HID; log-only — rejected.

## 5. Exception policy

- **Decision**: Catch exceptions from a rule `fn`, log with rule name, treat as non-acting for that rule, continue remaining rules only if `one_action_per_tick` already satisfied policy (prefer: abort rest of tick after error to avoid cascading failures).
- **Rationale**: Spec edge case; keep Studio stop path reachable.
- **Alternatives considered**: Crash the run on first rule error — too harsh for demo/authoring.

## 6. Naming

- **Decision**: Public types `Rule`, `RuleContext`, `RuleLoop`. Method `RuleLoop.add_rule` + `@loop.rule` decorator optional convenience.
- **Rationale**: Clear mapping from legacy Bot without claiming to be Bot.
- **Alternatives considered**: Name `ScriptBot` — more confusion with legacy Bot.
