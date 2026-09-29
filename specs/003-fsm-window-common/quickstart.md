# Quickstart

```powershell
uv run pytest tests/unit/test_rule_loop.py tests/unit/test_window_resolve.py -q
uv run python scripts/validate_catalog.py
uv run python -m nge_studio
```

Manual: set window title only → Start binds/activates; miss → error; smoke uses dataclass FSM + `common`/`rules`.
