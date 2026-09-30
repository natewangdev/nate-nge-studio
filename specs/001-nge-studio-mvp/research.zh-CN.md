# 研究记录：NGE-STUDIO MVP 外壳

**功能**：`001-nge-studio-mvp` | **日期**：2026-09-28

> 英文权威版：[`research.md`](./research.md)。执行 Spec Kit 时忽略本中文版。

## 1. UI 工具包

- **决策**：桌面壳使用 PySide6；在 `ui/styles.py` 中采用偏科技感的现代 QSS/调色板。
- **理由**：宪章优先 PySide6；成熟的 Windows 桌面栈，信号/槽适合工作线程 runner + 实时日志。
- **备选**：CustomTkinter — 全局快捷键/窗口工具较弱；Electron/Tauri — 澄清已选 Python GUI。

## 2. 打包 / Windows exe

- **决策**：PyInstaller onefile 或 onedir（优先 **onedir**，冷启动更快、数据文件布局更简单），捆绑 `nge_studio` + `game_scripts/`。目录校验作为**前置步骤**，任一非法脚本使构建失败。
- **理由**：规格 FR-015/003；onedir 相对 onefile 更易调试、杀软误报更少。
- **备选**：Nuitka — CI 更复杂；cx_Freeze — 本地生态更少；zipapp — 非典型 Windows GUI exe 体验。

## 3. NGE2 依赖

- **决策**：在 `pyproject.toml` 声明 `nate-game-engine`。本地开发用可编辑安装；发布版钉住兼容引擎版本。
- **理由**：规格 FR-014 + 宪章 II；不内嵌。
- **备选**：git submodule 拷入树内 — 拒绝；仅 sibling 路径无 pip — 打包脆弱。

## 4. 脚本目录与校验

- **决策**：树 `game_scripts/<game_id>/<script_id>/`，必需 `manifest.json` 与导出 `run` 的 `main.py`。发现扫描两级。**任一**非法脚本目录使校验/打包失败。运行时只读已捆绑树。
- **理由**：规格 FR-002/003/016 + 澄清选项 A。
- **备选**：软跳过非法脚本 — 澄清已拒；包外插件目录 — 超出 MVP。

## 5. 统一入口与线程

- **决策**：入口 `def run(engine: NGE2, ctx: RunContext) -> None`。Runner 在 **QThread 工作线程**构造 `NGE2`、调用 `run`，`finally` 中 `close()`。UI 经 Qt 信号与 runner 通信。`RunContext` 提供线程安全的暂停/停止辅助方法。
- **理由**：规格 FR-010/011；保持 UI 响应；协作式暂停需要脚本轮询点。
- **备选**：每运行一进程 — 更重且日志/快捷键更复杂；纯 asyncio — 与阻塞式 NGE2 HID 不契合。

## 6. 暂停 / 恢复 / 结束与挂起

- **决策**：暂停置标志；脚本须调用 `wait_if_paused()` / 检查 `should_stop()`。结束置取消并 join 工作线程。**宽限期**：取消后 10 秒；若 `run` 未返回，UI 显示挂起警告 — **MVP 不强制杀进程**。Studio 超时走同一结束路径。
- **理由**：宪章 IV；澄清恢复 = 启动/F9；边界允许警告而不强制杀。
- **备选**：MVP 杀线程/进程 — 不作主路径；无限挂起无反馈 — 拒绝。

## 7. 全局快捷键

- **决策**：经 `ctypes` 使用 Win32 `RegisterHotKey` / `UnregisterHotKey`，与 Qt 消息泵集成，发射启动/暂停/结束信号。默认 F9/F10/F11。注册失败则保持上一成功绑定或未绑定，并应用内报错。
- **理由**：其他窗口前台时仍为真正全局；F 键通常无需提权。
- **备选**：`keyboard` 包 — 常需管理员；`QShortcut` — 失焦非全局；`pynput` — Windows 焦点策略下更不稳定。

## 8. 窗口点选

- **决策**：点选模式：改光标，左键用 `WindowFromPoint` 取顶层 hwnd；若属 Studio 进程（比 PID）则拒绝；UI 显示标题。MVP 不要求窗口列表兜底。
- **理由**：规格 FR-006 + 澄清禁止自身窗口。
- **备选**：仅手输 hwnd — UX 弱；仅 EnumWindows 列表 — 偏离「点选」。

