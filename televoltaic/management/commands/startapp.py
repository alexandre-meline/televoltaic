"""startapp command stub for TeleVoltaic."""

from __future__ import annotations

from typing import Any

from ..base import BaseCommand


class StartAppCommand(BaseCommand):
    """Create a new application inside a TeleVoltaic project."""

    help = "Generate a new app skeleton in the current project."

    def handle(self, **options: Any) -> int:
        """Execute the app creation logic (placeholder)."""
        print("startapp: not yet implemented.")
        return 0
