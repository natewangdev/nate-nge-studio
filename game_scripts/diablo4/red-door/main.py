"""Diablo IV test script — find bag-close template + OCR town name."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

from nge_studio.rules import RuleContext, RuleLoop
import rules

if TYPE_CHECKING:
    from nge2 import NGE2

    from nge_studio.runner.context import RunContext

log = logging.getLogger("nge.diablo4.red-door")

# Client/screen region (l, t, r, b) for town-name OCR
TOWN_OCR_REGION = (1344, 2, 1514, 31)
BAG_CLOSE_TEMPLATE = "images/背包关闭.png"
TOWN_NAME = "基奥瓦沙"


@dataclass
class FSM:
    """Placeholder FSM for RuleLoop (extend with phase fields as needed)."""

    FRIEND_NAME: str = "路西法"

loop = RuleLoop(one_action_per_tick=True, tick_interval_sec=0.25)

loop.add_rule(rules.form_dungeon_party, name="form_dungeon_party", priority=30, cooldown=5.0)
loop.add_rule(rules.fallback_behavior, name="fallback_behavior", priority=0, cooldown=1.0)

@loop.rule(name="click_bag_close", priority=20, cooldown=0.8)
def click_bag_close(ctx: RuleContext) -> bool:
    """Find bag-close icon and left-click its center."""
    engine = ctx.engine
    find = engine.find
    control = engine.control
    try:
        match = find.find_image(BAG_CLOSE_TEMPLATE, threshold=0.85)
    except Exception as exc:
        log.warning("click_bag_close: find_image 失败: %s", exc)
        return False
    if match is None:
        log.info("click_bag_close: 未找到背包关闭图标")
        return False
    try:
        control.move_and_click(match.x, match.y)
    except Exception as exc:
        log.warning("click_bag_close: 点击失败: %s", exc)
        return False

    log.info(
        "click_bag_close: 点击 (%.0f, %.0f) score=%.3f",
        match.x,
        match.y,
        match.score,
    )
    return True

@loop.rule(name="town_press_i", priority=10, cooldown=1.0)
def town_press_i(ctx: RuleContext) -> bool:
    """OCR town strip; if text is 基奥瓦沙, press i."""
    engine = ctx.engine
    ocr = engine.ocr
    control = engine.control
    try:
        lines = ocr.recognize(region=TOWN_OCR_REGION, min_score=0.4)
    except Exception as exc:
        log.warning("town_press_i: OCR 失败: %s", exc)
        return False
    texts = [str(ln.text).strip() for ln in lines]
    hit = any(t == TOWN_NAME or TOWN_NAME in t for t in texts if t)
    if not hit:
        if texts:
            log.debug("town_press_i: OCR=%s (未命中)", texts)
        return False
    try:
        control.key_click("i")
    except Exception as exc:
        log.warning("town_press_i: 按键 i 失败: %s", exc)
        return False

    log.info("town_press_i: 识别到「%s」，已按 i（OCR=%s）", TOWN_NAME, texts)
    return True


def run(engine: NGE2, ctx: RunContext) -> None:
    log.info("脚本启动 (engine=%s)", type(engine).__name__)
    loop.run(engine, ctx, state=FSM())
    log.info("脚本结束")
