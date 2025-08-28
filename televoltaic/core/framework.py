"""Core framework bootstrap logic for TeleVoltaic."""

from __future__ import annotations

from dataclasses import dataclass, field

from ..routing.patterns import Router
from .apps import AppConfig
from .exceptions import AppRegistryError, ConfigurationError


@dataclass
class TeleVoltaicSettings:
    """Represent in-memory settings used by the framework."""

    installed_apps: list[str] = field(default_factory=list)
    debug: bool = False
    telegram_token: str | None = None


class AppRegistry:
    """Maintain references to loaded applications."""

    def __init__(self) -> None:
        """Initialize empty registry."""
        self._apps: dict[str, AppConfig] = {}

    def register(self, app_config: AppConfig) -> None:
        """Register a single AppConfig instance."""
        if app_config.name in self._apps:
            raise AppRegistryError(
                f"App '{app_config.name}' " "is already registered."
            )
        self._apps[app_config.name] = app_config

    def get(self, name: str) -> AppConfig:
        """Retrieve an app by name."""
        try:
            return self._apps[name]
        except KeyError as exc:
            raise AppRegistryError(f"App '{name}' not found.") from exc

    def all(self) -> list[AppConfig]:
        """Return all registered applications."""
        return list(self._apps.values())


class TeleVoltaic:
    """Main entry point for initializing the TeleVoltaic framework."""

    def __init__(self, settings: TeleVoltaicSettings) -> None:
        """Create TeleVoltaic instance with provided settings."""
        self.settings = settings
        self.registry = AppRegistry()
        self.router = Router()
        self._initialized = False

    def load_apps(self) -> None:
        """Import and register each installed application."""
        for dotted_path in self.settings.installed_apps:
            module_path, _, attr = dotted_path.partition(":")
            if not attr:
                raise ConfigurationError(
                    f"Invalid app reference '{dotted_path}'. "
                    "Expected 'module:ClassName'."
                )
            module = __import__(module_path, fromlist=[attr])
            app_config_cls = getattr(module, attr, None)
            is_cls = isinstance(app_config_cls, type)
            if app_config_cls is None or not is_cls:
                raise ConfigurationError(
                    f"Attribute '{attr}' not found or not a class in "
                    f"'{module_path}'."
                )
            app_config: AppConfig = app_config_cls()  # type: ignore[call-arg]
            self.registry.register(app_config)

    def collect_routes(self) -> None:
        """Collect handler definitions from each app."""
        from ..routing.patterns import _global_router

        for app in self.registry.all():
            # Import handlers module to trigger decorator registration
            handlers_module_path = f"{app.name}.handlers"
            try:
                __import__(handlers_module_path, fromlist=[""])
            except ImportError:
                # No handlers.py in this app
                continue

        # Copy routes from global router to instance router
        self.router.commands.update(_global_router.commands)
        self.router.callbacks.extend(_global_router.callbacks)
        self.router.messages.extend(_global_router.messages)

    def initialize(self) -> None:
        """Initialize the framework lifecycle."""
        if self._initialized:
            return
        self.load_apps()
        self.collect_routes()
        self._initialized = True

    def is_ready(self) -> bool:
        """Return True if framework finished initialization."""
        return self._initialized
