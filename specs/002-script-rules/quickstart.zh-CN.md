# 快速开始：脚本 Rule 辅助库

**功能**：`002-script-rules` | **日期**：2026-09-28

> 英文权威版：[`quickstart.md`](./quickstart.md)。

## 自动化

```powershell
uv run pytest tests/unit/test_rule_loop.py -q
uv run python scripts/validate_catalog.py
```

## 手工

```powershell
uv run python -m nge_studio
```

选中 demo 冒烟 → 启动 → 见 Rule 日志与 capture 探测；暂停无后续规则动作；结束/时长到期回空闲。

## 完成条件

- [ ] `test_rule_loop` + 目录校验通过
- [ ] Smoke 使用 `RuleLoop` 且源码含真实引擎 I/O 规则
- [ ] `002` 双语 Spec Kit 文档成对
