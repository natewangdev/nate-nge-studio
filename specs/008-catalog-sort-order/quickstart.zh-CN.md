# 快速开始：目录排序

**功能**：`008-catalog-sort-order`

> 英文权威版：[quickstart.md](./quickstart.md)。执行 Spec Kit 时忽略本中文版。

## 前提

- 含 `game_scripts/` 的仓库检出，以及本项目使用的 pytest 环境。

## 自动化检查

在仓库根目录：

```text
pytest tests/unit/test_catalog.py -q
```

期望：未知键仍硬失败；`sort_order` 接受整数；浮点/布尔失败；`discover_catalog` 顺序符合 [data-model.md](./data-model.md)（显式在前、省略在后、并列按文件夹 ID）。

## 手动 UI 检查（可选）

1. 给两个游戏写与文件夹名顺序不一致的 `sort_order`；运行 Studio。
2. 左栏游戏分组跟随 `sort_order`，而非文件夹名。
3. 确认目录树没有拖拽或上下按钮。
4. 选中脚本；启动设置键仍为 `game_id/script_id`。

## 顺序样例（概念）

- 游戏 `z_game` `sort_order`: 1  
- 游戏 `a_game` 省略  
→ `z_game` 出现在 `a_game` 之前。

- 同一游戏下：脚本 `b` `sort_order`: 2，脚本 `a` `sort_order`: 2  
→ 先 `a` 后 `b`（按 ID 并列）。
