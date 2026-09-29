"""Shared helpers for demo game scripts."""

from __future__ import annotations

import logging

log = logging.getLogger("nge.demo.common")


def format_heartbeat(beats: int, *, grab_ok: bool) -> str:
    """Shared log line helper used by smoke rules."""
    return f"心跳 #{beats} (grab_ok={grab_ok})"
