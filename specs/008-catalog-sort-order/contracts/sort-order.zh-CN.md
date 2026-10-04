# 契约：目录 `sort_order`

**功能**：`008-catalog-sort-order` | **日期**：2026-10-04

> 英文权威版：[sort-order.md](./sort-order.md)。执行 Spec Kit 时忽略本中文版。

扩展：

- 脚本 manifest：`specs/001-nge-studio-mvp/contracts/manifest-schema.md`
- 游戏 manifest：`specs/004-icon-game-display/contracts/game-manifest-schema.md`

## 字段

| 位置 | 字段 | 必填 | 类型 |
|------|------|------|------|
| `game_scripts/<game_id>/manifest.json` | `sort_order` | 否 | JSON 整数 |
| `game_scripts/<game_id>/<script_id>/manifest.json` | `sort_order` | 否 | JSON 整数 |

## 规则

- 出现时允许：JSON 整数（负、零、正）。
- 出现时禁止：布尔、浮点、字符串、数组、对象、`null`。
- 缺键：合法；该项进入该列表的**省略**组。
- 其他未知键：目录校验仍失败（严格）。
- 游戏 manifest 仍**禁止** `defaults`。

## 列表顺序（规范性）

游戏（已发现游戏之间）与脚本（同一游戏内）：

1. 有显式 `sort_order` 的项在前，升序。
2. 然后是省略 `sort_order` 的项。
3. 并列（同一整数，或皆省略）：文件夹 ID 字典序。

## UI

- 左栏树**必须**遵循发现顺序。
- **不得**提供改序控件，也**不得**把顺序写入操作者设置。

## 错误

非法 `sort_order` → 整次目录校验失败；消息含文件路径，并说明 `sort_order` 必须是整数。
