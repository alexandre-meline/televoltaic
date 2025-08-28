"""Application configuration system for TeleVoltaic."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AppConfig:
    """Represent application configuration.

    Inspired by Django's AppConfig. Each app subclasses this to
    register handlers, middleware and models.
    """

    name: str
    verbose_name: str | None = None
    default: bool = False
    handlers: list[Any] = field(default_factory=list)
    middleware: list[str] = field(default_factory=list)
    models: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Finalize initialization after dataclass auto __init__."""
        if self.verbose_name is None:
            self.verbose_name = self.name.title()

    def ready(self) -> None:
        """Execute app bootstrap hook (override in subclasses)."""
        return None
