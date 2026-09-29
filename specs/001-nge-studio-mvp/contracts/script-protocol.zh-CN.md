# 契约：脚本入口协议

**功能**：`001-nge-studio-mvp` | **日期**：2026-09-28

> 英文权威版：[`script-protocol.md`](./script-protocol.md)。执行 Spec Kit 时忽略本中文版。

本契约约束 NGE-STUDIO 与每个目录脚本之间的约定。

## 布局

```text
game_scripts/<game_id>/
  common.py          # 可选 — 本游戏共享方法（不是目录脚本）
  rules.py           # 可选 — 本游戏共享规则（不是目录脚本）
  <script_id>/
    manifest.json    # 必需 — 见 manifest-schema.md
    main.py          # 必需 — 必须定义 run()
    ...              # 参数可能引用的可选资源
```

目录发现**仅**遍历 `<game_id>/<script_id>/` 文件夹。游戏级 `common.py` / `rules.py` **不得**当作脚本。加载脚本时，Studio **必须**将游戏目录加入 `sys.path`（或等价方式），以便 `main.py` 可 `import common` / `import rules`。

## 入口

```python
from nge2 import NGE2

def run(engine: NGE2, ctx: "RunContext") -> None:
    """Studio 在构造 NGE2 后于工作线程调用。"""
    ...
```

规则：

- Studio 从脚本目录导入 `main` 并调用 `run`。
- Studio 拥有 `engine` 的构造与 `close()`（返回后不得依赖引擎仍可用）。
- 在 `ctx.should_stop()` 为真后，`run` **应当**尽快返回。
- 长循环**必须**定期调用 `ctx.wait_if_paused()` 或 `ctx.checkpoint()`，使暂停/结束在 SC-003 目标内保持协作式。

## RunContext（概念）

| 成员 | 行为 |
|------|------|
| `is_paused() -> bool` | 暂停激活时为真 |
| `should_stop() -> bool` | 结束或 Studio 超时后为真 |
| `wait_if_paused(poll_sec=0.05) -> None` | 暂停时阻塞；恢复或请求停止时返回 |
| `checkpoint() -> None` | `wait_if_paused()` 后若已请求停止则走停止路径（实现可选异常或布尔；推荐抛出 Studio 定义的 `ScriptStopped`） |

推荐模式：

```python
def run(engine, ctx):
    while not ctx.should_stop():
        ctx.wait_if_paused()
        if ctx.should_stop():
            break
        # 做一单位工作...
```

## Studio 生命周期保证

1. 进程内最多一个活动 `run`。
2. 结束/超时：置停止 → 最多等待 **10s** join → 工作线程退出时在 `finally` 中 `engine.close()`；超过 10s 则挂起警告（MVP 不强制杀）。
3. logger 层级 `nge` 下的日志镜像到活动会话的 UI 面板。

## 非目标

- MVP 不支持其他入口名（`main()`、`__call__`）
- MVP 不支持 `async def run`
