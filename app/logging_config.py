"""Logging configuration with structured logging support.

This module configures structured logging with:
- Request ID tracking
- Readable format for local development
- Key-value pairs for easy parsing
- No sensitive data exposure
"""
import logging
import sys

from app.logging_context import get_request_id


class StructuredFormatter(logging.Formatter):
    """Formatter that includes request ID and structured key-value pairs."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with request ID and structured data."""
        # Get request ID from context
        request_id = get_request_id() or "no-request-id"
        
        # Add request_id to record for formatting
        record.request_id = request_id
        
        # Format the message with request ID
        return super().format(record)


def init_logging(level: str = "INFO") -> None:
    """
    Configure root logger with structured formatting.
    
    Log format:
        YYYY-MM-DD HH:MM:SS LEVEL    logger_name        [request_id] - message
    
    Example:
        2024-01-15 10:30:45 INFO     app.routes.telegram [a1b2c3d4] - message_received user_id=123 channel=telegram
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    handler = logging.StreamHandler(sys.stdout)
    formatter = StructuredFormatter(
        "%(asctime)s %(levelname)-8s %(name)-20s [%(request_id)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(handler)



