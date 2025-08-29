"""Default settings loader for TeleVoltaic.

This module centralizes the configuration loading logic and prepares
a plain Python dict that the framework can later adapt into the
`TeleVoltaicSettings` dataclass.

Goals:
- Provide a single DEFAULT_SETTINGS structure.
- Allow user overrides (e.g. from a project settings.py).
- Optionally apply environment variable overrides (12‑factor friendly).
- Introduce ROOT_ROUTES (Django-like routing entry point).
- Keep backward compatibility for existing keys (DEBUG, INSTALLED_APPS).

Environment variables (all optional):
    TELEVOLTAIC_DEBUG = "1" | "true" | "yes"
    TELEVOLTAIC_TOKEN = "<telegram bot token>"
    TELEVOLTAIC_ROOT_ROUTES = "myproject.routes:urlpatterns"
    TELEVOLTAIC_INSTALLED_APPS = "app1,app2,app3"

Design notes:
- We keep the return type as a raw dict for now (historical behavior).
- A helper `adapt_to_framework` is provided to map dict -> TeleVoltaicSettings.
  (Framework code can call it; this avoids circular import issues.)
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # Only for static typing; avoids runtime import cycle.
    from .framework import TeleVoltaicSettings

DEFAULT_SETTINGS: dict[str, Any] = {
    "DEBUG": False,
    "INSTALLED_APPS": [],
    "TELEGRAM": {
        "TOKEN": None,
    },
    # Entry point for declarative routing (Django-like).
    # Example: "myproject.routes:urlpatterns"
    "ROOT_ROUTES": None,
}

TRUE_SET = {"1", "true", "yes", "on", "y"}


def _as_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    return value.strip().lower() in TRUE_SET


def _split_csv(value: str | None) -> list[str] | None:
    if not value:
        return None
    return [item.strip() for item in value.split(",") if item.strip()]


def _deep_merge(
    base: dict[str, Any], extra: Mapping[str, Any]
) -> dict[str, Any]:
    """Shallow + one-level deep merge."""
    result = dict(base)
    for key, value in extra.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, Mapping)
        ):
            merged_child = dict(result[key])
            merged_child.update(value)  # shallow
            result[key] = merged_child
        else:
            result[key] = value
    return result


def env_overrides() -> dict[str, Any]:
    """Build a dict of settings overrides from environment variables."""
    overrides: dict[str, Any] = {}

    debug_env = _as_bool(os.getenv("TELEVOLTAIC_DEBUG"))
    if debug_env is not None:
        overrides["DEBUG"] = debug_env

    token_env = os.getenv("TELEVOLTAIC_TOKEN")
    if token_env:
        overrides.setdefault("TELEGRAM", {})
        overrides["TELEGRAM"]["TOKEN"] = token_env

    routes_env = os.getenv("TELEVOLTAIC_ROOT_ROUTES")
    if routes_env:
        overrides["ROOT_ROUTES"] = routes_env

    apps_env = _split_csv(os.getenv("TELEVOLTAIC_INSTALLED_APPS"))
    if apps_env is not None:
        overrides["INSTALLED_APPS"] = apps_env

    return overrides


def load_settings(
    overrides: dict[str, Any] | None = None,
    *,
    use_env: bool = True,
) -> dict[str, Any]:
    """Return merged settings dict.

    Precedence (lowest → highest):
        1. DEFAULT_SETTINGS
        2. overrides (user/project settings module)
        3. environment variables (if use_env=True)
    """
    settings = dict(DEFAULT_SETTINGS)

    if overrides:
        settings = _deep_merge(settings, overrides)

    if use_env:
        env = env_overrides()
        settings = _deep_merge(settings, env)

    return settings


def adapt_to_framework(
    settings_dict: Mapping[str, Any],
) -> TeleVoltaicSettings:
    """Adapt a raw settings dict to a TeleVoltaicSettings instance.

    This helper is optional; framework code can import and call it
    AFTER defining the TeleVoltaicSettings dataclass with the
    fields: installed_apps, debug, telegram_token, root_routes.

    Returns
    -------
    TeleVoltaicSettings
        Instance populated from the raw dict.

    Raises
    ------
    RuntimeError
        If the TeleVoltaicSettings dataclass shape changes unexpectedly.
    """
    # Local import to avoid circular import at module load time.
    from .framework import TeleVoltaicSettings as _TVSettings  # type: ignore

    installed_apps = list(settings_dict.get("INSTALLED_APPS", []))
    debug = bool(settings_dict.get("DEBUG", False))
    telegram_token = (settings_dict.get("TELEGRAM", {}) or {}).get(
        "TOKEN", None
    )
    root_routes = settings_dict.get("ROOT_ROUTES")

    try:
        return _TVSettings(
            installed_apps=installed_apps,
            debug=debug,
            telegram_token=telegram_token,
            **(
                {"root_routes": root_routes}
                # type: ignore[attr-defined]
                if "root_routes" in _TVSettings.__dataclass_fields__
                else {}
            ),
        )
    except TypeError as exc:  # pragma: no cover
        raise RuntimeError(
            "TeleVoltaicSettings signature changed; "
            "update adapt_to_framework()."
        ) from exc


__all__ = [
    "DEFAULT_SETTINGS",
    "load_settings",
    "env_overrides",
    "adapt_to_framework",
]
