# NGE-STUDIO

Windows 桌面端游戏脚本管理平台，基于 [nate-game-engine](https://github.com/natewangdev/nate-game-engine)（import `nge2`）。

## 环境

- Windows 10/11
- Python 3.11+
- 按下方「NGE2（nate-game-engine）依赖来源」选好引擎安装方式后执行同步

```powershell
cd D:\GitHub\nate-nge-studio
uv sync --group dev
```

## NGE2（nate-game-engine）依赖来源

`pyproject.toml` 的 `dependencies` 始终声明包名 `nate-game-engine`；真正从哪里安装由 `[tool.uv.sources]`（或日后 PyPI）决定。改完来源后重新执行 `uv sync --group dev`。业务代码统一 `from nge2 import NGE2`，与安装来源无关。

### 1. 本地可编辑（默认，开发联调）

适合一边改引擎一边跑 Studio。修改 `../nate-game-engine` 源码后，一般无需再 sync；**重启 Studio（或重新启动脚本）**即可用到新代码。

```toml
[tool.uv.sources]
nate-game-engine = { path = "../nate-game-engine", editable = true }
```

要求本机存在兄弟目录 `D:\GitHub\nate-game-engine`（或把 `path` 改成你的实际路径）。

### 2. 从 GitHub 拉取指定 tag / release

适合固定到某个已发布版本，不依赖本地引擎仓。示例使用 tag `v0.1.0`（按 [Releases / tags](https://github.com/natewangdev/nate-game-engine/tags) 替换）：

```toml
[tool.uv.sources]
nate-game-engine = { git = "https://github.com/natewangdev/nate-game-engine.git", tag = "v0.1.0" }
```

也可改用 `branch = "main"` 或 `rev = "<commit-sha>"`。私有仓库需本机已配置 GitHub 凭据（HTTPS / SSH）。

临时命令等价写法：

```powershell
uv add "nate-game-engine @ git+https://github.com/natewangdev/nate-game-engine.git@v0.1.0"
```

注意：使用 Git tag 后，本地对引擎仓的修改**不会**自动进入 Studio。

### 3. 从 PyPI 安装（后续）

引擎正式发布到 PyPI 后：

1. 删除（或注释）`[tool.uv.sources]` 里对 `nate-game-engine` 的覆盖；
2. 在 `dependencies` 中写版本约束，例如：

```toml
dependencies = [
    "PySide6>=6.6",
    "nate-game-engine>=0.1.0",
]
```

然后 `uv sync --group dev`，将从 PyPI 解析安装。

## 开发运行

```powershell
uv run python -m nge_studio
# 或
uv run nge-studio
```

## 校验脚本目录

新增 `game_scripts/<game_id>/<script_id>/`（含 `manifest.json` + `main.py` 的 `run`）后：

```powershell
uv run python scripts/validate_catalog.py
# 或
uv run nge-studio-validate
```

任一非法脚本会使校验**失败**（非 0 退出），并打印路径与原因。

## 脚本作者协议

见 `specs/001-nge-studio-mvp/contracts/script-protocol.md`。摘要：

```python
def run(engine, ctx):
    while not ctx.should_stop():
        ctx.wait_if_paused()
        # ...
```

## 默认全局快捷键

| 动作 | 默认 |
|------|------|
| 启动 / 恢复 | F9 |
| 暂停 | F10 |
| 结束 | F11 |

设置保存在 `%LOCALAPPDATA%\NGE-STUDIO\settings.json`。

## 打包 exe

**必须先校验目录**，失败则不要打包：

```powershell
uv run python scripts/validate_catalog.py
if ($LASTEXITCODE -ne 0) { throw "catalog invalid" }
uv run pyinstaller --noconfirm packaging/nge-studio.spec
```

产物目录：`dist/NGE-STUDIO/`（onedir）。其中嵌入 `game_scripts/`，并通过 `collect_data_files` 打入 `rapidocr_onnxruntime` 的 `config.yaml` / 模型等数据（否则引擎构造 OCR 会报找不到 config）。源码中新增脚本后需重新打包才会出现在该构建的界面目录中。

**说明**：打包 exe 启动脚本时仍会走完整 `NGE2` 构造（OCR / YOLO / HID）。冒烟示例若未准备 `models/yolo.onnx` 或本机无 ESP32-S3，可能在 OCR 修复后继续在 YOLO/串口步骤失败——这属于引擎运行环境，而非目录发现问题。

## 测试

```powershell
uv run pytest -q
uv run ruff check src tests
```

## Spec Kit

本仓库使用 Spec Kit（Cursor / `cursor-agent`）。功能规格见 `specs/001-nge-studio-mvp/`。
