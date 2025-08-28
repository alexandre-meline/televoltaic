"""Route dispatcher that matches an Update to a single pattern."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from .api import BasePattern

logger = logging.getLogger("televoltaic.routing")


@dataclass(slots=True)
class MatchResult:
    """Store a successful route match."""

    pattern: BasePattern
    handler: Any
    match: Any | None = None


class Dispatcher:
    """Perform matching of an update against registered patterns."""

    def __init__(self, patterns: list[BasePattern]) -> None:
        """Initialize dispatcher with preprocessed patterns."""
        self.patterns = patterns
        # Pre-compile regex patterns
        for p in self.patterns:
            p.compile()

    def match(self, update: Any) -> MatchResult | None:
        """Return first matching route or None."""
        # Extract features
        text = getattr(getattr(update, "message", None), "text", None)
        cmd: str | None = None
        if text and text.startswith("/"):
            cmd = text.lstrip("/").split()[0]

        cb_query = getattr(update, "callback_query", None)
        cb_data = getattr(cb_query, "data", None)

        # Priority 1: command
        if cmd:
            for p in self.patterns:
                if p.kind == "command" and p.pattern == cmd:
                    handler = p.load_handler()
                    return MatchResult(pattern=p, handler=handler)

        # Priority 2: callback
        if cb_data:
            for p in self.patterns:
                if p.kind == "callback":
                    assert p._compiled  # compiled earlier
                    m = p._compiled.match(cb_data)
                    if m:
                        handler = p.load_handler()
                        return MatchResult(pattern=p, handler=handler, match=m)

        # Priority 3: message
        if text:
            for p in self.patterns:
                if p.kind == "message":
                    assert p._compiled
                    m = p._compiled.search(text)
                    if m:
                        handler = p.load_handler()
                        return MatchResult(pattern=p, handler=handler, match=m)

        return None
