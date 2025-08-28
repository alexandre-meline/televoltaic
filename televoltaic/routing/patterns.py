"""Routing patterns and decorators for TeleVoltaic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Protocol


class HandlerFunc(Protocol):
    """Callable protocol for a handler function."""

    def __call__(self, *args: Any, **kwargs: Any) -> Any:  # noqa: D401
        ...


@dataclass
class Route:
    """Store route definition metadata."""

    kind: str
    pattern: str
    handler: HandlerFunc
    name: str | None = None
    middleware: list[str] | None = None


class Router:
    """Register command, callback and message routes."""

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


def command(
    pattern: str, name: str | None = None
) -> Callable[[HandlerFunc], HandlerFunc]:
    """Register a command handler via decorator."""

    def decorator(func: HandlerFunc) -> HandlerFunc:
        _global_router.add_command(pattern, func, name=name)
        return func

    return decorator


def callback(
    pattern: str, name: str | None = None
) -> Callable[[HandlerFunc], HandlerFunc]:
    """Register a callback handler via decorator."""

    def decorator(func: HandlerFunc) -> HandlerFunc:
        _global_router.add_callback(pattern, func, name=name)
        return func

    return decorator


def message(
    pattern: str, name: str | None = None
) -> Callable[[HandlerFunc], HandlerFunc]:
    """Register a message handler via decorator."""

    def decorator(func: HandlerFunc) -> HandlerFunc:
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
