# 任务列表：NGE-STUDIO MVP 外壳

**输入**：`/specs/001-nge-studio-mvp/` 设计文档

**前置**：plan.md、spec.md、research.md、data-model.md、contracts/、quickstart.md

**测试**：包含 — 计划完成定义要求目录、runner、设置的自动化测试（假引擎；CI 无 HID）。

**组织**：按用户故事分组，便于独立实现与测试。

> 英文权威版：[`tasks.md`](./tasks.md)。执行 Spec Kit 时忽略本中文版。

## 格式：`[ID] [P?] [Story] Description`

- **[P]**：可并行
- **[Story]**：用户故事标签（`[US1]`…`[US5]`）
- 描述含确切文件路径

任务正文与勾选状态以英文版为准；实现过程中须同步更新本文件勾选，保持信息等价。

## Phase 1: 搭建

- [x] T001 按计划创建 `src/nge_studio/` 包目录与 `__init__.py`
- [x] T002 [P] 创建 `tests/unit|contract|integration/`
- [x] T003 创建 `pyproject.toml`（`nate-nge-studio` / `nge_studio` / PySide6 / nge2 / 入口）
- [x] T004 [P] 添加 Python `.gitignore`
- [x] T005 [P] 编写中文为主的 `README.md`

## Phase 2: 基础

- [x] T006 `catalog/models.py` 数据类与合并规则
- [x] T007 [P] `runner/context.py` RunContext / ScriptStopped
- [x] T008 [P] `settings/store.py` AppData JSON
- [x] T009 [P] `logging_bridge/qt_handler.py`
- [x] T010 runner 骨架 `service.py` + `loader.py`
- [x] T011 `__init__.py` / `__main__.py` / `app.py` 空壳主窗
- [x] T012 [P] `tests/unit/test_run_context.py`
- [x] T013 [P] `tests/unit/test_settings_store.py`

## Phase 3: US1 目录浏览

- [x] T014 [P] [US1] `tests/unit/test_catalog.py`
- [x] T015 [US1] `catalog/validate.py`
- [x] T016 [US1] `catalog/discover.py`
- [x] T017 [US1] `scripts/validate_catalog.py`
- [x] T018 [US1] `game_scripts/demo/smoke/` 样例
- [x] T019 [US1] 目录面板 UI
- [x] T020 [US1] 启动加载目录 + `styles.py`

## Phase 4: US2 参数与窗口点选

- [x] T021 [P] [US2] `tests/unit/test_launch_merge.py`
- [x] T022 [P] [US2] `tests/unit/test_window_pick.py`
- [x] T023 [US2] `ui/widgets/param_form.py`
- [x] T024 [US2] `window_pick/picker.py`
- [x] T025 [US2] 表单与设置持久化接线
- [x] T026 [US2] 启动前参数校验

## Phase 5: US3 启停与快捷键

- [x] T027 [P] [US3] `tests/integration/test_runner.py`
- [x] T028 [US3] `runner/loader.py`
- [x] T029 [US3] `runner/service.py` 完整生命周期
- [x] T030 [US3] `runner/engine_factory.py`
- [x] T031 [US3] `hotkeys/win32.py`
- [x] T032 [US3] 主窗控制与快捷键接线
- [x] T033 [US3] Studio 超时
- [x] T034 [US3] 完善 `demo/smoke/main.py`

## Phase 6: US4 实时日志

- [x] T035 [US4] `ui/widgets/log_panel.py`
- [x] T036 [US4] 日志 handler 接线
- [x] T037 [P] [US4] `tests/unit/test_log_buffer.py`

## Phase 7: US5 打包 exe

- [x] T038 [US5] `packaging/nge-studio.spec`
- [x] T039 [US5] README 打包说明 + frozen 路径
- [x] T040 [US5] 校验失败阻断打包说明

## Phase 8: 收尾

- [x] T041 [P] README 协议/快捷键补充
- [x] T042 pytest + ruff
- [x] T043 quickstart 冒烟
- [x] T044 [P] 同步 `tasks.zh-CN.md` 勾选

## 建议 MVP

先完成 Phase 1–3（目录 + 校验），再增量 US2→US5。
