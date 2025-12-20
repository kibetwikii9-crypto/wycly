"""Schemas package for Pydantic models."""

# Import from the schemas.py file (not this package)
# This allows backward compatibility: from app.schemas import TelegramUpdate
import sys
import importlib.util

# Load the schemas.py file as a module
spec = importlib.util.spec_from_file_location("app.schemas_file", "app/schemas.py")
schemas_file = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schemas_file)

# Re-export everything from schemas.py
TelegramUpdate = schemas_file.TelegramUpdate
NormalizedMessage = schemas_file.NormalizedMessage
MessageChannel = schemas_file.MessageChannel

__all__ = ["TelegramUpdate", "NormalizedMessage", "MessageChannel"]

