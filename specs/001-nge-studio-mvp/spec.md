# Feature Specification: NGE-STUDIO MVP Shell

**Feature Branch**: `001-nge-studio-mvp`

**Created**: 2026-09-28

**Status**: Draft

**Input**: User description: "NGE-STUDIO — Windows desktop shell to manage multiple NGE2 game scripts: modern tech UI, build-time catalog discovery with manifests, full launch parameters plus Studio timeout, cooperative start/pause/stop with global hotkeys, window picker, live logs, single concurrent run, pip dependency on nate-game-engine, ship as Windows exe."

## Clarifications

### Session 2026-09-28

- Q: Desktop UI technology preference? → A: Python GUI (Option A; PySide6 preferred per constitution).
- Q: Script layout and IDs? → A: Accept `game_scripts/<game_id>/<script_id>/` with `main` entry + required `manifest`; no strong preference on ID character rules beyond stable folder names.
- Q: “Run duration” vs NGE2 init? → A: Studio-layer timeout; UI exposes the full NGE2 construction parameter set plus Studio timeout.
- Q: Pause/stop semantics? → A: Cooperative pause; stop cancels via context then closes the NGE2 engine; scripts implement a unified entry protocol.
- Q: Concurrent runs? → A: Only one script run at a time.
- Q: Global hotkeys? → A: Defaults F9 start / F10 pause / F11 stop; editable in UI and persisted; one binding each.
- Q: Window handle input? → A: Provide point-and-pick window selection.
- Q: Relation to nate-game-engine? → A: Pip dependency (editable local and/or published).
- Q: Distribution? → A: Package as Windows executable.
- Q: Spec language? → A: Same as engine repo — English authoritative + Simplified Chinese companion.
- Q: When a script folder is missing a required manifest or unified entry, should packaging fail the whole build, or skip that script and continue? → A: Fail the entire package/build when any invalid script is found (Option A).
- Q: While a script is paused, how should the operator resume—reuse Start (F9), or a separate Resume control? → A: When paused, the same Start control and F9 become Resume (Option A).
- Q: If the operator picks NGE-STUDIO’s own window during window pick, should that be disallowed or allowed into hwnd? → A: Disallow selecting Studio’s own window and prompt the operator to choose another (Option A).
- Q: After a script run ends (idle), should the log panel clear or keep that run’s logs? → A: Keep the last run’s logs until the next Start clears/replaces them with the new stream (Option A).
- Q: Must hwnd be set before Start, or may it be left empty like NGE2 (screen-absolute coordinates)? → A: hwnd is optional; empty starts with NGE2 screen-coordinate semantics (Option B).
- Q: Should `ocr_kwargs` get a file-picker like path fields? → A: No file picker for `ocr_kwargs` (JSON text only); file pickers apply to YOLO model and YOLO names (Option B).
- Q: What file-dialog filters for YOLO model / names? → A: Suggested filters `*.onnx` (model) and `*.names`/`*.txt` (names), with an All files fallback (Option A).
- Q: After picking a path, store absolute or relative? → A: Write a path relative to `resource_dir` when the selection is under that directory; otherwise write an absolute path (Option B).
- Q: If `resource_dir` is empty/invalid when opening a picker, where should the dialog start? → A: Fall back to the user home directory (Option A).
- Q: UI run duration in hours — change persisted field? → A: Keep storing `run_duration_sec`; UI edits hours and converts (`hours × 3600`) on read/write (Option A).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Browse packaged games and scripts (Priority: P1)

An operator opens NGE-STUDIO and sees the games and scripts that were included when this build was packaged. Each script shows human-readable metadata from its manifest. After the maintainer adds a new game folder or script folder in source and rebuilds, the new items appear in that new build’s UI.

**Why this priority**: Without a discoverable catalog, no other studio capability has a target.

**Independent Test**: Package (or run a catalog scan equivalent used by packaging) with sample `game_scripts` tree including manifests; launch the app; verify games/scripts and display names; omit a script and rebuild; verify absence/presence matches the packaged tree.

