# 快速验证指南：NGE-STUDIO MVP 外壳

**功能**：`001-nge-studio-mvp` | **日期**：2026-09-28

> 英文权威版：[`quickstart.md`](./quickstart.md)。执行 Spec Kit 时忽略本中文版。

实现完成后做端到端验证。契约：[script-protocol.md](./contracts/script-protocol.md)、[manifest-schema.md](./contracts/manifest-schema.md)、[settings-store.md](./contracts/settings-store.md)。模型：[data-model.md](./data-model.md)。

## 前置条件

- Windows 10/11，Python 3.11+
- 本仓库本地检出
- 可通过 pip/可编辑安装的邻近或已发布 `nate-game-engine`
- （可选硬件路径）可用的 ESP32-S3 HID，以完整构造 NGE2

## 安装

```powershell
cd <repo-root>
uv sync --extra dev
# 可编辑引擎示例（按路径调整）：
# uv pip install -e ..\nate-game-engine
```

## 自动化验证（CI / 无硬件）

```powershell
uv run python scripts/validate_catalog.py
uv run pytest -q
uv run ruff check src tests
```

**期望**：

- 样例 `demo/smoke` 树下目录校验退出码 0
- 引入损坏脚本目录（缺 `manifest.json`）时校验非 0 退出并指明路径
- 使用假引擎的单元/契约测试通过（单实例拒绝、暂停/结束上下文、设置往返、默认合并）

## 手工 UI 验证（开发态运行）

```powershell
uv run python -m nge_studio
```

**期望**：

1. 主窗口打开（简体中文文案）；目录在 `demo` 下显示 **冒烟示例**（或 `smoke`）。
2. 选中脚本 → 表单显示 manifest 默认；`hwnd` 可为空；启动仍可用；运行时长单位为**小时**。
3. 窗口点选：点到 Studio 自身被拒绝并提示；点选其他顶层窗口填入 hwnd + 标题；点选按钮高度与 hwnd 输入框一致。
4. 选择：`resource_dir` / `log_dir` 选文件夹；YOLO 模型/names 选文件（起始于 `resource_dir` 或主目录）；落在资源目录下写相对路径；`ocr_kwargs` 无选择按钮。
5. 按环境用假/真引擎：启动 → 日志实时出现；暂停停下进展；启动/F9 恢复；结束后回空闲并保留日志；再次启动清空/替换日志。
6. 在设置中改快捷键，重启应用 → 新绑定生效；默认曾为 F9/F10/F11。
7. 运行中第二次启动被拒绝并给出清晰说明。

## 打包验证

```powershell
uv run python scripts/validate_catalog.py
# README / 打包说明中的 PyInstaller 命令，例如：
# uv run pyinstaller --noconfirm packaging/nge-studio.spec
```

**期望**：

- `dist/` 下产物无需操作者再装系统 Python 即可启动
- 目录与已打包 `game_scripts` 树一致
- 存在非法脚本时校验失败并阻断打包

## 完成条件

- [ ] `validate_catalog` + `pytest` + `ruff` 通过
- [ ] 上述手工 UI 清单已观察到
- [ ] 打包 exe 能打开并显示已打包目录
- [ ] 本功能双语 Spec Kit 产物保持成对
