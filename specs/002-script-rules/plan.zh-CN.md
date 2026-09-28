# 实现计划：脚本 Rule 辅助库

**分支**：`002-script-rules` | **日期**：2026-09-28 | **规格**：[spec.zh-CN.md](./spec.zh-CN.md)

> 英文权威版：[`plan.md`](./plan.md)。

## 摘要

在 `nge_studio.rules` 提供可复用 Rule 循环（priority / cooldown / 每 tick 单动作 / 共享 state），绑定 Studio `RunContext` 做暂停/结束；省略旧 Bot 的会话总时长、tick 抖动、`break_every`。重写 `demo/smoke`，至少一条规则调用真实 NGE2 感知/控制。启停与时长仍归 UI。

## 技术上下文 / 宪章

与 `plan.md` 一致：Python 3.11+、无新第三方依赖、pytest 假引擎、宪章门禁全部 PASS。

## 源码结构

`src/nge_studio/rules/`（`models.py` + `loop.py`）、`game_scripts/demo/smoke/main.py`、`tests/unit/test_rule_loop.py`。
