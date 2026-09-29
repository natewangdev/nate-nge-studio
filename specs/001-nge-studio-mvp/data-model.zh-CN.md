# 数据模型：NGE-STUDIO MVP 外壳

**功能**：`001-nge-studio-mvp` | **日期**：2026-09-28

> 英文权威版：[`data-model.md`](./data-model.md)。执行 Spec Kit 时忽略本中文版。

持久化：仅 JSON 设置文件。目录实体在发现时从文件系统派生。

## 实体

### Game（游戏）

| 字段 | 类型 | 规则 |
|------|------|------|
| game_id | str | `game_scripts/` 下文件夹名；非空；稳定 ID |
| path | path | 游戏文件夹绝对路径 |
| scripts | list[Script] | 通过校验的子脚本文件夹 |

### Script（脚本）

| 字段 | 类型 | 规则 |
|------|------|------|
| game_id | str | 所属游戏 |
| script_id | str | 游戏下文件夹名；非空；稳定 ID |
| path | path | 脚本文件夹绝对路径 |
| entry_module | path | **必须**为脚本目录下 `main.py` |
| manifest | Manifest | 解析自 `manifest.json` |
| display_name | str | `manifest.display_name`，缺失则回退 `script_id` |

**标识**：目录内唯一键 `game_id/script_id`。

### Manifest

| 字段 | 类型 | 规则 |
|------|------|------|
| display_name | str | 可选；缺失/空 → UI 用 `script_id` |
| description | str | 可选 |
| defaults | LaunchParameters | 可选的部分表单默认值 |

见 [manifest-schema.md](./contracts/manifest-schema.md)。

### LaunchParameters（启动参数）

面向作者的 NGE2 构造字段 + Studio 超时。

| 字段 | 类型 | 规则 |
|------|------|------|
| resource_dir | str/path | 启动时必填（解析后非空） |
| hwnd | int \| null | 可选；null/空 → 可从 `window_title` 解析，或未绑定 |
| window_title | str \| null | 可选；仅当 `hwnd` 为空时使用；经 NGE2 `find_by_title` 子串匹配；取第一个；无匹配 → 启动失败 |
| capture | `"dxcam"` \| `"mss"` | 默认 `"dxcam"` |
| humanize | bool | 默认 `true` |
| control_mode | int | 默认 `2`；非法值在引擎构造时失败 |
| log_dir | str/path \| null | 可选；UI 支持手输或文件夹选择 |
| yolo_model | str/path | 默认按 NGE2（`models/yolo.onnx`）；UI 支持手输或文件选择 |
| yolo_names | str/path \| null | 默认按 NGE2；UI 支持手输或文件选择 |
| ocr_kwargs | object \| null | JSON 对象；非法 JSON 启动校验失败；**无**文件选择 |
| run_duration_sec | number \| null | 仅 Studio 的规范存储（秒）；null/省略/≤0 → 无超时；&gt;0 → 到期结束。**UI 以小时编辑**（小时 × 3600 ↔ `run_duration_sec`） |

**路径选择规则**（仅 UI）：

- 文件夹选择：`resource_dir`、`log_dir`。
- 文件选择：`yolo_model`（建议 `*.onnx` + 所有文件）、`yolo_names`（建议 `*.names`/`*.txt` + 所有文件）。
- 对话框起始目录：当前 `resource_dir` 非空且存在时用其；否则用户主目录。
- 选择后：若路径位于 `resource_dir` 下则存相对路径；否则存绝对路径。

### LaunchConfiguration（持久化覆盖）

| 字段 | 类型 | 规则 |
|------|------|------|
| script_key | str | `game_id/script_id` |
| parameters | LaunchParameters | 上次使用值（可部分） |
| updated_at | datetime | 可选 ISO 时间戳 |

**选中时合并**：manifest `defaults` ← 被已存在的上次字段覆盖。

### RunContext（运行上下文）

| 字段 | 类型 | 规则 |
|------|------|------|
| paused | bool | 暂停置位；恢复（暂停时启动）清除 |
| stop_requested | bool | 结束或 Studio 超时置位 |
| started_at | datetime | 运行开始时设置 |

**操作**（见 [script-protocol.md](./contracts/script-protocol.md)）：`is_paused`、`should_stop`、`wait_if_paused`、`checkpoint`。

### RunSession（运行会话）

| 字段 | 类型 | 规则 |
|------|------|------|
| script_key | str | 活动脚本身份 |
| state | enum | `idle` \| `running` \| `paused` \| `stopping` |
| engine | NGE2 \| null | 非空闲时持有；退出时关闭 |
| log_lines | list[str] | 上限 5000；空闲后保留至下次启动 |
| hung_warning | bool | 结束宽限（10s）到仍未 join 时为真 |

**转换**：

```text
idle --启动--> running
running --暂停--> paused
paused --启动/F9（恢复）--> running
running|paused --结束|超时--> stopping --join+close--> idle
idle --启动（非空闲时）--> 拒绝（保持原状态）
```

进程内最多一个非空闲会话。

### HotkeyBinding（快捷键绑定）

| 字段 | 类型 | 规则 |
|------|------|------|
| action | `"start"` \| `"pause"` \| `"stop"` | 各恰好一个绑定 |
| key | str | 规范键名（如 `F9`）；默认 F9/F10/F11 |
| modifiers | set | 可选；MVP 默认无修饰键 |

### AppSettings（文件根）

| 字段 | 类型 | 规则 |
|------|------|------|
| hotkeys | list[HotkeyBinding] | 三个动作 |
| launch_configs | map[script_key → LaunchConfiguration] | 每脚本覆盖 |

见 [settings-store.md](./contracts/settings-store.md)。

### WindowPickResult（窗口点选结果）

| 字段 | 类型 | 规则 |
|------|------|------|
| hwnd | int | 顶层窗口句柄 |
| title | str | 展示标签 |
| pid | int | 所属进程；**不得**等于 Studio PID |

## 校验规则

- 缺失 `manifest.json` 或 `main.py` / 缺失 `run` → 目录校验**构建失败**
- manifest JSON 损坏或 schema 违规 → **构建失败**
- `resource_dir` 为空启动 → UI 拒绝并报错
- `ocr_kwargs` JSON 非法 → 拒绝启动
- 会话非空闲时第二次启动 → 拒绝并说明
- 点选指向 Studio PID → 拒绝；hwnd 不变
- 引擎构造时 hwnd 无效 → 启动失败；会话回空闲；无僵尸运行

## 非目标

- 多运行会话、远程设置同步、脚本市场元数据