**Acceptance Scenarios**:

1. **Given** a packaged build that includes at least one game with one valid script (entry + manifest), **When** the operator opens the catalog, **Then** the game and script appear with the manifest display name (falling back to folder ID if display name missing).
2. **Given** a script directory missing a required manifest or unified entry, **When** packaging/catalog validation runs, **Then** the entire package/build fails with a clear error that identifies the offending path.
3. **Given** a new script folder was added under an existing game in source, **When** the operator runs an older build that was packaged before that addition, **Then** the new script does **not** appear until a rebuild/repackage includes it.
4. **Given** multiple games each with multiple scripts, **When** the operator browses the catalog, **Then** items are grouped by game and each script is selectable independently.

---

### User Story 2 - Configure launch parameters and pick a target window (Priority: P1)

After selecting a script, the operator configures NGE2 launch parameters (full construction set) and a Studio run-duration timeout, optionally loading defaults from the script manifest. Path-like fields support both typing and OS browse dialogs. The operator can pick a target window visually instead of typing a handle, and the chosen handle is applied to the hwnd parameter.

**Why this priority**: Correct parameters and window binding are required before a useful run.

**Independent Test**: Select a script; edit each exposed parameter; use folder/file browse for path fields; use window picker on a known window; enter a fractional hour timeout; confirm saved session values apply on next select of that script; clear timeout and verify “no Studio timeout” behavior.

**Acceptance Scenarios**:

1. **Given** a selected script, **When** the operator views launch settings, **Then** the UI exposes the full documented NGE2 construction parameter set needed by authors (`resource_dir`, `hwnd`, `capture`, `humanize`, `control_mode`, `log_dir`, `yolo_model`, `yolo_names`, `ocr_kwargs`) plus a Studio-owned run-duration timeout shown in **hours**.
2. **Given** the script manifest provides default parameter values, **When** the operator first selects the script (or resets to defaults), **Then** those defaults populate the form (run duration displayed as hours when `run_duration_sec` is set).
3. **Given** the operator activates window pick mode, **When** they select a visible top-level window that is not Studio itself, **Then** the corresponding window handle is written into the hwnd field and a recognizable window title/label is shown.
4. **Given** the operator activates window pick mode, **When** they attempt to select NGE-STUDIO’s own window, **Then** the selection is rejected, hwnd is not changed to Studio’s handle, and the operator is prompted to choose another window.
5. **Given** the operator sets a positive run-duration timeout in hours (including non-integers such as `0.5`), **When** a run exceeds that duration, **Then** Studio stops the run using the same stop path as manual stop (cancel + engine close).
6. **Given** the operator leaves run-duration empty/disabled, **When** a script runs, **Then** Studio does not stop it solely due to elapsed time.
7. **Given** the operator edited parameters for a script, **When** they leave and later re-select that script in the same user profile/machine settings store, **Then** the last-used parameter values are restored.
8. **Given** a valid `resource_dir`, **When** the operator uses Browse on `resource_dir` or `log_dir`, **Then** a folder dialog opens (starting under `resource_dir` when that dialog should) and the chosen folder is written into the field; the operator may also type a path manually.
9. **Given** a valid `resource_dir`, **When** the operator uses Browse on `yolo_model` or `yolo_names`, **Then** a file dialog opens starting at `resource_dir` (suggested filters `*.onnx` / `*.names`+`*.txt` plus All files), and the chosen path is written relative to `resource_dir` when under that directory, otherwise absolute; `ocr_kwargs` remains JSON text **without** a file Browse control.
10. **Given** `resource_dir` is empty or not an existing directory, **When** the operator opens any path browse dialog that would start at `resource_dir`, **Then** the dialog starts at the user home directory instead.
11. **Given** the launch parameter form is visible, **When** the operator compares the window-pick button and path-browse buttons to their row inputs, **Then** those buttons share the same control height as the adjacent input fields.

