# 数据模型：目录排序

**功能**：`008-catalog-sort-order` | **日期**：2026-10-04

> 英文权威版：[data-model.md](./data-model.md)。执行 Spec Kit 时忽略本中文版。

## 实体

### GameManifest（扩展）

| 字段 | 类型 | 必填 | 规则 |
|------|------|------|------|
| `display_name` | 字符串或省略 | 否 | 同 004 |
| `description` | 字符串或省略 | 否 | 同 004 |
| `sort_order` | 整数或省略 | 否 | 若出现：JSON 整数，非 bool、非浮点。允许 0 与负数 |

缺少游戏 manifest 文件 ⇒ 该游戏 `sort_order = None`（省略组）。

### Manifest（脚本，扩展）

| 字段 | 类型 | 必填 | 规则 |
|------|------|------|------|
| 既有字段 | — | — | 同 001/006 |
| `sort_order` | 整数或省略 | 否 | 与游戏相同的整数规则 |

### Game / Script（运行时）

| 属性 | 说明 |
|------|------|
| `game_id` / `script_id` | 文件夹名；身份不变 |
| `manifest.sort_order` | 解析后为 `int \| None` |
| `scripts` 列表 | 按 FR-005 在游戏内排序 |
| 目录 `list[Game]` | 按 FR-005 在游戏间排序 |

## 同一列表比较

1. `sort_order is not None` 的项在 `None` 之前。
2. 非 `None` 中按数值升序。
3. 相同 `sort_order`，或全部为 `None`：按 `game_id` 或 `script_id` 字典序（Python 默认 `str` 对文件夹名）。

## 校验

- 未知顶层键仍失败。
- 出现但非整数 → `CatalogValidationError`（路径 + 原因），整次目录校验失败。
- 缺失 → 合法。

## 关系

- 脚本 `sort_order` 仅在同一游戏的脚本间比较。
- 游戏 `sort_order` 仅在发现返回的游戏间比较。
