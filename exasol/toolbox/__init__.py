import logging
import os
from importlib.metadata import version

import structlog
from structlog.dev import ConsoleRenderer
from structlog.processors import (
    TimeStamper,
    add_log_level,
    format_exc_info,
)

__version__ = version("exasol-toolbox")

log_level = os.getenv("LOG_LEVEL", "INFO").upper()

structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, log_level)),
    processors=[
        # 1. Enrich the data first
        add_log_level,
        TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        # 2. Handle exceptions
        format_exc_info,
        # 3. Render
        ConsoleRenderer(pad_level=False),
    ],
)
