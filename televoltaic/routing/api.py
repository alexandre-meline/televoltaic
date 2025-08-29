"""Declarative routing API inspired by Django's URL configuration."""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from importlib import import_module
from typing import Any, cast

Handler = Callable[..., Any]


class HandlerLoaderError(RuntimeError):
    """Raised when a handler cannot be imported."""


class RouteNameConflictError(RuntimeError):
    """Raised when a named route collides with an existing name."""


@dataclass(slots=True)
class BasePattern:
    """Base pattern representation for a Telegram update route."""

    kind: str  # command|callback|message
    pattern: str  # command name or regex
    handler_path: str  # dotted import path to handler callable
    name: str | None = None
    namespace: str | None = None

    _compiled: Any | None = None
    _handler: Handler | None = None

    def compile(self) -> None:
        """Compile regex pattern for callback/message kinds."""
        if self.kind in ("callback", "message") and self._compiled is None:
            self._compiled = re.compile(self.pattern)

    def load_handler(self) -> Handler:
        """Import and cache the handler callable."""
        if self._handler is not None:
            return self._handler
        module_path, _, attr = self.handler_path.rpartition(".")
        if not module_path or not attr:
            raise HandlerLoaderError(
                f"Invalid handler path '{self.handler_path}'."
            )
        try:
            module = import_module(module_path)
        except Exception as exc:  # pragma: no cover
            raise HandlerLoaderError(
                f"Cannot import module '{module_path}' for handler "
                f"'{self.handler_path}'."
            ) from exc
        handler_obj = getattr(module, attr, None)
        if handler_obj is None:
            raise HandlerLoaderError(
                f"Attribute '{attr}' not found in '{module_path}'."
            )
        if not callable(handler_obj):
            raise HandlerLoaderError(
                f"Handler '{self.handler_path}' is not callable."
            )
        self._handler = cast(Handler, handler_obj)
        return self._handler

    @property
    def fq_name(self) -> str | None:
        """Return fully qualified route name with namespace."""
        if self.name is None:
            return None
        if self.namespace:
            return f"{self.namespace}:{self.name}"
        return self.name


@dataclass(slots=True)
class Include:
    """Represent inclusion of another patterns list."""

    target: str
    namespace: str | None = None


def command(
    name_or_pattern: str,
    handler: str,
    name: str | None = None,
    namespace: str | None = None,
) -> BasePattern:
    """Create a command pattern (command name without slash)."""
    return BasePattern(
        kind="command",
        pattern=name_or_pattern,
        handler_path=handler,
        name=name,
        namespace=namespace,
    )


def callback(
    regex: str,
    handler: str,
    name: str | None = None,
    namespace: str | None = None,
) -> BasePattern:
    """Create a callback data pattern (regex)."""
    return BasePattern(
        kind="callback",
        pattern=regex,
        handler_path=handler,
        name=name,
        namespace=namespace,
    )


def message(
    regex: str,
    handler: str,
    name: str | None = None,
    namespace: str | None = None,
) -> BasePattern:
    """Create a message text pattern (regex)."""
    return BasePattern(
        kind="message",
        pattern=regex,
        handler_path=handler,
        name=name,
        namespace=namespace,
    )


def include(target: str, namespace: str | None = None) -> Include:
    """Include another patterns module."""
    return Include(target=target, namespace=namespace)


def patterns(
    namespace: str | None, *entries: BasePattern | Include
) -> list[BasePattern | Include]:
    """Return list of provided patterns preserving order.

    Namespace is applied only to direct BasePattern children lacking one.
    """
    out: list[BasePattern | Include] = []
    for entry in entries:
        if isinstance(entry, BasePattern):
            if namespace and entry.namespace is None:
                entry.namespace = namespace
        out.append(entry)
    return out


def flatten(
    entries: Iterable[BasePattern | Include],
    *,
    _seen: set[str] | None = None,
) -> list[BasePattern]:
    """Flatten nested include structures to a flat pattern list."""
    if _seen is None:
        _seen = set()
    flat: list[BasePattern] = []
    for entry in entries:
        if isinstance(entry, BasePattern):
            flat.append(entry)
            continue
        if entry.target in _seen:
            continue
        _seen.add(entry.target)
        module_ref, attr = (
            entry.target.split(":")[0],
            (
                entry.target.split(":")[1]
                if ":" in entry.target
                else "urlpatterns"
            ),
        )
        module = import_module(module_ref)
        target_patterns = getattr(module, attr, None)
        if target_patterns is None:
            raise RuntimeError(
                f"Included module '{entry.target}' missing '{attr}'."
            )
        nested: list[BasePattern | Include] = []
        for p in target_patterns:
            if isinstance(p, BasePattern):
                if entry.namespace and p.namespace is None:
                    p.namespace = entry.namespace
                nested.append(p)
            else:
                # type: ignore[attr-defined]
                if entry.namespace and p.namespace is None:
                    p.namespace = entry.namespace  # type: ignore[attr-defined]
                nested.append(p)
        flat.extend(flatten(nested, _seen=_seen))
    return flat


__all__ = [
    "BasePattern",
    "Include",
    "command",
    "callback",
    "message",
    "include",
    "patterns",
    "flatten",
    "HandlerLoaderError",
    "RouteNameConflictError",
]