## 9. 设置持久化

- **决策**：JSON 文件 `%LOCALAPPDATA%/NGE-STUDIO/settings.json`，按 `game_id/script_id` 存快捷键与每脚本上次启动参数。合并：manifest 默认 → 选中时叠加上次值；「重置默认」仅重载 manifest。
- **理由**：规格 FR-007；AppData 为 Windows 标准每用户存储。
- **备选**：SQLite — 过重；设置放 exe 旁 — 不适合 Program Files / 多用户。

## 10. 实时日志

- **决策**：自定义 `logging.Handler` 挂到根 logger `nge`（及可选 `nge_studio`），经 Qt 信号进日志面板。保留上限 **5000** 行，丢弃最旧。结束后保留至下次启动清空/替换。
- **理由**：规格 FR-013/SC-004 + 澄清日志保留；NGE2 已在 `nge` 下打日志。
- **备选**：仅轮询日志文件 — 延迟更高；无界缓冲 — UI 风险。

## 11. 操作者界面语言

- **决策**：MVP 操作者可见文案（标签、按钮、错误）使用**简体中文**。Spec Kit 文档仍双语（代理以英文为准）。
- **理由**：主维护者/操作者语言；降低 SC-001 摩擦。
- **备选**：英文 UI — 与操作者不够对齐；完整 i18n 框架 — MVP YAGNI。

## 12. 参数表面与 `ocr_kwargs`

- **决策**：规格所列面向作者的 NGE2 构造参数均提供表单字段；工厂钩子省略。`ocr_kwargs` 为 JSON 文本，启动时校验（**无**文件选择）。`hwnd` 可选。Studio 超时规范存为 `run_duration_sec`，但 **UI 以小时编辑**（空 = 禁用；允许非整数）。
- **理由**：规格 FR-005 / FR-005d + 假设；保持 settings/manifest 兼容。
- **备选**：嵌套 OCR 表单 — 延后；强制 hwnd — 澄清已拒；持久化改为小时字段 — 拒绝（选项 A 继续存秒）。

## 12b. 路径选择 UX

- **决策**：`resource_dir` / `log_dir` 文件夹选择；`yolo_model` / `yolo_names` 文件选择（建议过滤 `*.onnx`、`*.names`/`*.txt`，另有所有文件）。对话框在 `resource_dir` 存在时以其为起始，否则用户主目录。落在 `resource_dir` 下的路径存相对，否则绝对。「点选窗口」与「选择」按钮与同行输入框同高。**启动时**：相对 `resource_dir` → 脚本目录；相对 `log_dir` → 已解析 `resource_dir`（FR-005h）；`log_dir` 不得接到脚本目录。
- **理由**：规格 FR-005a–e（2026-09-28 澄清）。
- **备选**：一律绝对路径；OCR kwargs 从 JSON 文件导入 — 拒绝。

## 12c. 窗口标题解析与激活（2026-09-30）

- **决策**：增加可选 `window_title`。构造前解析 hwnd：已设 hwnd 则用之；否则 `find_by_title` 子串匹配取第一个；否则未绑定。有标题无匹配 → 启动失败。绑定构造成功后、`run` 前 `engine.window.activate()`。
- **理由**：规格 FR-005f/g。
- **备选**：精确标题匹配；找不到则降级未绑定 — 拒绝。

## 12d. 游戏级公共模块（2026-09-30）

- **决策**：可选 `game_scripts/<game_id>/common.py` 与 `rules.py`；不是目录脚本；保证脚本 `main` 可导入（游戏目录加入 `sys.path`）。demo 示范用法。
- **理由**：规格 FR-017。
- **备选**：任意游戏级 `.py`；`lib/` 子包 — 本次拒绝。

## 13. 无硬件测试

- **决策**：测试注入假引擎工厂；目录/设置/上下文纯测；可选 `@pytest.mark.qt`；硬件/HID 手工路径仅写在 quickstart。
- **理由**：宪章质量门禁 + CI 友好。
- **备选**：CI 要求真实 HID — 拒绝。
