import logging
import os

import structlog
from structlog.dev import ConsoleRenderer
from structlog.processors import (
    CallsiteParameter,
    CallsiteParameterAdder,
    TimeStamper,
    add_log_level,
    format_exc_info,
)

log_level = os.getenv("LOG_LEVEL", "INFO").upper()

structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, log_level)),
    processors=[
        # 1. Enrich the data first
        add_log_level,
        TimeStamper(fmt="iso"),
        CallsiteParameterAdder(
            {
                CallsiteParameter.MODULE,
                CallsiteParameter.FUNC_NAME,
            }
        ),
        # 2. Handle exceptions
        format_exc_info,
        # 3. Rendering option
        ConsoleRenderer(),
    ],
)
