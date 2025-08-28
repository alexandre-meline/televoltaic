"""Base middleware abstractions for TeleVoltaic."""

from __future__ import annotations

from collections.abc import Awaitable
from typing import Any, Callable, Protocol


class Update:
    """Represent an incoming update (placeholder)."""

    def __init__(self, raw: Any) -> None:
        """Store raw update payload."""
        self.raw = raw


Handler = Callable[[Update], Awaitable[Any]]


class Middleware(Protocol):
    """Protocol for middleware call signature."""

    async def __call__(  # noqa: D401
        self,
        update: Update,
        next_handler: Handler,
    ) -> Any:
        """Process an update and invoke the next handler in the chain."""
        ...


class BaseMiddleware:
    """Base class that middleware implementations can subclass."""

    async def __call__(  # type: ignore[override]
        self,
        update: Update,
        next_handler: Handler,
    ) -> Any:
        """Invoke the middleware and call the next handler."""
        return await next_handler(update)
