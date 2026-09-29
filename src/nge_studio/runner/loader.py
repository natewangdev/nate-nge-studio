"""Import script main.run."""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import Callable
from pathlib import Path
from types import ModuleType
from typing import Any

# Keep author-facing APIs in the frozen import graph (scripts load via importlib).
import nge_studio.rules  # noqa: F401
import nge_studio.runner.window_resolve  # noqa: F401


def load_run_callable(script_dir: Path) -> Callable[..., Any]:
    main_py = script_dir / "main.py"
    if not main_py.is_file():
        raise FileNotFoundError(f"缺少入口: {main_py}")
    mod_name = f"nge_studio_script_{script_dir.parent.name}_{script_dir.name}"
    spec = importlib.util.spec_from_file_location(mod_name, main_py)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法加载: {main_py}")
    module = importlib.util.module_from_spec(spec)
    script_dir_resolved = script_dir.resolve()
    game_dir_resolved = script_dir_resolved.parent
    # Game dir first so ``import common`` / ``import rules`` resolve to game-level modules.
    inserted: list[str] = []
    for path in (str(game_dir_resolved), str(script_dir_resolved)):
        if path not in sys.path:
            sys.path.insert(0, path)
            inserted.append(path)
    try:
        sys.modules[mod_name] = module
        spec.loader.exec_module(module)
    finally:
        for path in inserted:
            try:
                sys.path.remove(path)
            except ValueError:
                pass
    run = getattr(module, "run", None)
    if not callable(run):
        raise AttributeError(f"{main_py} 未导出可调用的 run")
    return run


def load_module(script_dir: Path) -> ModuleType:
    load_run_callable(script_dir)
    mod_name = f"nge_studio_script_{script_dir.parent.name}_{script_dir.name}"
    return sys.modules[mod_name]
