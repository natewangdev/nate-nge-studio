from __future__ import annotations

import logging

log = logging.getLogger("nge.diablo4.common")

# 好友列表区域 (l, t, r, b)
FRIEND_LIST_REGION = (1057, 76, 1579, 828)
# 好友列表面板模板（相对脚本 resource_dir）
FRIEND_LIST_TEMPLATE = "images/好友列表.png"

def format_heartbeat(beats: int, *, grab_ok: bool) -> str:
    """Shared log line helper used by smoke rules."""
    return f"心跳 #{beats} (grab_ok={grab_ok})"
