"""NGE-STUDIO: Windows desktop shell for NGE2 game scripts."""

from __future__ import annotations

try:
    from importlib.metadata import PackageNotFoundError, version

    __version__ = version("nate-nge-studio")
except PackageNotFoundError:
    __version__ = "0.1.0+dev"

__all__ = ["__version__"]
