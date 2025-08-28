"""Base classes for management commands (televoltaic-admin / manage.py)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseCommand(ABC):
    """Abstract base for a management command."""

    help: str = "No help text provided."

    def __init__(self) -> None:
        """Initialize command instance."""
        super().__init__()

    def add_arguments(self, parser: Any) -> None:
        """Add argparse-style arguments (override if needed)."""
        return None

    @abstractmethod
    def handle(self, **options: Any) -> int:
        """Execute the command logic; return exit code."""
        raise NotImplementedError


class CommandRegistry:
    """Registry maintaining available CLI commands."""

    def __init__(self) -> None:
        """Initialize empty command registry."""
        self._commands: dict[str, BaseCommand] = {}

    def register(self, name: str, command: BaseCommand) -> None:
        """Register a command instance under a name."""
        self._commands[name] = command

    def get(self, name: str) -> BaseCommand:
        """Retrieve a command by name."""
        try:
            return self._commands[name]
        except KeyError as exc:
            raise KeyError(f"Command '{name}' not found.") from exc

    def list(self) -> list[str]:
        """List all registered command names."""
        return list(self._commands.keys())
