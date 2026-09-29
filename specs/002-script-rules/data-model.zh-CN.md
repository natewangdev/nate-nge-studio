# 数据模型：脚本 Rule 辅助库

**功能**：`002-script-rules` | **日期**：2026-09-28（2026-09-30 更新 FSM）

> 英文权威版：[`data-model.md`](./data-model.md)。

## 实体

- **Rule**：`name`、`priority`、`cooldown`、`fn(RuleContext) -> bool`；仅在返回 `True` 后刷新冷却。
- **RuleContext**：`engine`、**dataclass FSM** `state`、`studio`（`RunContext`）。
- **RuleLoop**：规则列表、`one_action_per_tick`（默认 True）、`tick_interval_sec`（无抖动）；`run(..., state=FSM)` **必须**传入 dataclass 实例。

## 生命周期

每 tick：`checkpoint` → 按优先级评估就绪规则 → sleep。无会话总时长、无 RuleLoop.pause。**拒绝** dict 作为 state。
