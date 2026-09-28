# 数据模型：脚本 Rule 辅助库

**功能**：`002-script-rules` | **日期**：2026-09-28

> 英文权威版：[`data-model.md`](./data-model.md)。

## 实体

- **Rule**：`name`、`priority`、`cooldown`、`fn(RuleContext) -> bool`；仅在返回 `True` 后刷新冷却。
- **RuleContext**：`engine`、共享 `state`、`studio`（`RunContext`）。
- **RuleLoop**：规则列表、`one_action_per_tick`（默认 True）、`tick_interval_sec`（无抖动）。

## 生命周期

每 tick：`checkpoint` → 按优先级评估就绪规则 → sleep。无会话总时长、无 RuleLoop.pause。
