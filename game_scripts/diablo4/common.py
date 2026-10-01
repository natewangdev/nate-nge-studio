from __future__ import annotations

import logging
from enum import StrEnum

log = logging.getLogger("nge.diablo4.common")

# 好友列表区域 (l, t, r, b)
FRIEND_LIST_REGION = (1057, 76, 1579, 828)
# 副本/主城 名称识别区域
MAP_NAME_REGION = (1343,1,1514,33)


# 好友列表过滤图片
FRIEND_LIST_FILTER_IMAGE = "images/好友列表.png"
# 制作人员图片
MAKE_PERSON_IMAGE = "images/制作人员.png"
# 在存档点重生图片
REBORN_IMAGE = "images/在存档点重生.png"

class GameState(StrEnum):
    """暗黑破坏神 IV 脚本共用游戏状态。"""

    NOT_IN_PARTY = "未组队"
    IN_PARTY = "已组队"
    DUNGEON_MAP = "副本跑图"
    DUNGEON_COMBAT = "副本打怪"
    CHECK_BAG = "检查背包"
    DUNGEON_DONE = "副本完成"
    HANDLE_GEAR = "处理装备"


def format_heartbeat(beats: int, *, grab_ok: bool) -> str:
    """Shared log line helper used by smoke rules."""
    return f"心跳 #{beats} (grab_ok={grab_ok})"
