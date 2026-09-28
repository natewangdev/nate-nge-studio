"""Diablo IV test script — find bag-close template + OCR town name."""

from __future__ import annotations

import logging
from typing import Any

from nge_studio.rules import RuleContext, RuleLoop

log = logging.getLogger("nge.diablo4.test")

# Client/screen region (l, t, r, b) for town-name OCR
TOWN_OCR_REGION = (1344, 2, 1514, 31)
BAG_CLOSE_TEMPLATE = "images/背包关闭.png"
TOWN_NAME = "基奥瓦沙"

loop = RuleLoop(one_action_per_tick=True, tick_interval_sec=0.25)


@loop.rule(name="click_bag_close", priority=20, cooldown=0.8)
def click_bag_close(rctx: RuleContext) -> bool:
    """Find bag-close icon and left-click its center."""
    engine = rctx.engine
    find = engine.find
    control = getattr(engine, "control", None)
    if find is None or control is None:
        log.warning("click_bag_close: engine 缺少 find/control")
        return False
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
def town_press_i(rctx: RuleContext) -> bool:
    """OCR town strip; if text is 基奥瓦沙, press i."""
    engine = rctx.engine
    ocr = getattr(engine, "ocr", None)
    control = getattr(engine, "control", None)
    if ocr is None or control is None:
        log.warning("town_press_i: engine 缺少 ocr/control")
        return False
    try:
        lines = ocr.recognize(region=TOWN_OCR_REGION, min_score=0.4)
    except Exception as exc:
        log.warning("town_press_i: OCR 失败: %s", exc)
        return False
    texts = [str(getattr(ln, "text", "")).strip() for ln in lines]
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


def run(engine: Any, ctx: Any) -> None:
    log.info("暗黑破坏神IV 测试脚本启动 (engine=%s)", type(engine).__name__)
    loop.state.clear()
    loop.run(engine, ctx)
    log.info("暗黑破坏神IV 测试脚本结束")
