"""Lightweight model and field abstractions for TeleVoltaic."""

from __future__ import annotations

from typing import Any


class Field:
    """Represent a generic field definition.

    Future versions can extend type coercion, validation and
    serialization logic.
    """

    def __init__(self, field_type: type = str, default: Any = None) -> None:
        """Initialize a Field with a Python type and optional default."""
        self.field_type = field_type
        self.default = default

    def to_python(self, value: Any) -> Any:
        """Convert raw value to Python type."""
        if value is None:
            return self.default
        try:
            return self.field_type(value)
        except Exception:
            return value


class ModelMeta(type):
    """Collect Field attributes declared on the class."""

    def __new__(
        mcls,
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, Any],
    ) -> ModelMeta:
        """Build new model class collecting Field instances."""
        fields: dict[str, Field] = {}
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                fields[key] = value
        attrs["_meta_fields"] = fields
        return super().__new__(mcls, name, bases, attrs)


class Model(metaclass=ModelMeta):
    """Base model class for TeleVoltaic API-bound entities."""

    _meta_fields: dict[str, Field]

    def __init__(self, **kwargs: Any) -> None:
        """Assign fields from provided keyword arguments."""
        for field_name, field_obj in self._meta_fields.items():
            setattr(
                self,
                field_name,
                kwargs.get(field_name, field_obj.default),
            )

    def to_dict(self) -> dict[str, Any]:
        """Serialize model to a dictionary."""
        data: dict[str, Any] = {}
        for name, field_obj in self._meta_fields.items():
            del field_obj  # Avoid unused variable (explicit discard).
            data[name] = getattr(self, name)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Model:
        """Instantiate model from a dictionary."""
        return cls(**data)

    def __repr__(self) -> str:
        """Return developer-friendly representation."""
        parts = []
        for k in self._meta_fields:
            parts.append(f"{k}={getattr(self, k)!r}")
        joined = ", ".join(parts)
        return f"<{self.__class__.__name__} {joined}>"
