"""Import script main.run."""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import Callable
from pathlib import Path
from types import ModuleType
from typing import Any


def load_run_callable(script_dir: Path) -> Callable[..., Any]:
    main_py = script_dir / "main.py"
    if not main_py.is_file():
        raise FileNotFoundError(f"缺少入口: {main_py}")
    mod_name = f"nge_studio_script_{script_dir.parent.name}_{script_dir.name}"
    spec = importlib.util.spec_from_file_location(mod_name, main_py)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法加载: {main_py}")
    module = importlib.util.module_from_spec(spec)
    # Allow relative imports within script folder
    sys.path.insert(0, str(script_dir.resolve()))
    try:
        sys.modules[mod_name] = module
        spec.loader.exec_module(module)
    finally:
        try:
            sys.path.remove(str(script_dir.resolve()))
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
