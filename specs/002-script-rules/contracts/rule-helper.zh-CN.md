# 契约：Rule 辅助库 API

**功能**：`002-script-rules` | **日期**：2026-09-28（2026-09-30 更新 FSM）

> 英文权威版：[`rule-helper.md`](./rule-helper.md)。

补充（不替代）MVP [`script-protocol`](../../001-nge-studio-mvp/contracts/script-protocol.zh-CN.md)。

```python
from dataclasses import dataclass
from nge_studio.rules import RuleLoop, RuleContext

@dataclass
class SmokeFSM:
    beats: int = 0

loop = RuleLoop(one_action_per_tick=True, tick_interval_sec=0.1)

@loop.rule(name="probe", priority=10, cooldown=1.0)
def probe(rctx: RuleContext) -> bool:
    rctx.state.beats += 1
    return True

def run(engine, ctx):
    loop.run(engine, ctx, state=SmokeFSM())
```

**保证**：每 tick 先 `checkpoint`；暂停不评估规则；冷却仅在 `True` 后刷新；默认每 tick 单动作；异常记日志并跳过本 tick 后续规则；**state 必须为 `@dataclass` 实例**（拒绝 dict）。

**不做**：`session_max`、tick 抖动、`break_every`；不拥有引擎构造/关闭。
