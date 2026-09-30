# Research: App Icon & Game Display Name

**Feature**: `004-icon-game-display` | **Date**: 2026-09-30

## R1 — Product icon asset & wiring

- **Decision**: Store a multi-size Windows `.ico` at `assets/icons/app.ico` (plus optional PNG source). Set `QApplication` / main window icon via `QIcon` at startup. Pass the same `.ico` to PyInstaller `EXE(..., icon=...)`. Resolve path with a small helper that checks repo-relative path in dev and `_MEIPASS` / beside-exe datas in frozen builds; **bundle the ico in `datas`** so runtime can load it, and also set EXE icon for Explorer.
- **Rationale**: Spec requires window + taskbar + packaged exe to share one script-themed mark. Qt needs a loadable file at runtime; Explorer needs the PE icon resource.
- **Alternatives considered**: PNG-only (weaker Explorer branding); system theme icons (not product-branded); per-build generated icon (harder to review).

## R2 — Missing icon failure mode

- **Decision**: Packaging spec / startup helper treats missing `assets/icons/app.ico` as a hard error for frozen runs and for packaging (path must exist when building). Dev may surface a clear error if asset is absent after the feature lands (no silent generic icon in the intended ship path).
- **Rationale**: Spec edge case forbids silent generic-icon releases.
- **Alternatives considered**: Soft warn + default Qt icon (rejected by FR).

## R3 — Game-level `manifest.json`

- **Decision**: Optional file `game_scripts/<game_id>/manifest.json`. Allowed top-level keys only: `display_name`, `description` (both optional strings). No `defaults`. Missing file → OK. Present but invalid → `CatalogValidationError` hard-fail. UI label = stripped `display_name` or `game_id`.
- **Rationale**: Matches clarification Q2/Q3 and mirrors script naming while keeping launch defaults script-only. Same filename as scripts but different path level; discovery already only treats *directories* as scripts.
- **Alternatives considered**: `game.json` (clearer name, rejected by product choice A); required file (rejected by Q3 A).

## R4 — Model shape

- **Decision**: Add `GameManifest` (or reuse a slim metadata dataclass) on `Game`; expose `Game.display_name` property analogous to `Script.display_name`. Do not change settings keys (`game_id/script_id`).
- **Rationale**: Minimal delta to existing catalog models; keeps identity stable (FR-010).
- **Alternatives considered**: Overloading script `Manifest` with unused `defaults` on games (confusing).

## R5 — Sample content

- **Decision**: Add readable Chinese/English display names for in-repo `demo` and `diablo4` game manifests as content examples.
- **Rationale**: Makes US2 independently demonstrable in quickstart.
- **Alternatives considered**: Leave samples without names (weaker demo).
