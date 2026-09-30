# Implementation Plan: Three-Column Main Layout

**Branch**: `005-three-column-layout` | **Date**: 2026-10-01 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/005-three-column-layout/spec.md`

## Summary

Rebuild the main window as a horizontal three-pane splitter (catalog | params+controls | live logs) with default stretch **2:3:3**, and persist/restore `QSplitter` sizes via an additive `ui.main_splitter_sizes` field in the existing settings JSON.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: PySide6 (`QSplitter`), existing `SettingsStore` / `MainWindow`

**Storage**: `%LOCALAPPDATA%/NGE-STUDIO/settings.json` (additive `ui` object)

**Testing**: pytest for settings load/save/validation of splitter sizes; manual/quickstart for visual layout

**Target Platform**: Windows desktop

**Project Type**: Desktop application shell

**Performance Goals**: Debounced save on splitter move; no impact on log throughput

**Constraints**: Backward compatible settings; invalid sizes → default 2:3:3; keep brand above catalog

**Scale/Scope**: Single main window layout change

## Constitution Check

| Gate | Status |
|------|--------|
| I Desktop Product First | PASS — shell UX layout |
| II–IV Engine / catalog / runner | PASS — untouched |
| VI Tests | PASS — settings unit tests + quickstart visual check |
| VII Spec Kit bilingual | PASS — EN + zh-CN spec |

**Post-design**: PASS

## Project Structure

```text
specs/005-three-column-layout/
  plan.md, research.md, data-model.md, quickstart.md
  contracts/ui-layout-settings.md
src/nge_studio/
  settings/store.py          # AppSettings.ui + load/save
  ui/main_window.py          # three-column splitter
tests/unit/test_settings_store.py  # splitter sizes cases
```

## Complexity Tracking

> None.
