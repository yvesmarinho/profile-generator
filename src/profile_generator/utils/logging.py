"""Structured logging setup using structlog.

This module configures structlog for JSON-formatted logging with appropriate
processors for development and production environments.
"""

import logging
import sys

import structlog

from profile_generator.models.config import LogLevel


def setup_logging(log_level: LogLevel = LogLevel.INFO) -> None:
    """Configure structured logging with structlog.

    Sets up JSON-formatted logging with appropriate processors for parsing and analysis.
    Configures both structlog and standard library logging to work together.

    Args:
        log_level: Logging level (debug, info, warning, error)

    Example:
        >>> from profile_generator.models.config import LogLevel
        >>> setup_logging(LogLevel.DEBUG)
        >>> log = structlog.get_logger()
        >>> log.info("scan_started", path="/projects", count=5)
    """
    # Map LogLevel enum to logging module levels
    level_map = {
        LogLevel.DEBUG: logging.DEBUG,
        LogLevel.INFO: logging.INFO,
        LogLevel.WARNING: logging.WARNING,
        LogLevel.ERROR: logging.ERROR,
    }
    stdlib_level = level_map[log_level]

    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=stdlib_level,
    )

    # Configure structlog with JSON output
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
