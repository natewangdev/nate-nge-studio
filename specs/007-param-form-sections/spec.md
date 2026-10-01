# Feature Specification: Param Form Sections Polish

**Feature Branch**: `007-param-form-sections`

**Created**: 2026-10-02

**Status**: Draft

**Input**: User description: "(1) Distinguish section titles「启动参数」/「脚本参数」from field labels; present launch params and script params as two separate bordered titled groups; (2) After window pick, do not show the window title under the hwnd input; (3) Humanize: left-aligned field label, right side checkbox only."

**Authority**: Extends / revises UI presentation in [`../001-nge-studio-mvp/spec.md`](../001-nge-studio-mvp/spec.md) (FR-005 surface, FR-006 window pick display) and [`../006-script-control-params/spec.md`](../006-script-control-params/spec.md) (FR-004 script-params distinct from NGE2 form). Does not change launch semantics, persistence keys, `ctx.script_params`, or duration end-action behavior. Center-column placement remains as in [`../005-three-column-layout/spec.md`](../005-three-column-layout/spec.md).

## Clarifications

### Session 2026-10-02

- Q: How should the two sections be visually structured? → A: Titled group boxes (border + title) labeled **启动参数** and **脚本参数**; field labels use ordinary form-row style, distinct from group titles; when the script has no `script_params`, hide the script group (Option A).
- Q: After a successful window pick, how is the window title shown? → A: Remove the secondary title hint under the hwnd input; still write the picked title into the `window_title` field (Option A).
- Q: Where should this requirement live in specs? → A: New feature `007-…` that revises/extends 001 and 006 UI presentation (Option B).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Two titled parameter groups (Priority: P1)

An operator selects a script in the center column and sees launch/engine/Studio fields inside a bordered group titled **启动参数**, and (when the manifest declares `script_params`) a second bordered group titled **脚本参数**. Group titles look like section headers; individual parameter labels remain ordinary form labels and are visually subordinate to the group titles.

**Why this priority**: Separating NGE2/Studio launch knobs from script-authored knobs is the main readability goal of this polish.

**Independent Test**: Open Studio; select `demo/smoke` (no script_params) and confirm only the **启动参数** group; select `demo/control_params` and confirm both groups with distinct title vs field-label styling.

**Acceptance Scenarios**:

1. **Given** any selected script, **When** the operator views the center parameter form, **Then** NGE2 construction fields and Studio duration / duration-end-action controls appear inside a titled group labeled **启动参数**.
2. **Given** a script whose manifest declares one or more `script_params`, **When** the operator selects it, **Then** those editors appear inside a second titled group labeled **脚本参数**, separate from the launch group (not mixed into the same untitled list).
3. **Given** a script with no `script_params` (or empty list), **When** the operator selects it, **Then** the **脚本参数** group is not shown.
4. **Given** both groups are visible, **When** the operator compares group titles to field labels (e.g. `resource_dir`, `拟人化移动`, script field labels), **Then** group titles are clearly distinct in weight/style from field labels (titles read as section headers; field labels as row captions).

---

### User Story 2 - Window pick without hwnd subtitle (Priority: P1)

After point-and-pick succeeds, the hwnd field shows the handle; the operator sees the window title in the **窗口标题 / window_title** field. No extra title text appears directly under the hwnd input row.

**Why this priority**: Removes duplicate title UI under hwnd while preserving 001 title convenience via `window_title`.

**Independent Test**: Pick a non-Studio window; confirm hwnd filled, `window_title` filled, and no title label/row under hwnd.

**Acceptance Scenarios**:

1. **Given** window pick succeeds on a non-Studio top-level window, **When** the form updates, **Then** `hwnd` is set and `window_title` is set to the picked window’s title (001 FR-006 convenience retained).
2. **Given** that successful pick, **When** the operator looks under the hwnd input row, **Then** no secondary title hint/label is shown there.
3. **Given** Studio’s own window is picked, **When** rejection occurs, **Then** behavior remains as in 001 (prompt; hwnd unchanged); still no hwnd subtitle row is required.

---

### User Story 3 - Humanize row alignment (Priority: P1)

The humanize control uses the same left-label / right-control pattern as other launch fields: left label **拟人化移动** (or equivalent Chinese label aligned with other field labels); right side is a checkbox **without** repeating the label text on the checkbox itself.

**Why this priority**: Fixes the current misaligned checkbox-as-label row.

**Independent Test**: Inspect the humanize row next to `capture` / `control_mode`; label column aligns; checkbox has no text (or only empty).

**Acceptance Scenarios**:

1. **Given** the **启动参数** group is visible, **When** the operator views the humanize row, **Then** the left side shows the field label and the right side shows only a checkbox control (no checkbox caption duplicating the label).
2. **Given** that layout, **When** compared to neighboring form rows, **Then** the humanize label sits in the same label column alignment as other parameter labels.

---

### Edge Cases

- Switching from a script with `script_params` to one without: **脚本参数** group disappears; **启动参数** remains.
- Reset-to-defaults: still restores launch defaults and script-param defaults per 001/006; control placement of the reset button MAY remain below both groups (outside the group boxes).
- Empty hwnd / empty window_title: unchanged Start semantics from 001.
- Very long group titles or many script fields: groups MAY scroll with the center column; titles remain visible as group headers.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The center-column parameter form MUST present NGE2 construction parameters and Studio-owned duration fields inside a bordered titled group whose title is **启动参数**.
- **FR-002**: When the selected script has declared `script_params`, the form MUST present those editors inside a separate bordered titled group whose title is **脚本参数**.
- **FR-003**: When the selected script has no `script_params` fields, the **脚本参数** group MUST be hidden.
- **FR-004**: Group titles (**启动参数** / **脚本参数**) MUST be visually distinct from ordinary parameter field labels (section-header vs row-caption hierarchy).
- **FR-005**: After a successful window pick, Studio MUST NOT show the picked window’s title as a secondary label/hint under the hwnd input. Studio MUST still populate `window_title` with the picked title (revises the “title shown under hwnd” reading of 001 US2 scenario 3 / FR-006 display; pick → `hwnd` + optional `window_title` fill remains).
- **FR-006**: The humanize control MUST use a left field label and a right-side checkbox with no duplicate caption on the checkbox (aligned with other launch parameter rows).
- **FR-007**: This feature MUST NOT change parameter meaning, validation, persistence, Start/resolve/activate behavior, or `ctx.script_params` injection beyond presentation described above.

### Key Entities

- **LaunchParamGroup**: UI section titled **启动参数** containing NGE2 + Studio duration / duration-end-action fields.
- **ScriptParamGroup**: UI section titled **脚本参数** containing dynamic `script_params` editors; absent when schema empty.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On a script with `script_params`, an observer can identify two titled groups (**启动参数** and **脚本参数**) within 3 seconds without reading docs.
- **SC-002**: On a script without `script_params`, only **启动参数** is shown; no empty **脚本参数** shell.
- **SC-003**: After one successful window pick, hwnd has no under-row title hint, and `window_title` contains the picked title.
- **SC-004**: Humanize label aligns with other left-column field labels; checkbox has no text caption.

## Assumptions

- “Bordered titled group” means a group-box style container (title on the border); exact QSS is implementation detail as long as FR-004 holds.
- Reset button stays below the groups unless a later feature relocates it.
- Chinese UI strings remain the operator-facing labels; English ids may still appear in field captions where 001 already does (e.g. `resource_dir`).
- No change to 005 column ratios or control placement under the form.
