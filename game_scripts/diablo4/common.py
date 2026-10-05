from __future__ import annotations

import logging
import math
from enum import StrEnum

from nge_studio.rules import RuleContext
from nge_studio.runner.context import ScriptStopped

log = logging.getLogger("nge.diablo4.common")

# 好友列表区域 (l, t, r, b)
FRIEND_LIST_REGION = (1057, 76, 1579, 828)
# 副本/主城 名称识别区域
MAP_NAME_REGION = (1343, 1, 1514, 33)
# 好友列表过滤图片
FRIEND_LIST_FILTER_IMAGE = "images/好友列表.png"
# 制作人员图片
MAKE_PERSON_IMAGE = "images/制作人员.png"
# 在存档点重生图片
REBORN_IMAGE = "images/在存档点重生.png"
# 加入小队图片
JOIN_PARTY_IMAGE = "images/加入小队.png"
# 小队已满-接受图片
FULL_PARTY_ACCEPT_IMAGE = "images/小队已满-接受.png"
# 立即转移图片
IMMEDIATE_TRANSFER_IMAGE = "images/立即转移.png"
# 传送至队长-接受图片
TELEPORT_TO_LEADER_ACCEPT_IMAGE = "images/传送至队长-接受.png"
# 离开小队图片
LEAVE_PARTY_IMAGE = "images/离开小队.png"
# 离开队伍-接受图片
LEAVE_PARTY_ACCEPT_IMAGE = "images/离开小队-接受.png"


class GameState(StrEnum):
    """暗黑破坏神 IV 脚本共用游戏状态。"""

    NOT_IN_PARTY = "未组队"
    TELEPORT = "传送"
    LEAVE_PARTY = "离开队伍"
    DUNGEON_MAP = "副本跑图"
    DUNGEON_COMBAT = "副本打怪"
    CHECK_BAG = "检查背包"
    DUNGEON_DONE = "副本完成"
    HANDLE_GEAR = "处理装备"
    LOOT = "拾取物品"
    TEST = "测试"


# 打开仓库
def open_stash(ctx: RuleContext) -> bool:

    return True


def _client_center(engine) -> tuple[float, float]:
    region = engine.window.client_region
    if region is None:
        screen_w, screen_h = engine.control.screen_size
        return screen_w / 2.0, screen_h / 2.0
    left, top, right, bottom = (float(v) for v in region.local)
    return (left + right) / 2.0, (top + bottom) / 2.0


def loot(
    ctx: RuleContext,
    conf: float = 0.25,
    max_picks: int = 40,
) -> None:
    engine = ctx.engine
    log.info("【拾取物品】conf=%s max_picks=%s", conf, max_picks)
    picked = 0
    try:
        while picked < max_picks:
            ctx.studio.checkpoint()
            dets = engine.yolo.detect(
                conf=conf,
                class_ids=[0],
                timeout_ms=0,
            )
            items = [d for d in dets if d.class_id == 0]
            if not items:
                if picked:
                    log.info("【拾取物品】检测不到物品，结束（已拾取 %s 次）", picked)
                return

            cx, cy = _client_center(engine)
            nearest = min(
                items,
                key=lambda d: math.hypot(d.x - cx, d.y - cy),
            )
            dist = math.hypot(nearest.x - cx, nearest.y - cy)
            log.info(
                "【拾取物品】最近物品 (%s, %s) dist=%.1f score=%.2f",
                nearest.x,
                nearest.y,
                dist,
                nearest.score,
            )
            engine.control.move(nearest.x, nearest.y)
            engine.control.key_click("f")
            picked += 1
            if dist < 300:
                delay_ms = 200
            else:
                delay_ms = int(round(dist / (100.0 * 5) * 1000))
            if delay_ms > 0:
                log.info("【拾取物品】等待 %s 毫秒", delay_ms)
                engine.time.sleep(delay_ms)
    except ScriptStopped:
        log.info("【拾取物品】收到结束信号，中止（已拾取 %s 次）", picked)
        return

    log.warning("【拾取物品】达到最大拾取次数 %s，停止以免空转", max_picks)


def _ray_hit_inset_rect(
    cx: float,
    cy: float,
    vx: float,
    vy: float,
    left: float,
    top: float,
    right: float,
    bottom: float,
    inset: float,
) -> tuple[float, float]:
    """从中心沿 (vx, vy) 走到内缩矩形边界上的点。"""
    inset_left = left + inset
    inset_top = top + inset
    inset_right = right - inset
    inset_bottom = bottom - inset
    if inset_right < inset_left or inset_bottom < inset_top:
        return cx, cy

    inf = math.inf
    if vx > 0:
        t_x = (inset_right - cx) / vx
    elif vx < 0:
        t_x = (inset_left - cx) / vx
    else:
        t_x = inf
    if vy > 0:
        t_y = (inset_bottom - cy) / vy
    elif vy < 0:
        t_y = (inset_top - cy) / vy
    else:
        t_y = inf
    t = min(t_x, t_y)
    if not math.isfinite(t) or t < 0:
        return cx, cy
    return cx + t * vx, cy + t * vy


def walk(
    ctx: RuleContext,
    direction: float,
    distance: float,
    speed: float = 100.0,
    *,
    spread: float = 0.0,
) -> None:
    engine = ctx.engine
    if distance < 0:
        raise ValueError(f"【跑图】distance 必须 >= 0，got {distance}")
    if speed <= 0:
        raise ValueError(f"【跑图】speed 必须 > 0，got {speed}")

    region = engine.window.client_region
    rad = math.radians(direction)
    vx = math.sin(rad)
    vy = -math.cos(rad)
    if region is None:
        screen_w, screen_h = engine.control.screen_size
        center_x = screen_w / 2.0
        center_y = screen_h / 2.0
        x = center_x + distance * vx
        y = center_y + distance * vy
    else:
        left, top, right, bottom = (float(v) for v in region.local)
        center_x = (left + right) / 2.0
        center_y = (top + bottom) / 2.0
        x = center_x + distance * vx
        y = center_y + distance * vy
        if x < left or x >= right or y < top or y >= bottom:
            x, y = _ray_hit_inset_rect(
                center_x,
                center_y,
                vx,
                vy,
                left,
                top,
                right,
                bottom,
                10.0,
            )

    engine.control.move_and_click(x, y, spread=spread)
    travel = math.hypot(x - center_x, y - center_y)
    delay_ms = int(round(travel / (speed * 3) * 1000))
    if delay_ms > 0:
        log.info("【跑图】移动到点位 (%s, %s) 等待 %s 毫秒", int(round(x)), int(round(y)), delay_ms)
        engine.time.sleep(delay_ms)
