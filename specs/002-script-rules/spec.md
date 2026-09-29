# Feature Specification: Script Rule Helper

**Feature Branch**: `002-script-rules`

**Created**: 2026-09-28

**Status**: Draft

**Input**: User description: "In the smoke script `run` entry, adopt the Rule design philosophy from the legacy nate-gaming-engine Bot, while Start / Pause / Stop / run duration remain controlled by the Studio UI layer."

## Clarifications

### Session 2026-09-28

- Q: Where should the Rule loop land? → A: Extract a reusable Studio/script helper (e.g. under `nge_studio`) that smoke demonstrates and other scripts may reuse (Option B). Not NGE2-first-class Bot in this feature.
- Q: How closely to match legacy Bot features? → A: Slim loop: priority, cooldown, `one_action_per_tick`, shared state; **no** tick jitter and **no** `break_every` human breaks (Option A).
- Q: How deep should smoke rules go? → A: At least one rule exercises real NGE2 perception and/or control APIs (Option B); not log-only fake rules.
- Q: Where to document this? → A: New feature spec `002-script-rules`, separate from MVP `001` protocol docs (Option B).
- Q: How does pause interact with the rule loop? → A: Each tick **starts** with `checkpoint` / `wait_if_paused`; while paused, **no** Rule is evaluated (Option A).

### Session 2026-09-30

- Q: How is shared FSM state modeled on `RuleContext`? → A: Authors MUST define a `@dataclass` FSM and pass it into the loop; `rctx.state.field = value` attribute access is required. Plain `dict` state is **not** supported (Option B). Spec updates apply to existing `002` (no new feature number).
- Q: Must smoke demonstrate dataclass FSM? → A: Yes — `demo/smoke` MUST use a dataclass FSM for `rctx.state` (and MAY import game-level `common`/`rules` per `001` FR-017).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Reusable Rule loop for Studio scripts (Priority: P1)

A script author builds a cooperative `run(engine, ctx)` using a Studio-provided Rule helper modeled on the legacy Bot: named rules with priority and cooldown, a **required `@dataclass` FSM** as shared state, and one-action-per-tick evaluation. Studio still owns Start, Pause, Stop, and run-duration timeout via the existing UI and `RunContext`.

**Why this priority**: Without a shared helper, every script reinvents the decision loop and drifts from the established Rule philosophy.

**Independent Test**: Unit-test the helper with a fake engine and fake `RunContext`: register two rules with different priorities on a dataclass FSM; assert attribute updates via `rctx.state`; assert only the higher-priority acting rule fires when `one_action_per_tick` is true; assert pause blocks evaluation until resume; assert stop ends the loop promptly; assert starting without a dataclass FSM is rejected.

**Acceptance Scenarios**:

1. **Given** a script registers multiple rules with priorities, **When** more than one rule would return `True` in the same tick, **Then** with `one_action_per_tick` enabled only the highest-priority ready rule acts that tick.
2. **Given** a rule has a cooldown and just returned `True`, **When** subsequent ticks occur before cooldown elapses, **Then** that rule is skipped until it is ready again.
3. **Given** Studio Pause is active, **When** the rule loop would start a tick, **Then** it waits via `wait_if_paused` / `checkpoint` and does **not** evaluate any rule until resumed or stop is requested.
4. **Given** Studio Stop or run-duration timeout sets stop on `RunContext`, **When** the loop observes `should_stop`, **Then** it exits without requiring the script to implement its own session max timer.
5. **Given** an author imports the helper from Studio, **When** they write a new catalog script, **Then** they can register rules and run the loop without copying Bot code from the legacy engine.
6. **Given** a `@dataclass` FSM instance is supplied to `RuleLoop.run`, **When** a rule assigns `rctx.state.some_field = value`, **Then** subsequent rules in later ticks observe that field value on the same object.
7. **Given** an author attempts to run the loop with a plain `dict` (or omits the required dataclass FSM), **When** `run` is invoked, **Then** the helper rejects the call with a clear error (dict state is not supported).

---

### User Story 2 - Smoke demo uses Rules with real NGE2 I/O (Priority: P1)

The packaged `demo/smoke` script’s `run` is rewritten to use the Rule helper. At least one rule calls a real NGE2 perception and/or control API (not merely logging). Lifecycle (start/pause/stop/duration) remains entirely Studio-driven.

**Why this priority**: Smoke is the primary teaching sample; it must show the intended Rule + Studio ownership split with realistic engine use.

**Independent Test**: Run smoke under Studio (or equivalent) with a real or test double NGE2 that records API calls; start → observe rule-driven engine use in logs/spies; pause → no further rule actions; resume → actions continue; stop or timeout → idle and engine closed by Studio.

**Acceptance Scenarios**:

1. **Given** smoke is selected and started with valid parameters, **When** the run is active, **Then** at least one registered rule invokes an NGE2 perception and/or control method (e.g. find/capture/move/click family as available on the constructed engine).
2. **Given** smoke is running, **When** the operator presses Pause, **Then** rule evaluation stops until Resume (Start/F9 while paused).
3. **Given** smoke is running, **When** the operator presses Stop or Studio duration elapses, **Then** the script returns cooperatively and Studio closes the engine; smoke does **not** enforce its own session max or framework pause.
4. **Given** a CI/fake-engine environment, **When** tests exercise smoke or the helper, **Then** the real-I/O rule is still expressed against the engine API surface (spy/fake may stub the call) so the sample remains valid without requiring HID hardware in CI.

