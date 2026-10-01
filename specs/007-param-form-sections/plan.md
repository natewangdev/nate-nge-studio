# Implementation Plan: Param Form Sections Polish

**Branch**: `007-param-form-sections` | **Date**: 2026-10-02 | **Spec**: [spec.md](./spec.md)

## Summary

Polish the center-column parameter form: wrap launch fields in a **启动参数** `QGroupBox` and script fields in a **脚本参数** `QGroupBox` (hide when empty); remove the hwnd under-row title hint while still filling `window_title` on pick; align humanize as left label + caption-less checkbox. Reuse existing `APP_QSS` `QGroupBox` title styling so section titles differ from form field labels.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: PySide6 (existing)  
**Storage**: N/A (presentation only)  
**Testing**: Manual UI check + existing unit tests; optional Qt smoke if present  
**Target Platform**: Windows desktop (NGE-STUDIO)  
**Project Type**: desktop-app  
**Performance Goals**: N/A  
**Constraints**: No change to launch/persist/runner semantics (FR-007)  
**Scale/Scope**: Single widget (`param_form.py`) + minor `set_hwnd` / styles touch if needed  

## Constitution Check

PASS — Desktop Product First (UI polish); no NGE2 API change; Simplified Chinese section titles; additive QSS only.

Post-design: PASS unchanged.

## Project Structure

### Documentation (this feature)

```text
specs/007-param-form-sections/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code

```text
src/nge_studio/ui/widgets/param_form.py
src/nge_studio/ui/styles.py   # only if GroupBox title weight needs bump
src/nge_studio/ui/main_window.py  # no API change expected if set_hwnd preserved
```

## Complexity Tracking

N/A
