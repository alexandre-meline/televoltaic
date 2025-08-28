"""Handler utilities (future execution adapters) for TeleVoltaic."""

from __future__ import annotations

from typing import Any, Callable


def execute_handler(
    handler: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Execute a handler with provided arguments (sync placeholder)."""
    return handler(*args, **kwargs)
