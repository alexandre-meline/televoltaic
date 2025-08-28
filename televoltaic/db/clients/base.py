"""Base client protocol stubs for TeleVoltaic."""

from __future__ import annotations

from typing import Any, Protocol


class BaseClient(Protocol):
    """Protocol representing basic CRUD operations."""

    async def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Create a resource."""
        ...

    async def retrieve(self, ident: str | int) -> dict[str, Any]:
        """Retrieve a resource by identifier."""
        ...

    async def update(
        self,
        ident: str | int,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Update a resource."""
        ...

    async def delete(self, ident: str | int) -> bool:
        """Delete a resource."""
        ...
