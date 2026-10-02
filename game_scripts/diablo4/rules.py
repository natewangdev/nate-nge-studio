"""Shared Diablo IV rules."""

from __future__ import annotations

import logging

import common

from nge_studio.rules import RuleContext

log = logging.getLogger("nge.d4.rules")

def team_up(ctx: RuleContext) -> bool:
    if ctx.state.STATE != common.GameState.NOT_IN_PARTY:
        return False
    
    log.info("------------------------------【组队】------------------------------")

    engine = ctx.engine
    engine.control.key_click("o")

    match = engine.find.find_image(
        common.FRIEND_LIST_FILTER_IMAGE,
        threshold=0.85,
        region=common.FRIEND_LIST_REGION,
        timeout_ms=3000,
    )
    if match is None:
        log.error("【组队】3秒内未找到好友列表过滤图片")
        return False

    match = engine.ocr.find_text(
        ctx.state.FRIEND_NAME, region=common.FRIEND_LIST_REGION
    )
    if match is None:
        engine.control.move(1301, 472)
        engine.time.delay(500, 1000)
        engine.control.scroll("down", 10)
        match = engine.ocr.find_text(
            ctx.state.FRIEND_NAME, region=common.FRIEND_LIST_REGION
        )
        if match is None:
            log.error("【组队】未找到好友{ctx.state.FRIEND_NAME}")
            return False

    engine.control.move_and_click(match.x, match.y, spread=10)

    match = engine.find.find_image(
        common.JOIN_PARTY_IMAGE,
        threshold=0.7,
        timeout_ms=3000,
    )
    if match is None:
        log.error("【组队】3秒内未找到加入小队图片")
        engine.control.key_click("esc")
        return False

    engine.control.move_and_click(match.x, match.y, spread=match.height / 2)
    engine.time.sleep(500)

    match = engine.find.find_image(
        common.FULL_PARTY_ACCEPT_IMAGE,
        threshold=0.7,
    )

    if match is not None:
        engine.control.move_and_click(match.x, match.y, spread=match.height / 2)
        engine.time.sleep(500)
        engine.control.key_click("esc")
        return False
    else:
        engine.time.delay(2000, 3000)
    
    # 找接受或者立即转移按钮
    match = engine.find.find_image(
        common.TELEPORT_TO_LEADER_ACCEPT_IMAGE,
        threshold=0.7,
    )
    if match is not None:
        engine.control.move_and_click(match.x, match.y, spread=match.height / 2)
    
    match = engine.find.find_image(
        common.IMMEDIATE_TRANSFER_IMAGE,
        threshold=0.7,
    )
    if match is not None:
        engine.control.move_and_click(match.x, match.y, spread=match.height / 2)

    # 判断是否进入指定副本
    match = engine.ocr.find_text(ctx.state.TARGET_MAP_NAME, region=common.MAP_NAME_REGION,timeout_ms=10000)
    if match is None:
        log.error("【组队】10秒未找到指定副本{ctx.state.TARGET_MAP_NAME}")
        return False
    
    # 离开队伍
    engine.control.key_click("o")
    engine.time.sleep(500)
    match = engine.find.find_image(common.LEAVE_PARTY_IMAGE, threshold=0.7)
    if match is None:
        log.error("【组队】未找到离开小队按钮")
        return False

    engine.control.move_and_click(match.x, match.y, spread=match.height / 2)
    engine.time.sleep(500)
    match = engine.find.find_image(common.LEAVE_PARTY_ACCEPT_IMAGE, threshold=0.7)
    if match is None:
        log.error("【组队】未找到离开队伍-接受图片")
        return False

    engine.control.move_and_click(match.x, match.y, spread=match.height / 2)
    ctx.state.STATE = common.GameState.DUNGEON_MAP
    return True

def fallback_behavior(ctx: RuleContext) -> bool:
    log.info("------------------------------【兜底】------------------------------")
    engine = ctx.engine
    match = engine.find.find_image(common.MAKE_PERSON_IMAGE, threshold=0.7)
    if match is not None:
        engine.control.move_and_click(match.x, match.y)
        return True

    match = engine.find.find_image(common.REBORN_IMAGE, threshold=0.7)
    if match is not None:
        engine.control.move_and_click(match.x, match.y)
        return True

    return False
