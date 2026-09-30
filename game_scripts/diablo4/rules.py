"""Shared Diablo IV rules."""

from __future__ import annotations

import logging
import time

import common

from nge_studio.rules import RuleContext

log = logging.getLogger("nge.diablo4.rules")

def form_dungeon_party(ctx: RuleContext) -> bool:
    ctx.engine.control.key_click("o")

    time.sleep(0.35)

    match = ctx.engine.find.find_image(
        common.FRIEND_LIST_TEMPLATE,
        threshold=0.85,
        region=common.FRIEND_LIST_REGION,
    )
    if match is None:
        log.info("form_dungeon_party: 未找到好友列表模板")
        ctx.engine.control.key_click("esc")
        return False

    lines = ctx.engine.ocr.recognize(region=common.FRIEND_LIST_REGION, min_score=0.4)
    texts = [str(ln.text).strip() for ln in lines]
    hit = next(
        (
            ln
            for ln in lines
            if (t := str(ln.text).strip())
            and (t == ctx.state.FRIEND_NAME or ctx.state.FRIEND_NAME in t)
        ),
        None,
    )
    if hit is None:
        log.info("form_dungeon_party: 未识别到「%s」（OCR=%s）", ctx.state.FRIEND_NAME, texts)
        ctx.engine.control.key_click("esc")
        return False

    ctx.engine.control.move_and_click(hit.x, hit.y)
    log.info(
        "form_dungeon_party: 已点击「%s」(%.0f, %.0f) OCR=%s",
        ctx.state.FRIEND_NAME,
        hit.x,
        hit.y,
        texts,
    )
    return True


def fallback_behavior(ctx: RuleContext) -> bool:
    log.info("fallback_behavior: 这是一个兜底行为")
    return True
