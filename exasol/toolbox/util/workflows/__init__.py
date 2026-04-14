import structlog

from exasol.toolbox import log_level

logger = structlog.get_logger(__name__)

if log_level == "DEBUG":
    logger = logger.bind(subsystem="workflows")
