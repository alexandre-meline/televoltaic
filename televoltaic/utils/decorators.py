"""Utility decorators for TeleVoltaic."""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any


def ensure_initialized(
    flag_getter: Callable[[], bool],
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Ensure framework is initialized before executing a function."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not flag_getter():
                raise RuntimeError("TeleVoltaic is not initialized.")
            return func(*args, **kwargs)

        return wrapper

    return decorator
