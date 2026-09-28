"""CLI: nge-studio-validate / scripts/validate_catalog.py"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from nge_studio.catalog.discover import resolve_catalog_root
from nge_studio.catalog.validate import CatalogValidationError, validate_catalog_tree


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="校验 game_scripts 目录（非法脚本则失败）")
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="game_scripts 根目录（默认自动解析）",
    )
    args = parser.parse_args(argv)
    root = resolve_catalog_root(args.root)
    try:
        passed = validate_catalog_tree(root)
    except CatalogValidationError as exc:
        print(f"校验失败: {exc}", file=sys.stderr)
        return 1
    print(f"校验通过: {root} （{len(passed)} 个脚本）")
    for game_id, script_id in passed:
        print(f"  - {game_id}/{script_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