---

### User Story 3 - Start, pause, and stop a script (Priority: P1)

The operator starts the selected script with current parameters. Only one run may be active. They can pause and resume cooperatively (while paused, Start/F9 act as Resume), and stop to cancel and release the engine. The same actions are available via on-screen buttons and global hotkeys (defaults F9/F10/F11), and hotkey bindings can be changed and persist.

**Why this priority**: Lifecycle control is the core operating loop of the studio.

**Independent Test**: Run a compliant sample script that honors pause/stop; exercise UI buttons and hotkeys; attempt a second start while running; verify engine resources are released after stop; change hotkeys, restart app, verify bindings.

**Acceptance Scenarios**:

1. **Given** a selected script with valid parameters and no active run, **When** the operator presses Start (UI or hotkey), **Then** Studio constructs NGE2 with those parameters, invokes the unified script entry with a run context, and shows a running state.
2. **Given** a selected script with hwnd left empty and otherwise valid parameters, **When** the operator presses Start, **Then** Studio starts successfully and NGE2 treats coordinates as screen-absolute physical pixels (no window binding).
3. **Given** a script is running, **When** the operator presses Pause, **Then** the run context reports paused and the compliant script stops progressing work until resumed (cooperative).
4. **Given** a paused run, **When** the operator presses Start/Resume (the Start control and F9 hotkey act as Resume while paused), **Then** the run context clears pause and the script may continue.
5. **Given** a running or paused script, **When** the operator presses Stop, **Then** the run context signals cancel, the script entry returns/aborts cooperatively, and Studio closes the NGE2 engine instance.
6. **Given** a run is already active, **When** the operator attempts to start another script (or the same again), **Then** Studio refuses and explains that only one run is allowed.
7. **Given** default hotkeys, **When** the operator presses F9 / F10 / F11 while the app is running (and hotkeys are enabled), **Then** start / pause / stop are triggered respectively even if another window is focused (global).
8. **Given** the operator changes hotkey bindings in settings, **When** they restart the application, **Then** the new bindings remain in effect.

---

### User Story 4 - Watch live logs while a script runs (Priority: P2)

While a script is running (or paused), the operator watches a scrolling live log panel that reflects engine/script log output with low latency suitable for monitoring. After stop, those lines remain visible until the next start.

**Why this priority**: Operators need visibility to diagnose stuck or misconfigured runs without attaching an external debugger.

**Independent Test**: Run a sample script that emits periodic log lines; verify lines appear in the UI in order; stop the run and confirm the panel retains that run’s lines until the next Start.

**Acceptance Scenarios**:

1. **Given** a running script that emits log lines, **When** the operator views the log panel, **Then** new lines appear without requiring manual refresh, in chronological order.
2. **Given** a high volume of log lines, **When** the panel updates, **Then** the UI remains usable (operator can still press stop); oldest lines MAY be trimmed after a documented cap.
3. **Given** no active run after a completed or stopped session, **When** the operator views the log panel, **Then** they still see that last run’s retained lines (not another script’s live stream).
4. **Given** retained lines from a previous run, **When** the operator starts a new run, **Then** the log panel clears (or replaces) those lines and begins showing the new run’s stream.

---

### User Story 5 - Ship and launch a Windows executable (Priority: P2)

A maintainer produces a Windows executable build of NGE-STUDIO that includes the packaged script catalog. An operator launches the exe on a supported Windows machine and uses the catalog/run flows without installing a separate Python toolchain as a user step.

**Why this priority**: Distribution as exe is an explicit product requirement for operators.

**Independent Test**: Build the packaged exe with at least one sample script; run it on a clean-ish Windows environment; verify catalog and a dry/mock run path work per Definition of Done in the plan.

**Acceptance Scenarios**:

