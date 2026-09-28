# 研究：脚本 Rule 辅助库

**功能**：`002-script-rules` | **日期**：2026-09-28

> 英文权威版：[`research.md`](./research.md)。

## 决策摘要

1. 辅助库放在 `nge_studio.rules`，不进 NGE2、不复制旧 `nge.bot`。
2. 精简能力：priority / cooldown / 每 tick 单动作 / 共享 state / 固定 tick 间隔；无会话总时长、无 jitter、无 break_every。
3. 每 tick 开头 `checkpoint`；暂停时不评估规则。
4. Smoke 主 I/O 规则调用 `engine.capture.grab()`（可降级）；可另加心跳日志规则。
5. 规则异常：记录日志、本 tick 视为未行动，并中止本 tick 后续规则评估。
6. 公开类型名：`Rule`、`RuleContext`、`RuleLoop`。
