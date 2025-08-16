import logging
import sys
from typing import Literal
from rich.logging import RichHandler

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def setup_logging(
    level: LogLevel = "INFO",
    use_rich: bool | None = None,
) -> None:
    """
    Configure root logger once (scripts should call this).
    Utilities should NOT call this.

    - If Rich is installed and use_rich is True/None => pretty, color logs.
    - Otherwise => plain stderr logs.
    """
    root = logging.getLogger()
    root.handlers.clear()  # avoid duplicate messages if called again
    root.setLevel(level)

    if use_rich:
        handler = RichHandler(
            rich_tracebacks=True,
            show_time=True,
            show_level=True,
            show_path=False,
            markup=True,         # allow [bold] etc. in messages if you want
        )
        # With RichHandler, keep formatter minimal—Rich renders time/level nicely.
        formatter = logging.Formatter("%(name)s | %(message)s")
        handler.setFormatter(formatter)
    else:
        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)

    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
