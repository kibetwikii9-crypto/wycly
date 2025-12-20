"""Request context for structured logging with request IDs.

This module provides request ID tracking using contextvars for async-safe
request context management. Each request gets a unique ID that is logged
throughout the request lifecycle.
"""
import contextvars
import uuid
from typing import Optional

# Context variable for request ID (async-safe)
_request_id: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "request_id", default=None
)


def get_request_id() -> Optional[str]:
    """Get the current request ID from context."""
    return _request_id.get()


def set_request_id(request_id: Optional[str] = None) -> str:
    """
    Set a request ID in the current context.
    
    If no request_id is provided, generates a new UUID.
    
    Args:
        request_id: Optional request ID string. If None, generates a new UUID.
    
    Returns:
        The request ID (newly generated or provided)
    """
    if request_id is None:
        request_id = str(uuid.uuid4())[:8]  # Short ID for readability
    
    _request_id.set(request_id)
    return request_id


def clear_request_id() -> None:
    """Clear the request ID from context."""
    _request_id.set(None)



