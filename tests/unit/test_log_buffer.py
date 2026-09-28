"""Log buffer cap tests."""

from __future__ import annotations

from nge_studio.logging_bridge.qt_handler import LogBuffer


def test_cap_5000() -> None:
    buf = LogBuffer(maxlen=5)
    for i in range(8):
        buf.append(str(i))
    assert len(buf) == 5
    assert buf.lines() == ["3", "4", "5", "6", "7"]
