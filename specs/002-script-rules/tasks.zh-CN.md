# 任务：脚本 Rule 辅助库

> 英文权威版：[`tasks.md`](./tasks.md)。任务 ID 与路径以英文版为准。

**测试**：包含 — FR-011 要求无 HID 的辅助库单测。

## 阶段摘要

1. **Setup**：确认 `src/nge_studio/rules/` 布局  
2. **基础**：`Rule` / `RuleContext` / `RuleLoop` + 导出  
3. **US1**：`tests/unit/test_rule_loop.py`（优先级、冷却、暂停、结束）  
4. **US2**：重写 `game_scripts/demo/smoke/main.py`（RuleLoop + capture.grab 探测）  
5. **US3**：文档边界核对 + README 短链（可选）  
6. **抛光**：pytest + ruff  

MVP：T001–T012。
