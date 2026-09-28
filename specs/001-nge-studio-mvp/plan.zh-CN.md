# 实现计划：NGE-STUDIO MVP 外壳

**分支**：`001-nge-studio-mvp` | **日期**：2026-09-28 | **规格**：[spec.md](./spec.md)

**输入**：来自 `/specs/001-nge-studio-mvp/spec.md` 的功能规格

> 英文权威版：[`plan.md`](./plan.md)。执行 Spec Kit 时忽略本中文版。

## 摘要

将 **NGE-STUDIO** 建成 Windows 桌面应用（PySide6）：发现已打包的 `game_scripts/` 目录，
允许操作者配置完整 NGE2 启动参数（外加 Studio 运行时长超时）、点选目标窗口，并以协作式
暂停/结束、全局快捷键与实时日志**同一时间只运行一个**脚本。脚本实现统一
`run(engine, ctx)` 协议。通过 PyInstaller 打成嵌入目录的 exe；非法脚本使打包/校验步骤硬失败。

## 技术上下文

**语言/版本**：Python 3.11+

**主要依赖**：`PySide6`（UI）；`nate-game-engine` / `nge2`（pip，可编辑本地和/或已发布）；
标准库 `logging` + Qt 信号桥；`ctypes` Win32 全局快捷键（`RegisterHotKey`）与窗口点选
（`WindowFromPoint` / `EnumWindows`）；`PyInstaller`（开发/发布打包，非运行时库依赖）

**存储**：`%LOCALAPPDATA%/NGE-STUDIO/` 下本地 JSON（每脚本启动配置 + 快捷键绑定）。无数据库。

**测试**：`pytest` + 可行处 `pytest-qt`；目录校验、设置、运行上下文、单实例 runner 的单元测试；
CI 使用假/mock NGE2，无需 HID 硬件

**目标平台**：Windows 10/11 桌面（主目标；其他 OS 不在范围）

**项目类型**：桌面应用（`src/nge_studio/` + `game_scripts/` + 打包配方）；import 包名
`nge_studio`；分发名 `nate-nge-studio`

**性能目标**：对齐规格 SC-003/SC-004 — 暂停可观察 ≤2s；正常结束回空闲 ≤5s；≥1 行/秒时日志
面板感知延迟 &lt;1s；典型开发机冷启动 UI 数秒内可用

**约束**：单活动运行；仅协作式生命周期（MVP 不强制杀进程）；构建时目录（发版后不热扫外部）；
禁止点选 Studio 自身 hwnd；非法脚本打包失败；MVP 操作者界面文案使用简体中文

**规模/范围**：一个主窗口（目录 + 参数 + 控制 + 日志）；样例演示脚本；约一个产品包 +
打包/校验 CLI 入口

## 宪章检查

*门禁：Phase 0 研究前必须通过。Phase 1 设计后复查。*

| 门禁 | 状态 | 说明 |
|------|------|------|
| I. 桌面产品优先 | PASS | 首要交付物为 PySide6 应用 + exe |
| II. 唯一引擎 NGE2 经 pip | PASS | 依赖 `nate-game-engine`；不内嵌引擎 |
| III. 打包时脚本目录 | PASS | `game_scripts/`；校验硬失败；新增需重建 |
| IV. 协作式 + 单实例 | PASS | `RunContext` + 单航班 runner；仅宽限警告 |
| V. 可观测性与快捷键 | PASS | 实时日志桥；默认 F9/F10/F11；绑定持久化 |
| VI–VII. 双语产物 | PASS | 本功能全部 Spec Kit Markdown 英中成对 |
| 平台：Windows / PySide6 / exe / py≥3.11 | PASS | 见技术上下文与 research |

**设计后复查**：PASS — 契约覆盖脚本协议、manifest、设置；结构保持 UI 与编排可分离；无需要
Complexity Tracking 的宪章违规。

## 项目结构

### 文档（本功能）

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
└── tasks.md                 # (/speckit-tasks — 非本命令)
```

### 源码（仓库根）

```text
src/nge_studio/
├── __init__.py
├── __main__.py
├── app.py
├── catalog/
├── runner/
├── settings/
├── hotkeys/
├── window_pick/
├── logging_bridge/
└── ui/

game_scripts/
└── demo/smoke/   # manifest.json + main.py

tests/
scripts/validate_catalog.py
pyproject.toml
```

**结构决策**：单一桌面应用包 `src/nge_studio/`，非 UI 领域与 `ui/` 分离。脚本位于仓库根
`game_scripts/`，打包时打入 exe。不做前后端拆分。

## 复杂度跟踪

> 无需要正当化的宪章违规。

## 完成定义（计划级）

- 目录发现 + 校验硬失败有自动化测试
- Runner 单实例、暂停/恢复/结束、Studio 超时用假引擎覆盖
- 设置往返（启动参数 + 快捷键）有测试
- `game_scripts/demo/smoke` 至少一个合规样例脚本
- 文档化的 PyInstaller（或等价）命令能产出 exe 并显示已打包目录
- 已配置时 `ruff` + `pytest` 通过；UI 冒烟路径见 [quickstart.md](./quickstart.md)
- 本功能双语 Spec Kit 产物保持同步