---

### User Story 3 - Document Rule ownership boundaries (Priority: P2)

Authors can read this feature’s contracts/quickstart and understand what Rules own versus what Studio owns, including the explicit non-goals relative to the legacy Bot (`session_max_seconds`, tick jitter, `break_every`).

**Why this priority**: Prevents reintroducing host concerns into script Rules.

**Independent Test**: Review checklist — docs state Studio owns start/pause/stop/duration/engine close; helper provides slim Rule loop only; smoke points to the helper.

**Acceptance Scenarios**:

1. **Given** the feature docs, **When** an author looks for session duration or pause APIs on the helper, **Then** they find none; docs direct them to Studio UI / `RunContext`.
2. **Given** the feature docs, **When** an author compares to legacy Bot, **Then** they see which Bot features are intentionally omitted (jitter, break_every, session_max).

---

### Edge Cases

- Rule raises: helper MUST isolate the failure (log + continue or fail the tick per documented policy) so one bad rule does not silently skip Studio stop handling; prefer log + skip remaining evaluation for that tick unless stop already requested.
- Cooldown of `0`: rule may fire every tick when it returns `True`.
- Empty rule list: loop still honors pause/stop and idle-ticks without acting.
- Fake engine missing perception/control: smoke’s real-I/O rule MUST degrade with a clear log and return `False` (or equivalent) rather than crashing the worker, so Studio can still Stop cleanly.
- Nested/blocking waits inside a rule longer than Studio hung grace: out of scope to force-kill; authors SHOULD keep rule bodies short and rely on tick-boundary pause/stop checks.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a reusable Rule-loop helper in the Studio package (not vendored legacy `nge.bot`) usable from catalog `run(engine, ctx)` entries.
- **FR-002**: A Rule MUST have at least: name, priority, cooldown seconds, and a callable `fn(rule_ctx) -> bool` where `True` means the rule acted this tick.
- **FR-003**: The helper MUST evaluate ready rules in priority order each tick and, when configured for one-action-per-tick (default on), stop evaluating further rules after the first `True`.
- **FR-004**: The helper MUST refresh a rule’s cooldown only after that rule returns `True`.
- **FR-005**: Each tick MUST begin with cooperative Studio pause/stop handling (`wait_if_paused` / `checkpoint` / equivalent). While paused, the helper MUST NOT evaluate any Rule.
- **FR-006**: The helper MUST NOT implement Studio run-duration, Start, Pause, or Stop; those remain Studio UI + `RunContext` + existing runner timeout.
- **FR-007**: The helper MUST NOT provide legacy Bot `session_max_seconds`, tick jitter, or `break_every` / `break_duration` human-break scheduling.
- **FR-008**: The helper MUST require a shared mutable **`@dataclass` FSM instance** for coordination between rules (exposed as `rctx.state`), distinct from Studio `RunContext`. Authors MUST update state via attribute access (`rctx.state.field = value`). Passing a plain `dict` (or omitting the FSM) MUST be rejected. Legacy dict-style `state["key"]` is **out of scope**.
- **FR-009**: `demo/smoke` MUST be rewritten to use the helper with a dataclass FSM and MUST register at least one rule that calls a real NGE2 perception and/or control API on the provided `engine`. Smoke SHOULD demonstrate importing game-level `common` / `rules` when those files exist under `demo/` (per `001` FR-017).
- **FR-010**: Smoke and the helper MUST remain compatible with Studio’s single-flight runner and engine `close()` in `finally`.
- **FR-011**: Automated tests MUST cover helper priority, cooldown, pause gating, stop exit, and dataclass FSM attribute updates without requiring HID hardware.

### Key Entities

- **Rule**: Named decision unit (priority, cooldown, `fn`); returns whether it acted.
- **RuleContext**: Per-tick bag passed to rules: `engine`, **dataclass FSM** `state`, and Studio `RunContext` as `studio`.
- **RuleLoop / ScriptBot** (name flexible): Hosts the list of rules and the tick loop bound to Studio `RunContext`; requires a dataclass FSM for `state`.
- **FSM State**: Author-defined `@dataclass` instance for phase machines across rules (not a dict).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A new script author can wire three prioritized rules and run under Studio pause/stop within 30 minutes using only this feature’s helper docs + smoke as reference.
- **SC-002**: With a compliant smoke run, Pause stops further rule actions within 2 seconds of the pause signal (aligned with Studio SC-003 spirit).
- **SC-003**: Helper unit tests pass in CI without ESP32/HID hardware.
- **SC-004**: Smoke’s real-I/O rule is visible in source (calls engine perception/control API); fake-engine tests still exercise that call path via stubs.

## Assumptions

- Legacy nate-gaming-engine Bot remains the **design reference only**; code is not imported from that repo into Studio.
- NGE2 remains the only engine; Rule helper adapts to the `engine` instance Studio constructs.
- MVP script entry `def run(engine, ctx)` from feature `001` is unchanged; this feature adds an optional recommended pattern on top.
- “Real NGE2 I/O” means calling public engine APIs for vision/find and/or HID control; exact API chosen at implement time may be the lightest reliable call that proves the path (with stub-friendly design for CI).
- Tick rate may be a simple fixed sleep/interval on the helper (no jitter) sufficient for demo and author scripts; precise Hz tuning is not a product requirement beyond being configurable at a basic level if implement chooses.
