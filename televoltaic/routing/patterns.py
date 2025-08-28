"""Legacy decorator-based routing (deprecated).

This layer is kept for backward compatibility while migrating
to the declarative patterns API (televoltaic.routing.api).
"""

from __future__ import annotations

import warnings
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol


class HandlerFunc(Protocol):
    """Callable protocol for a handler function."""

    def __call__(self, *args: Any, **kwargs: Any) -> Any:  # noqa: D401
        ...


@dataclass
class Route:
    """Store route definition metadata (legacy)."""

    kind: str
    pattern: str
    handler: HandlerFunc
    name: str | None = None
    middleware: list[str] | None = None


class Router:
    """Legacy in-memory router used by decorators."""

    def __init__(self) -> None:
        """Initialize empty route registries."""
        self.commands: dict[str, Route] = {}
        self.callbacks: list[Route] = []
        self.messages: list[Route] = []

    def add_command(
        self,
        pattern: str,
        handler: HandlerFunc,
        name: str | None = None,
    ) -> None:
        """Register a command route."""
        self.commands[pattern] = Route("command", pattern, handler, name=name)

    def add_callback(
        self,
        pattern: str,
        handler: HandlerFunc,
        name: str | None = None,
    ) -> None:
        """Register a callback query route."""
        self.callbacks.append(Route("callback", pattern, handler, name=name))

    def add_message(
        self,
        pattern: str,
        handler: HandlerFunc,
        name: str | None = None,
    ) -> None:
        """Register a message route."""
        self.messages.append(Route("message", pattern, handler, name=name))


_global_router = Router()


def _deprecation(note: str) -> None:
    """Emit a deprecation warning for legacy decorators."""
    warnings.warn(
        f"[televoltaic.routing.patterns] {note} "
        "Use the declarative API (televoltaic.routing.api) instead.",
        DeprecationWarning,
        stacklevel=2,
    )


def command(
    pattern: str, name: str | None = None
) -> Callable[[HandlerFunc], HandlerFunc]:
    """Register a command handler via decorator (deprecated)."""

    def decorator(func: HandlerFunc) -> HandlerFunc:
        _deprecation("command() decorator is deprecated.")
        _global_router.add_command(pattern, func, name=name)
        return func

    return decorator


def callback(
    pattern: str, name: str | None = None
) -> Callable[[HandlerFunc], HandlerFunc]:
    """Register a callback handler via decorator (deprecated)."""

    def decorator(func: HandlerFunc) -> HandlerFunc:
        _deprecation("callback() decorator is deprecated.")
        _global_router.add_callback(pattern, func, name=name)
        return func

    return decorator


def message(
    pattern: str, name: str | None = None
) -> Callable[[HandlerFunc], HandlerFunc]:
    """Register a message handler via decorator (deprecated)."""

    def decorator(func: HandlerFunc) -> HandlerFunc:
        _deprecation("message() decorator is deprecated.")
        _global_router.add_message(pattern, func, name=name)
        return func

    return decorator


__all__ = [
    "command",
    "callback",
    "message",
    "Router",
    "Route",
    "_global_router",
]
