# Implementation Plan: NGE-STUDIO MVP Shell

**Branch**: `001-nge-studio-mvp` | **Date**: 2026-09-28 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-nge-studio-mvp/spec.md`

Chinese companion (human-readable only): [`plan.zh-CN.md`](./plan.zh-CN.md).

## Summary

Build **NGE-STUDIO** as a Windows desktop app (PySide6) that discovers a packaged
`game_scripts/` catalog, lets an operator configure full NGE2 launch parameters (plus
Studio run-duration timeout), pick a target window, and run exactly one script at a time
with cooperative pause/stop, global hotkeys, and live logs. Scripts implement a unified
`run(engine, ctx)` protocol. Ship via PyInstaller exe embedding the catalog; invalid
scripts fail the package/validate step hard.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: `PySide6` (UI); `nate-game-engine` / `nge2` (pip, editable local
and/or published); stdlib `logging` + Qt signal bridge; Win32 via `ctypes` for global
hotkeys (`RegisterHotKey`) and window pick (`WindowFromPoint` / `EnumWindows`);
`PyInstaller` (dev/release packaging, not a runtime dep of the installed library layout)

**Storage**: Local JSON settings under `%LOCALAPPDATA%/NGE-STUDIO/` (per-script launch
config + hotkey bindings). No database.

**Testing**: `pytest` + `pytest-qt` for UI-adjacent tests where practical; unit tests for
catalog validation, settings, run-context, runner single-flight; fake/mock NGE2 for CI
without HID hardware

**Target Platform**: Windows 10/11 desktop (primary; other OS out of scope)

**Project Type**: Desktop application (`src/nge_studio/` + `game_scripts/` + packaging
recipe); import package `nge_studio`; distribution name `nate-nge-studio`

**Performance Goals**: Align with spec SC-003/SC-004 — pause observable ≤2s; normal stop
to idle ≤5s; log panel perceived lag &lt;1s at ≥1 line/s; cold UI open usable within a few
seconds on a typical developer machine

**Constraints**: Single active run; cooperative lifecycle only (no force-kill in MVP);
build-time catalog (no post-ship external hot-scan); disallow picking Studio’s own hwnd;
fail packaging on invalid scripts; Chinese operator-facing UI strings for MVP

**Scale/Scope**: One main window (catalog + params + controls + log); sample demo script(s);
~1 product package + packaging/validate CLI entry

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| I. Desktop product first | PASS | Primary deliverable is PySide6 app + exe |
| II. NGE2 sole engine via pip | PASS | Dependency on `nate-game-engine`; no vendored engine |
| III. Packaged script catalog | PASS | `game_scripts/`; validate fails hard; rebuild to add scripts |
| IV. Cooperative + single runner | PASS | `RunContext` + single-flight runner; grace warn only |
| V. Observability & hotkeys | PASS | Live log bridge; F9/F10/F11 defaults; persisted bindings |
| VI–VII. Bilingual artifacts | PASS | All Spec Kit Markdown for this feature paired EN+zh-CN |
| Platform: Windows / PySide6 / exe / py≥3.11 | PASS | Documented in Technical Context + research |

**Post-design re-check**: PASS — contracts cover script protocol, manifest, settings;
structure keeps UI vs orchestration separable; no constitution violations requiring
Complexity Tracking.

## Project Structure

### Documentation (this feature)

```text
specs/001-nge-studio-mvp/
├── plan.md
├── plan.zh-CN.md
├── research.md
├── research.zh-CN.md
├── data-model.md
├── data-model.zh-CN.md
├── quickstart.md
├── quickstart.zh-CN.md
├── contracts/
│   ├── script-protocol.md
│   ├── script-protocol.zh-CN.md
│   ├── manifest-schema.md
│   ├── manifest-schema.zh-CN.md
│   ├── settings-store.md
│   └── settings-store.zh-CN.md
├── checklists/
│   ├── requirements.md
│   └── requirements.zh-CN.md
└── tasks.md                 # (/speckit-tasks — not this command)
```

### Source Code (repository root)

```text
src/nge_studio/
├── __init__.py              # package version export
├── __main__.py              # python -m nge_studio
├── app.py                   # QApplication bootstrap, main window wiring
├── catalog/
│   ├── __init__.py
│   ├── discover.py          # scan game_scripts tree
│   ├── validate.py          # hard-fail rules (shared by CLI + packaging)
│   └── models.py            # Game/Script/Manifest dataclasses
├── runner/
│   ├── __init__.py
│   ├── context.py           # RunContext: pause / cancel signals
│   ├── loader.py            # import script entry `run`
│   └── service.py           # single-flight start/pause/resume/stop + timeout
├── settings/
│   ├── __init__.py
│   └── store.py             # JSON load/save under LOCALAPPDATA
├── hotkeys/
│   └── win32.py             # RegisterHotKey / UnregisterHotKey bridge → Qt signals
├── window_pick/
│   └── picker.py            # point-and-pick; reject Studio hwnd
├── logging_bridge/
│   └── qt_handler.py        # logging.Handler → Qt signal for live panel
└── ui/
    ├── main_window.py       # catalog, params form, controls, log panel
    ├── styles.py            # modern tech-oriented palette / QSS
    └── widgets/             # parameter editors, window-pick button, etc.

game_scripts/
└── demo/
    └── smoke/
        ├── manifest.json
        └── main.py          # compliant sample `run(engine, ctx)`

tests/
├── unit/                    # catalog, manifest, context, settings merge
├── contract/                # protocol/manifest schema fixtures
└── integration/             # runner with fake engine; optional pytest-qt smokes

scripts/
└── validate_catalog.py      # CLI used by packaging / CI (or `nge-studio-validate` entry)

pyproject.toml               # name nate-nge-studio; package nge_studio; deps; entry points
# packaging recipe documented in quickstart (PyInstaller spec or documented command)
```

**Structure Decision**: Single desktop app package under `src/nge_studio/` with non-UI
domains (`catalog`, `runner`, `settings`, `hotkeys`, `window_pick`, `logging_bridge`)
separated from `ui/`. Scripts live in repo-root `game_scripts/` and are bundled into the
exe at package time. No frontend/backend split.

## Complexity Tracking

> No constitution violations requiring justification.

## Definition of Done (plan-level)

- Catalog discover + validate hard-fail covered by automated tests
- Runner single-flight, pause/resume/stop, and Studio timeout covered with fake engine
- Settings round-trip (launch params + hotkeys) tested
- At least one compliant sample script under `game_scripts/demo/smoke`
- Documented PyInstaller (or equivalent) command produces an exe that shows the packaged catalog
- `ruff` + `pytest` pass when configured; UI smoke path described in [quickstart.md](./quickstart.md)
- Bilingual Spec Kit artifacts for this feature kept in sync
