"""Resolve launch hwnd from explicit hwnd or window_title."""

from __future__ import annotations

from nge_studio.catalog.models import LaunchParameters


class WindowResolveError(ValueError):
    """No matching window for the given title."""


def resolve_hwnd_for_launch(params: LaunchParameters) -> int | None:
    """Return hwnd for NGE2 construct.

    Precedence: explicit ``params.hwnd`` wins; else first ``find_by_title`` match;
    else ``None`` (unbound). Raises ``WindowResolveError`` when title is set but
    no window matches.
    """
    if params.hwnd is not None:
        return int(params.hwnd)
    title = (params.window_title or "").strip()
    if not title:
        return None
    from nge2.window import Window

    matches = Window(None).find_by_title(title)
    if not matches:
        raise WindowResolveError(f"未找到标题包含 {title!r} 的窗口")
    return int(matches[0].hwnd)
