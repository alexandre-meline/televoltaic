"""Logging configuration bootstrap for TeleVoltaic."""

from __future__ import annotations

import logging
import logging.config
from typing import Any


def build_default_config(
    *,
    debug: bool = False,
    structured: bool = False,
) -> dict[str, Any]:
    """Return a dictionary logging config (dictConfig style).

    Parameters
    ----------
    debug:
        If True, lower handler/logger levels to DEBUG and use verbose
        formatter.
    structured:
        If True, use key/value style formatter instead of concise text.
    """
    formatter_name = "kv" if structured else "concise"
    level = "DEBUG" if debug else "INFO"
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "concise": {
                "()": "televoltaic.logging.formatters.ConciseFormatter",
                "debug": debug,
            },
            "kv": {
                "()": "televoltaic.logging.formatters.KeyValueFormatter",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": level,
                "formatter": formatter_name,
            }
        },
        "loggers": {
            "televoltaic": {
                "handlers": ["console"],
                "level": level,
                "propagate": False,
            },
            "televoltaic.core": {"level": level},
            "televoltaic.routing": {"level": level},
            "televoltaic.telegram": {"level": level},
            "televoltaic.middleware": {"level": level},
            "televoltaic.errors": {"level": level},
        },
        "root": {
            "level": "WARNING",
            "handlers": ["console"],
        },
    }


def init_logging(
    *,
    debug: bool,
    user_config: dict[str, Any] | None = None,
    structured: bool = False,
    allow_override: bool = True,
) -> None:
    """Initialize logging for TeleVoltaic.

    Behaviour:
    - If user_config provided (and allow_override), apply it directly.
    - If root logger already configured (handlers exist) and no user_config,
      do nothing (respect user setup).
    - Else build and apply default configuration.
    """
    root_logger = logging.getLogger()
    if user_config and allow_override:
        logging.config.dictConfig(user_config)
        return
    if root_logger.handlers:
        return
    cfg = build_default_config(debug=debug, structured=structured)
    logging.config.dictConfig(cfg)