1. **Given** a successful packaging pipeline, **When** the maintainer completes a release build, **Then** a Windows executable artifact is produced that embeds/bundles the script catalog for that build.
2. **Given** the packaged exe on a supported Windows system, **When** the operator double-clicks/launches it, **Then** the main UI opens and the catalog matches what was packaged.

---

### Edge Cases

- Invalid hwnd (window closed after pick): start fails with a clear error before or at engine construction; no zombie run state.
- Missing `resource_dir` or YOLO model paths: start fails with actionable error from Studio and/or NGE2; UI shows the message.
- Script ignores cooperative pause/stop: Stop still attempts cancel + engine close; if the entry does not return within a documented grace period, Studio surfaces a hung-script warning (force-kill optional later; not required for MVP unless plan adopts it).
- Hotkey conflict with another global hook: Studio reports registration failure and keeps previous binding or unbound state visibly.
- Manifest present but malformed JSON/fields: entire package/build fails with a clear error that identifies the offending path.
- Operator picks a window belonging to Studio itself: selection is rejected; hwnd is unchanged; operator is prompted to pick another window.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST present a modern, tech-oriented visual desktop UI on Windows for managing NGE2 game scripts.
- **FR-002**: System MUST discover games/scripts from a conventional source tree of the form `game_scripts/<game_id>/<script_id>/` at build/package time (and in development via the same catalog rules used for packaging).
- **FR-003**: Each script directory MUST include a `manifest` file and a unified entry module; packaging/catalog validation MUST fail the entire build if any discovered script directory violates the documented protocol or manifest rules (clear error naming the path).
- **FR-004**: Manifest MUST support at least: display name, optional description, and optional default launch parameter values. Game ID and script ID MUST be the folder names.
- **FR-005**: Selecting a script MUST allow configuring the full NGE2 construction parameter surface: `resource_dir`, `hwnd`, `capture`, `humanize`, `control_mode`, `log_dir`, `yolo_model`, `yolo_names`, `ocr_kwargs`, plus Studio run-duration timeout. `hwnd` MUST be optional; an empty hwnd MUST still allow Start, with NGE2 screen-absolute coordinate semantics.
- **FR-005a**: `resource_dir` and `log_dir` MUST each provide a text input and a Browse control that opens a **folder** dialog; values MAY also be typed manually.
- **FR-005b**: `yolo_model` and `yolo_names` MUST each provide a text input and a Browse control that opens a **file** dialog (suggested filters: model `*.onnx`; names `*.names` and `*.txt`; plus All files). `ocr_kwargs` MUST remain editable JSON text and MUST NOT offer a file Browse control.
- **FR-005c**: Path/file browse dialogs MUST start in the current `resource_dir` when that path is a non-empty existing directory; otherwise they MUST start in the user home directory. After a successful pick, if the chosen path is under `resource_dir`, the field MUST store a path relative to `resource_dir`; otherwise it MUST store an absolute path.
- **FR-005d**: Studio run-duration MUST be edited in the UI as **hours** (non-integer values allowed, e.g. `0.5`). Persistence and the runner MUST continue to use `run_duration_sec` (seconds = hours × 3600). Empty/omitted/≤0 means no Studio timeout.
- **FR-005e**: The window-pick button and path Browse buttons MUST match the visual height of their adjacent input fields on the same row.
- **FR-006**: System MUST provide a visual window-picker to populate `hwnd` from a user-selected top-level window. Selecting NGE-STUDIO’s own window MUST be rejected with a clear prompt; hwnd MUST NOT be set to Studio’s handle.
- **FR-007**: System MUST persist per-script last-used launch parameters and global hotkey bindings across application restarts on the same machine/user profile.
- **FR-008**: System MUST support Start, cooperative Pause, and Stop for the active run via UI controls and via three configurable global hotkeys (defaults F9 / F10 / F11). While paused, the Start control and its hotkey MUST act as Resume (no separate Resume control required).
- **FR-009**: System MUST allow at most one active script run at a time and refuse additional starts with a clear message.
- **FR-010**: Scripts MUST be invoked through a unified entry protocol that receives an NGE2 engine instance and a run context exposing pause and cancel/stop signals.
- **FR-011**: On Stop (or Studio timeout), System MUST signal cancel through the run context and close the NGE2 engine instance when the run ends.
- **FR-012**: When Studio run-duration timeout is set and elapses, System MUST stop the run using the same cancel + engine-close path as manual Stop.
- **FR-013**: System MUST display near-real-time log output for the active run in the UI. After a run ends, the panel MUST retain that run’s lines until the next Start clears or replaces them with the new run’s stream.
- **FR-014**: System MUST depend on `nate-game-engine` / `nge2` via pip (editable local path and/or published package), not a vendored engine copy.
- **FR-015**: System MUST be shippable as a Windows executable that includes the packaged script catalog for that build.
- **FR-016**: Adding games/scripts in source MUST require rebuild/repackage before they appear in that build’s UI catalog.

