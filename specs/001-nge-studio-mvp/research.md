# Research: NGE-STUDIO MVP Shell

**Feature**: `001-nge-studio-mvp` | **Date**: 2026-09-28

Chinese companion: [`research.zh-CN.md`](./research.zh-CN.md).

## 1. UI toolkit

- **Decision**: PySide6 (Qt for Python) for the desktop shell; modern tech-oriented QSS/palette in `ui/styles.py`.
- **Rationale**: Constitution prefers PySide6; mature Windows desktop stacking, signals/slots fit worker-thread runner + live logs.
- **Alternatives considered**: CustomTkinter — weaker global-hotkey/window tooling; Electron/Tauri — rejected by clarify (Python GUI).

## 2. Packaging / Windows exe

- **Decision**: PyInstaller onefile or onedir (prefer **onedir** for faster cold start and simpler data-file layout) bundling `nge_studio` + `game_scripts/`. Catalog validation runs as a **pre-step** that fails the build on any invalid script.
- **Rationale**: Spec FR-015/003; onedir reduces antivirus false positives and eases debugging vs onefile.
- **Alternatives considered**: Nuitka — more complex CI; cx_Freeze — less common locally; zipapp — not a true Windows GUI exe UX.

## 3. NGE2 dependency

- **Decision**: Declare `nate-game-engine` in `pyproject.toml`. Local dev uses editable install (`uv add --editable ../nate-game-engine` or documented path). Released Studio pins a compatible engine version.
- **Rationale**: Spec FR-014 + constitution II; no vendoring.
- **Alternatives considered**: Git submodule copy into tree — rejected; sibling-path-only without pip — brittle for packaging.

## 4. Script catalog & validation

- **Decision**: Tree `game_scripts/<game_id>/<script_id>/` with required `manifest.json` and `main.py` exporting `run`. Discovery walks two levels. **Any** invalid discovered script directory fails validate/package (exit non-zero, path in message). Runtime catalog reads the bundled tree only (same rules); does not scan arbitrary external folders after ship.
- **Rationale**: Spec FR-002/003/016 + clarify Option A.
- **Alternatives considered**: Soft-skip invalid scripts — rejected in clarify; plugin folders outside the package — out of MVP scope.

## 5. Unified script entry & threading

- **Decision**: Entry `def run(engine: NGE2, ctx: RunContext) -> None` in `main.py`. Runner constructs `NGE2` on a **dedicated worker thread (QThread)**, calls `run`, then `engine.close()` in `finally`. UI talks to runner via Qt signals. `RunContext` exposes thread-safe `is_paused()`, `wait_if_paused()`, `should_stop()`, `checkpoint()` helpers.
- **Rationale**: Spec FR-010/011; keeps Qt UI responsive; cooperative pause needs polling points in scripts.
- **Alternatives considered**: Multiprocess per run — heavier and complicates log/hotkey; asyncio-only — poor fit with blocking NGE2 HID calls.

## 6. Pause / resume / stop & hung scripts

- **Decision**: Pause sets a flag; scripts must call `wait_if_paused()` / check `should_stop()` in loops. Stop sets cancel then joins the worker. **Grace period**: 10 seconds after cancel; if `run` has not returned, UI shows hung-script warning and leaves Stop disabled until join completes or process exit — **no force-kill in MVP**. Studio timeout uses the same stop path.
- **Rationale**: Constitution IV (cooperative primary); clarify resume = Start/F9; edge case allows warn without requiring kill.
- **Alternatives considered**: Thread kill / process kill in MVP — rejected as primary path; indefinite hang with no UI feedback — rejected.

## 7. Global hotkeys

- **Decision**: Win32 `RegisterHotKey` / `UnregisterHotKey` via `ctypes`, message pump integrated with Qt (`nativeEvent` / dedicated listener), emit Qt signals for Start/Pause/Stop. Defaults F9/F10/F11. Persist bindings; on registration failure, keep previous successful binding or unbound and show in-app error.
- **Rationale**: True global hotkeys while another window is focused; F-keys generally work without elevation.
- **Alternatives considered**: `keyboard` package — often needs admin; Qt `QShortcut` — not global when unfocused; `pynput` — less predictable on Windows focus policies.

## 8. Window picker

- **Decision**: Point-and-pick mode: change cursor, on left-click use `WindowFromPoint` / ancestor top-level hwnd; reject if hwnd belongs to the Studio process (compare PID); show title in UI. Optional list fallback is not required for MVP.
- **Rationale**: Spec FR-006 + clarify disallow self-window.
- **Alternatives considered**: Manual hwnd hex only — weaker UX; always-on EnumWindows list only — diverges from “点选”.

## 9. Settings persistence

- **Decision**: JSON file `%LOCALAPPDATA%/NGE-STUDIO/settings.json` storing hotkeys and per-script last-used launch params keyed by `game_id/script_id`. Merge: manifest defaults → last-used overlay on select; explicit “reset to defaults” reloads manifest only.
- **Rationale**: Spec FR-007; AppData is the Windows-standard per-user store.
- **Alternatives considered**: SQLite — overkill; settings next to exe — breaks for Program Files installs / multi-user.

## 10. Live logs

- **Decision**: Custom `logging.Handler` attached to root logger `nge` (and optionally `nge_studio`) that emits Qt signals to the log panel. Cap retained lines at **5000**; drop oldest. Retain after stop until next Start clears/replaces.
- **Rationale**: Spec FR-013/SC-004 + clarify log retention; NGE2 already logs under `nge`.
- **Alternatives considered**: Polling log files only — higher latency; unbounded buffer — UI risk.

## 11. Operator UI language

- **Decision**: MVP operator-facing strings (labels, buttons, errors) in **Simplified Chinese**. Spec Kit docs remain bilingual (EN authoritative for agents).
- **Rationale**: Primary maintainer/operator language; reduces friction for SC-001.
- **Alternatives considered**: English UI — less aligned with operator; full i18n framework — YAGNI for MVP.

## 12. Parameter surface & `ocr_kwargs`

- **Decision**: Form fields for all author-facing NGE2 ctor params listed in the spec; factory hooks omitted. `ocr_kwargs` as JSON text field validated on Start (**no** file browse). `hwnd` optional. Studio timeout is stored as `run_duration_sec` but **edited in the UI as hours** (empty = disabled; non-integers allowed).
- **Rationale**: Spec FR-005 / FR-005d + assumptions; keeps settings/manifest backward compatible.
- **Alternatives considered**: Nested OCR form — deferred; require hwnd — rejected in clarify; rename persist field to hours — rejected (Option A keep seconds).

## 12b. Path browse UX

- **Decision**: Folder browse for `resource_dir` and `log_dir`; file browse for `yolo_model` / `yolo_names` with suggested filters (`*.onnx`, `*.names`/`*.txt`, plus All files). Dialogs start at `resource_dir` when it exists, else user home. Picked paths under `resource_dir` are stored relative; otherwise absolute. Window-pick and Browse buttons match adjacent input height.
- **Rationale**: Spec FR-005a–e clarifications (2026-09-28).
- **Alternatives considered**: Always absolute paths; OCR kwargs JSON file import — rejected.

## 13. Testing without hardware

- **Decision**: Inject a fake engine factory in tests; catalog/settings/context tests pure; optional `@pytest.mark.qt` for widget smokes; hardware/HID manual path documented in quickstart only.
- **Rationale**: Constitution quality gates + CI friendliness.
- **Alternatives considered**: Require real HID in CI — rejected.
