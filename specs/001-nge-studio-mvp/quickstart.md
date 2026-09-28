# Quickstart Validation: NGE-STUDIO MVP Shell

**Feature**: `001-nge-studio-mvp` | **Date**: 2026-09-28

Chinese companion: [`quickstart.zh-CN.md`](./quickstart.zh-CN.md).

Validate end-to-end after implementation. Contracts: [script-protocol.md](./contracts/script-protocol.md), [manifest-schema.md](./contracts/manifest-schema.md), [settings-store.md](./contracts/settings-store.md). Model: [data-model.md](./data-model.md).

## Prerequisites

- Windows 10/11, Python 3.11+
- Local checkout of this repo
- Nearby or published `nate-game-engine` installable via pip/editable
- (Optional hardware path) ESP32-S3 HID available for a full NGE2 construct

## Setup

```powershell
cd <repo-root>
uv sync --extra dev
# Editable engine example (adjust path):
# uv pip install -e ..\nate-game-engine
```

## Automated validation (CI / no hardware)

```powershell
uv run python scripts/validate_catalog.py
uv run pytest -q
uv run ruff check src tests
```

**Expected**:

- Catalog validate exits 0 with the sample `demo/smoke` tree
- Introducing a broken script folder (missing `manifest.json`) makes validate exit non-zero naming the path
- Unit/contract tests pass with fake engine (single-flight refuse, pause/stop context, settings round-trip, merge defaults)

## Manual UI validation (developer run)

```powershell
uv run python -m nge_studio
```

**Expected**:

1. Main window opens (Simplified Chinese labels); catalog shows **冒烟示例** (or `smoke`) under `demo`.
2. Select script → form shows manifest defaults; `hwnd` may be empty; Start still enabled.
3. Window pick: clicking Studio itself is rejected with a prompt; picking another top-level window fills hwnd + title.
4. With fake/mock or real engine per environment: Start → logs appear live; Pause halts progress; Start/F9 resumes; Stop returns idle and keeps log lines; Start again clears/replaces logs.
5. Change hotkeys in settings, restart app → new bindings work; defaults were F9/F10/F11.
6. Second Start while running is refused with a clear message.

## Packaging validation

```powershell
uv run python scripts/validate_catalog.py
# Documented PyInstaller command from README / packaging notes, e.g.:
# uv run pyinstaller --noconfirm packaging/nge-studio.spec
```

**Expected**:

- Artifact under `dist/` launches without a system Python install step for the operator
- Catalog matches the packaged `game_scripts` tree
- Validate failure blocks packaging when an invalid script is present

## Done when

- [ ] `validate_catalog` + `pytest` + `ruff` green
- [ ] Manual UI checklist above observed
- [ ] Packaged exe opens and shows packaged catalog
- [ ] Bilingual Spec Kit artifacts for this feature remain paired
