"""Catalog package."""

from nge_studio.catalog.discover import discover_catalog, resolve_catalog_root
from nge_studio.catalog.models import (
    Game,
    LaunchParameters,
    Manifest,
    Script,
    merge_launch_parameters,
)
from nge_studio.catalog.validate import CatalogValidationError, validate_catalog_tree

__all__ = [
    "CatalogValidationError",
    "Game",
    "LaunchParameters",
    "Manifest",
    "Script",
    "discover_catalog",
    "merge_launch_parameters",
    "resolve_catalog_root",
    "validate_catalog_tree",
]
