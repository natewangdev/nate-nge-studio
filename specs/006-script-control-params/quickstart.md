# Quickstart: 006

```powershell
uv run pytest tests/unit/test_run_context.py tests/unit/test_script_params.py tests/integration/test_runner.py -q
uv run python scripts/validate_catalog.py
```

Manual: declare `script_params` on a script; edit in UI; Start and log `ctx.script_params`; call `ctx.request_stop()`; set duration + 关机 only in tests with mock shutdown.
