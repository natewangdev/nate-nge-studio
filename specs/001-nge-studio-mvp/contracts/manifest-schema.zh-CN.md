# 契约：Manifest Schema

**功能**：`001-nge-studio-mvp` | **日期**：2026-09-28

> 英文权威版：[`manifest-schema.md`](./manifest-schema.md)。执行 Spec Kit 时忽略本中文版。

文件：`game_scripts/<game_id>/<script_id>/manifest.json`（UTF-8 JSON 对象）。

## Schema（概念）

```json
{
  "display_name": "string (optional)",
  "description": "string (optional)",
  "defaults": {
    "resource_dir": "string (optional)",
    "hwnd": null,
    "window_title": null,
    "capture": "dxcam",
    "humanize": true,
    "control_mode": 2,
    "log_dir": null,
    "yolo_model": "models/yolo.onnx",
    "yolo_names": "models/yolo.names",
    "ocr_kwargs": null,
    "run_duration_sec": null
  }
}
```

## 字段规则

| 字段 | 必需 | 说明 |
|------|------|------|
| `display_name` | 否 | 空/缺失 → UI 显示 `script_id` |
| `description` | 否 | 自由文本 |
| `defaults` | 否 | 对象；未知键 → 校验**失败**（严格） |
| `defaults.capture` | 否 | 若存在仅允许 `"dxcam"` 或 `"mss"` |
| `defaults.hwnd` | 否 | `null` 或非负整数 |
| `defaults.window_title` | 否 | `null` 或字符串；hwnd 为空时用于标题解析 |
| `defaults.ocr_kwargs` | 否 | `null` 或 JSON 对象（非字符串） |
| `defaults.run_duration_sec` | 否 | `null` 或 &gt; 0 的数字（秒）。UI 以小时编辑（× 3600）。 |

## 校验结果

- 文件缺失、非 JSON 对象、或规则违规 → **目录校验使整次构建失败**，并给出路径 + 原因。
- defaults 中的相对路径在启动时相对**脚本目录**解释（除非已是绝对路径）。

## 示例（样例冒烟脚本）

```json
{
  "display_name": "冒烟示例",
  "description": "合规样例：尊重暂停/结束并周期性打日志",
  "defaults": {
    "resource_dir": ".",
    "capture": "dxcam",
    "humanize": true,
    "control_mode": 2,
    "run_duration_sec": null
  }
}
```
