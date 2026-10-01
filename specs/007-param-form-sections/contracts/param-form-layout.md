# Contract: Param Form Layout (UI)

**Feature**: `007-param-form-sections`

## Center column parameter form

```text
┌─ 启动参数 ─────────────────────────┐
│ label | control (QFormLayout)      │
│ … hwnd row (no under-title hint)   │
│ 拟人化移动 | [ ]  (checkbox no text) │
│ … duration / duration_end_action   │
└────────────────────────────────────┘
┌─ 脚本参数 ─────────────────────────┐  (omit if no script_params)
│ dynamic fields                     │
└────────────────────────────────────┘
[ 重置为默认 ]   (outside groups)
```

## Window pick result mapping

| Field | After successful pick |
|-------|------------------------|
| `hwnd` | Set to picked handle |
| `window_title` | Set to picked title |
| Under-hwnd hint | **Absent** |

## Labels

| UI string | Role |
|-----------|------|
| 启动参数 | GroupBox title |
| 脚本参数 | GroupBox title |
| 拟人化移动 | Form field label (not checkbox caption) |
