"""Unit tests for script_params schema and merge."""

from __future__ import annotations

from pathlib import Path

import pytest

from nge_studio.catalog.models import (
    ScriptParamField,
    coerce_script_param_value,
    merge_script_params,
)
from nge_studio.catalog.validate import CatalogValidationError, parse_manifest


def test_parse_script_params_ok() -> None:
    manifest = parse_manifest(
        {
            "display_name": "T",
            "script_params": [
                {"id": "loops", "type": "int", "label": "循环", "default": 3},
                {
                    "id": "mode",
                    "type": "choice",
                    "choices": ["a", "b"],
                    "default": "b",
                },
                {"id": "flag", "type": "bool", "default": True},
            ],
        },
        source=Path("manifest.json"),
    )
    assert len(manifest.script_params) == 3
    assert manifest.script_params[0].id == "loops"
    assert manifest.script_params[1].choices == ["a", "b"]


def test_parse_script_params_rejects_bad_id() -> None:
    with pytest.raises(CatalogValidationError):
        parse_manifest(
            {"script_params": [{"id": "1bad", "type": "string"}]},
            source=Path("m.json"),
        )


def test_parse_choice_requires_choices() -> None:
    with pytest.raises(CatalogValidationError):
        parse_manifest(
            {"script_params": [{"id": "mode", "type": "choice"}]},
            source=Path("m.json"),
        )


def test_merge_overlay_wins() -> None:
    fields = [
        ScriptParamField(id="loops", type="int", default=1),
        ScriptParamField(id="name", type="string", default="x"),
    ]
    merged = merge_script_params(fields, {"loops": 9, "unknown": 1})
    assert merged == {"loops": 9, "name": "x"}


def test_coerce_choice_fallback() -> None:
    field = ScriptParamField(id="mode", type="choice", choices=["a", "b"], default="b")
    assert coerce_script_param_value(field, "nope") == "b"
