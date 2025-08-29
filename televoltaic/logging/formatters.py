"""Built-in logging formatters for TeleVoltaic."""

from __future__ import annotations

import logging
import time


class ConciseFormatter(logging.Formatter):
    """Simple concise or verbose formatter depending on debug flag."""

    default_fmt = "[%(levelname).1s %(asctime)s %(name)s] %(message)s"
    debug_fmt = (
        "[%(levelname)s %(asctime)s %(name)s "
        "%(module)s:%(lineno)d] %(message)s"
    )
    datefmt = "%H:%M:%S"

    def __init__(self, debug: bool = False) -> None:
        """Configure internal format string based on debug flag."""
        fmt = self.debug_fmt if debug else self.default_fmt
        super().__init__(fmt=fmt, datefmt=self.datefmt)

    def formatTime(  # type: ignore[override]
        self,
        record: logging.LogRecord,
        datefmt: str | None = None,
    ) -> str:
        """Format time with millisecond precision."""
        if datefmt:
            return super().formatTime(record, datefmt)
        ct = self.converter(record.created)
        return time.strftime(self.datefmt, ct) + f".{int(record.msecs):03d}"


class KeyValueFormatter(logging.Formatter):
    """Format logs as lightweight key=value pairs."""

    def format(self, record: logging.LogRecord) -> str:  # noqa: D102
        base: dict[str, object] = {
            "lvl": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            base["exc"] = self.formatException(record.exc_info).splitlines()[
                -1
            ]
        if hasattr(record, "route"):
            base["route"] = record.route  # type: ignore[attr-defined]
        if hasattr(record, "kind"):
            base["kind"] = record.kind  # type: ignore[attr-defined]
        if hasattr(record, "duration_ms"):
            base["dur_ms"] = (
                f"{record.duration_ms:.2f}"  # type: ignore[attr-defined]
            )
        parts = [f"{k}={v}" for k, v in base.items()]
        return " ".join(parts)
