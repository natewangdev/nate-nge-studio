"""Shared Diablo IV rules."""

from __future__ import annotations

import logging

import common

from nge_studio.rules import RuleContext

log = logging.getLogger("nge.d4.rules")

def goto_team(ctx: RuleContext) -> bool:
    if (ctx.state.STATE != common.GameState.NOT_IN_PARTY):
        return False
    
    engine = ctx.engine
    engine.control.key_click("o")

    match = engine.find.find_image(
        common.FRIEND_LIST_FILTER_IMAGE,
        threshold=0.85,
        region=common.FRIEND_LIST_REGION,
        timeout_ms=5000,
    )
    if match is None:
        log.error("组队rule: 5秒内未找到好友列表过滤图片")
        return False

    match = engine.ocr.find_text(ctx.state.FRIEND_NAME,region=common.FRIEND_LIST_REGION)
    if match is None:
        return False
    return True


def fallback_behavior(ctx: RuleContext) -> bool:
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
