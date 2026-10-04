# 任务：目录排序

**输入**：`/specs/008-catalog-sort-order/` 下的设计文档

**前提**：plan.md、spec.md、research.md、data-model.md、contracts/sort-order.md

**测试**：包含 — 宪章对目录逻辑的质量门禁（`tests/unit/test_catalog.py` 中的 pytest）。

> 英文权威版：[tasks.md](./tasks.md)。执行 Spec Kit 时忽略本中文版。

## 阶段 1：准备

- [x] T001 确认 `specs/008-catalog-sort-order/` 文档及既有 `src/nge_studio/catalog/models.py`、`validate.py`、`discover.py`

## 阶段 2：基础

- [x] T002 在 `src/nge_studio/catalog/models.py` 的 `Manifest` 与 `GameManifest` 上增加可选 `sort_order: int | None = None`（可选；出现时必须为 JSON 整数；允许 0 与负数）
- [x] T003 将 `sort_order` 加入 `_MANIFEST_TOP` 与 `_GAME_MANIFEST_TOP`；在 `src/nge_studio/catalog/validate.py` 用 `isinstance(value, int) and not isinstance(value, bool)` 解析（拒绝浮点、布尔、字符串、null、数组、对象）；未知键仍失败

## 阶段 3：用户故事 1 - 维护者声明的目录顺序（P1）🎯 MVP

**目标**：左栏目录中游戏与脚本遵循显式 `sort_order`、再省略项、再文件夹 ID 并列；操作者不能改序。

**独立测试**：`pytest tests/unit/test_catalog.py -q`；打开 Studio 确认树顺序与发现一致且无拖拽/上下控件。

- [x] T004 [US1] 在 `src/nge_studio/catalog/discover.py` 的 `discover_catalog` 中排序：显式 `sort_order` 升序在前；省略在后；并列按 `game_id`/`script_id` 字典序；脚本顺序按游戏隔离
- [x] T005 [US1] 确认 `src/nge_studio/ui/widgets/catalog_panel.py` 的 `CatalogPanel.set_games` 按列表顺序插入且无改序控件
- [x] T006 [US1] 在 `tests/unit/test_catalog.py` 增加单元测试：显式/省略混排；相同 `sort_order` 按 ID 并列；缺字段合法；浮点/布尔/`null` 整次校验失败且含路径；未知键仍失败
- [x] T007 [P] [US1] 在 `specs/001-nge-studio-mvp/contracts/manifest-schema.md` 与 `manifest-schema.zh-CN.md` 记录脚本 `sort_order`
- [x] T008 [P] [US1] 在 `specs/004-icon-game-display/contracts/game-manifest-schema.md` 记录游戏 `sort_order`（若缺双语则补 `game-manifest-schema.zh-CN.md`）
- [x] T009 [P] [US1] 可选：在仓库 `game_scripts/**/manifest.json` 写入样例 `sort_order`，使作者顺序可与文件夹名顺序不同

## 阶段 4：收尾

- [x] T010 运行 `pytest tests/unit/test_catalog.py` 及已配置的 ruff；执行 [quickstart.md](./quickstart.md) 自动化检查

## 依赖与执行顺序

- 阶段 1 → 阶段 2（T002–T003）→ 阶段 3 US1（T004–T009；T006 后 T007–T009 可并行）→ 阶段 4
- 仅一个故事；MVP 即 US1
