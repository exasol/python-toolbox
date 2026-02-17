import logging
import os

import structlog

log_level = os.getenv("LOG_LEVEL", "INFO").upper()

structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, log_level))
)
