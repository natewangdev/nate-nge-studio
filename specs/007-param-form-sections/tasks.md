# Tasks: Param Form Sections Polish

**Input**: Design documents from `/specs/007-param-form-sections/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

## Phase 1: Setup

- [x] T001 Confirm branch `007-param-form-sections` and specs present

## Phase 2: Foundational

- [x] T002 Confirm `APP_QSS` `QGroupBox` title styling is distinct from field labels in `src/nge_studio/ui/styles.py` (bump weight if needed)

## Phase 3: US1 Two titled groups

**Goal**: Launch + script fields in separate GroupBoxes; hide script group when empty

- [x] T003 [US1] Wrap launch fields in `QGroupBox("启动参数")` and script fields in `QGroupBox("脚本参数")` in `src/nge_studio/ui/widgets/param_form.py`
- [x] T004 [US1] Remove obsolete `_script_heading` label; drive visibility via script GroupBox in `param_form.py`

## Phase 4: US2 No hwnd subtitle

- [x] T005 [US2] Remove `hwnd_title` hint row; keep `window_title` fill in `set_hwnd` / `set_parameters` in `param_form.py`

## Phase 5: US3 Humanize alignment

- [x] T006 [US3] Change humanize to left label「拟人化移动」+ caption-less checkbox in `param_form.py`

## Phase 6: Polish

- [x] T007 Run pytest (unit) + ruff; mark tasks done; follow `quickstart.md` manual checklist

## Dependencies

T001 → T002 → T003/T004 → T005 → T006 → T007 (same file; sequential preferred)
