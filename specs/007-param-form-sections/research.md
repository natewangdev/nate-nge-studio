# Research: 007 Param Form Sections

## R1 — Section containers

- **Decision**: Use `QGroupBox("启动参数")` / `QGroupBox("脚本参数")` with existing `APP_QSS` `QGroupBox` / `QGroupBox::title` (cyan title vs normal field labels).
- **Rationale**: Matches clarify Option A; QSS already present from earlier chrome.
- **Alternatives**: Custom QFrame + QLabel heading — more code, weaker native title-on-border affordance.

## R2 — hwnd title after pick

- **Decision**: Remove `hwnd_title` hint row entirely; `set_hwnd` / `set_parameters` only set `hwnd` + `window_title`.
- **Rationale**: Spec FR-005; avoids duplicate title under hwnd while keeping 001 fill of `window_title`.
- **Alternatives**: Status-bar flash only — rejected (Option A keeps field fill).

## R3 — humanize row

- **Decision**: `form.addRow("拟人化移动", QCheckBox())` with empty checkbox text (or `setText("")`).
- **Rationale**: Aligns with QFormLayout label column used by other rows.
- **Alternatives**: Keep checkbox caption — rejected by spec FR-006.

## R4 — script group visibility

- **Decision**: Keep current hide-when-no-fields behavior; put dynamic script form layout inside the script `QGroupBox`.
- **Rationale**: Matches FR-003 and 006 empty-schema behavior.
