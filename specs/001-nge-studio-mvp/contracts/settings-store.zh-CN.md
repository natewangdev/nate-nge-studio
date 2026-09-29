# 契约：设置存储

**功能**：`001-nge-studio-mvp` | **日期**：2026-09-28

> 英文权威版：[`settings-store.md`](./settings-store.md)。执行 Spec Kit 时忽略本中文版。

## 位置

```text
%LOCALAPPDATA%/NGE-STUDIO/settings.json
```

首次保存时创建父目录。文件缺失时使用内置默认（快捷键 F9/F10/F11；启动覆盖为空）。

## 文档形态

```json
{
  "version": 1,
  "hotkeys": {
    "start": { "key": "F9", "modifiers": [] },
    "pause": { "key": "F10", "modifiers": [] },
    "stop": { "key": "F11", "modifiers": [] }
  },
  "launch_configs": {
    "demo/smoke": {
      "updated_at": "2026-09-28T12:00:00",
      "parameters": {
        "resource_dir": ".",
        "hwnd": 123456,
        "window_title": "Diablo",
        "capture": "dxcam",
        "humanize": true,
        "control_mode": 2,
        "log_dir": null,
        "yolo_model": "models/yolo.onnx",
        "yolo_names": "models/yolo.names",
        "ocr_kwargs": null,
        "run_duration_sec": 3600
      }
    }
  }
}
```

## 规则

- `version`：正整数；未知未来版本 → 尽力加载或备份后重置（实现**不得**因此崩溃）。
- 快捷键动作**必须**保持 `start` / `pause` / `stop` 三个键。动作间物理键重复 → 拒绝保存并 UI 报错。
- `launch_configs` 键**必须**为 `game_id/script_id`。
- 成功编辑防抖和/或启动时持久化上次参数（实现可选时机；按 FR-007 **必须**跨重启保留）。
- 加载时 JSON 损坏 → 旁路备份文件，以默认启动，并提示一次警告。

## 非目标

- MVP 不做漫游配置、云同步、静态加密
