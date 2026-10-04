# 契约：游戏 Manifest Schema

**功能**：`004-icon-game-display` | **日期**：2026-09-30

> 英文权威版：[game-manifest-schema.md](./game-manifest-schema.md)。执行 Spec Kit 时忽略本中文版。

文件：`game_scripts/<game_id>/manifest.json`（UTF-8 JSON 对象）。**可选。**

与 `game_scripts/<game_id>/<script_id>/manifest.json` 的脚本 manifest 区分。

## Schema（概念）

```json
{
  "display_name": "string (optional)",
  "description": "string (optional)",
  "sort_order": 0
}
```

## 字段规则

| 字段 | 必需 | 说明 |
|------|------|------|
| `display_name` | 否 | 空/缺失 → UI 显示 `game_id` |
| `description` | 否 | 自由文本；v1 标签可忽略 |
| `sort_order` | 否 | 若出现须为 JSON 整数。游戏目录顺序见 `specs/008-catalog-sort-order/contracts/sort-order.md` |
| `defaults` | **禁止** | 启动默认值只属于脚本 manifest |
| 其他键 | **禁止** | 严格：未知键 → 目录校验失败 |

## 校验结果

- 文件不存在 → 合法（不是错误）。
- 文件存在且 JSON 非法 / 非对象 / 违反规则 → **整次目录校验失败**，错误含路径 + 原因。
- 目录发现**不得**将此文件当作脚本条目。

## 示例

```json
{
  "display_name": "演示游戏",
  "description": "样例与冒烟脚本所在游戏",
  "sort_order": 1
}
```
