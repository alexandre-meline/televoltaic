"""Default settings loader for TeleVoltaic."""

from __future__ import annotations

from typing import Any

DEFAULT_SETTINGS: dict[str, Any] = {
    "DEBUG": False,
    "INSTALLED_APPS": [],
    "TELEGRAM": {
        "TOKEN": None,
    },
}


def load_settings(overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return merged settings with optional overrides."""
    result = dict(DEFAULT_SETTINGS)
    if overrides:
        for key, value in overrides.items():
            if isinstance(value, dict) and isinstance(result.get(key), dict):
                result[key] = {**result[key], **value}  # shallow merge
            else:
                result[key] = value
    return result