### Key Entities

- **Game**: A folder under `game_scripts` identified by `game_id`; groups related scripts.
- **Script**: A folder under a game identified by `script_id`; has manifest, unified entry, and optional resources referenced by parameters.
- **Manifest**: Metadata and optional default launch parameters for a script.
- **Launch Configuration**: Operator-facing parameter set (NGE2 construction fields + Studio timeout) for a script, including last-used values.
- **Run Context**: Signals cooperative pause and cancel/stop to the running script entry.
- **Run Session**: The single active execution (script identity, state: idle/running/paused/stopping, associated logs).
- **Hotkey Binding**: Mapping of Start/Pause/Stop actions to global key combinations, persisted in settings.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: An operator can open the app, select a packaged sample script, set parameters (including window pick), and start a run in under 3 minutes without reading external docs beyond in-app labels.
- **SC-002**: 100% of scripts that appear in a given build’s catalog were present in that build’s packaged `game_scripts` tree; scripts added only in source after packaging never appear in the older build.
- **SC-003**: With a compliant sample script, pause stops observable progress within 2 seconds of the pause signal, and stop returns the UI to idle with engine resources released within 5 seconds under normal conditions.
- **SC-004**: While a sample script logs at least once per second, the UI log panel shows new lines with perceived lag under 1 second on a typical developer machine.
- **SC-005**: After changing hotkeys and restarting the app, the new bindings work on the first try without reconfiguration.
- **SC-006**: A maintainer can produce a Windows executable artifact via the documented packaging path, and an operator can launch that artifact and see the packaged catalog without installing Python manually.

## Assumptions

- Target operators are local Windows users controlling their own machine; no multi-user accounts or remote orchestration in MVP.
- Sample/demo game scripts sufficient for acceptance testing will be added in-repo under `game_scripts/`.
- NGE2 remains the only supported engine; scripts do not embed alternate automation stacks.
- “Full NGE2 construction parameters” means the documented public constructor fields intended for authors; internal factory hooks (`capture_factory`, `transport_factory`, `ocr_factory`, `yolo_factory`) are advanced/testing knobs and are **out of MVP UI** unless a later clarification includes them.
- `hwnd` may be left empty at Start; behavior matches NGE2 unbound-window (screen-absolute) semantics.
- `ocr_kwargs` is exposed as an advanced structured field (JSON text) rather than a large dedicated form or file picker in MVP.
- Path browse UX (folders for `resource_dir`/`log_dir`, files for YOLO fields, relative-when-under-`resource_dir`, home fallback) applies only to the launch-parameter form; it does not change NGE2 constructor semantics.
- Run-duration **display unit is hours**; the canonical stored field remains `run_duration_sec` in manifests and settings for backward compatibility.
- Global hotkeys require appropriate OS permissions; failure modes are reported in-app.
- Visual design direction (modern + tech) will be detailed in the implementation plan/UI guidelines without blocking this spec.
- Packaging tool choice (e.g. PyInstaller vs alternatives) is a plan decision, not a product requirement beyond “Windows exe”.
