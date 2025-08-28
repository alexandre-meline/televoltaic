"""Custom exception classes for TeleVoltaic framework."""

from __future__ import annotations


class TeleVoltaicError(Exception):
    """Base exception for all TeleVoltaic errors."""


class ConfigurationError(TeleVoltaicError):
    """Raised when configuration is invalid or missing."""


class AppRegistryError(TeleVoltaicError):
    """Raised when an application cannot be registered or found."""


class RoutingError(TeleVoltaicError):
    """Raised when a command or pattern cannot be resolved."""
