# Quickstart: 007 Param Form Sections

## Automated

```powershell
uv run pytest tests/unit -q --tb=line
uv run ruff check src/nge_studio/ui/widgets/param_form.py src/nge_studio/ui/styles.py
```

## Manual

1. Launch Studio; select **demo / 冒烟示例** → only **启动参数** group; no **脚本参数**.
2. Select **demo / 控制参数示例** → both groups; group titles visually distinct from field labels.
3. Point-pick a window → hwnd filled; **窗口标题** filled; nothing under hwnd row.
4. Confirm **拟人化移动** label on the left, empty checkbox on the right.
5. Reset defaults still works; Start still runs unchanged.
