#!/usr/bin/env python
"""Validate game_scripts catalog (hard-fail)."""

from nge_studio.catalog.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
