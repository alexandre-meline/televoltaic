"""Helper functions for TeleVoltaic framework."""

from __future__ import annotations

from typing import Any


def safe_import(dotted_path: str) -> Any:
    """Dynamically import a symbol from a dotted path module:attr."""
    module_path, _, attr = dotted_path.partition(":")
    module = __import__(module_path, fromlist=[attr])
    return getattr(module, attr)
