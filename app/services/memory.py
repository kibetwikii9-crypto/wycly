"""In-memory conversation memory for tracking user interactions.

This module provides a simple in-memory store for conversation context.
Memory is stored per user_id and tracks conversation history.

Currently uses a dictionary (in-memory) but can be replaced with
Redis or a database later without changing the interface.
"""
import logging
from typing import Dict, Optional

log = logging.getLogger(__name__)

# In-memory store: {user_id: {last_intent: str, message_count: int, unknown_intent_count: int}}
_memory_store: Dict[str, Dict[str, any]] = {}


def get_memory(user_id: str) -> Dict[str, any]:
    """
    Get conversation memory for a user.

    Returns memory dictionary with:
    - last_intent: The last detected intent for this user
    - message_count: Total number of messages from this user

    If user has no memory, returns default values.

    Args:
        user_id: Platform-specific user identifier

    Returns:
        Dictionary with memory data:
        {
            "last_intent": str or None,
            "message_count": int
        }
        Always returns a valid dictionary, never None

    Error Handling:
        - Handles None or invalid user_id
        - Handles corrupted memory entries
        - Always returns valid default structure
    """
    # Safe default
    default_memory = {
        "last_intent": None,
        "message_count": 0,
        "unknown_intent_count": 0,
    }

    try:
        # Validate user_id
        if not user_id or not isinstance(user_id, str):
            log.warning(f"Invalid user_id provided to get_memory: {type(user_id)}")
            return default_memory.copy()

        if user_id not in _memory_store:
            return default_memory.copy()

        # Get memory and validate structure
        memory = _memory_store.get(user_id)
        if not isinstance(memory, dict):
            log.warning(f"Memory entry for user {user_id} is not a dict, resetting")
            _memory_store[user_id] = default_memory.copy()
            return default_memory.copy()

        # Validate and fix memory structure
        result = memory.copy()
        if "last_intent" not in result:
            result["last_intent"] = None
        if "message_count" not in result or not isinstance(result["message_count"], (int, float)):
            result["message_count"] = 0
        if "unknown_intent_count" not in result or not isinstance(result["unknown_intent_count"], (int, float)):
            result["unknown_intent_count"] = 0

        return result

    except Exception as e:
        log.error(f"Error getting memory for user {user_id}: {e}", exc_info=True)
        return default_memory.copy()


def update_memory(user_id: str, intent: str) -> None:
    """
    Update conversation memory for a user.

    Updates:
    - last_intent: Sets to the provided intent
    - message_count: Increments by 1

    Args:
        user_id: Platform-specific user identifier
        intent: Detected intent string (e.g., "greeting", "pricing")
        unknown_intent_count: Count of consecutive unknown intents (optional)

    Error Handling:
        - Handles None or invalid user_id
        - Handles None or invalid intent
        - Resets corrupted memory entries
        - Never raises exceptions (logs errors instead)
    """
    try:
        # Validate user_id
        if not user_id or not isinstance(user_id, str):
            log.warning(f"Invalid user_id provided to update_memory: {type(user_id)}")
            return

        # Validate intent
        if intent is None:
            intent = "unknown"
        if not isinstance(intent, str):
            try:
                intent = str(intent)
            except Exception:
                log.warning(f"Could not convert intent to string: {type(intent)}")
                intent = "unknown"

        # Initialize memory if needed
        if user_id not in _memory_store:
            _memory_store[user_id] = {
                "last_intent": None,
                "message_count": 0,
                "unknown_intent_count": 0,
            }

        # Validate existing memory structure
        if not isinstance(_memory_store[user_id], dict):
            log.warning(f"Memory entry for user {user_id} is corrupted, resetting")
            _memory_store[user_id] = {
                "last_intent": None,
                "message_count": 0,
                "unknown_intent_count": 0,
            }

        # Update memory safely
        _memory_store[user_id]["last_intent"] = intent
        
        # Safely increment message_count
        current_count = _memory_store[user_id].get("message_count", 0)
        if isinstance(current_count, (int, float)):
            _memory_store[user_id]["message_count"] = int(current_count) + 1
        else:
            log.warning(f"Invalid message_count for user {user_id}, resetting to 1")
            _memory_store[user_id]["message_count"] = 1

        # Update unknown_intent_count based on intent
        # If intent is "unknown", increment count; otherwise reset to 0
        if intent == "unknown":
            current_unknown = _memory_store[user_id].get("unknown_intent_count", 0)
            if isinstance(current_unknown, (int, float)):
                _memory_store[user_id]["unknown_intent_count"] = int(current_unknown) + 1
            else:
                _memory_store[user_id]["unknown_intent_count"] = 1
        else:
            # Reset unknown count when a known intent is detected
            _memory_store[user_id]["unknown_intent_count"] = 0

    except Exception as e:
        log.error(f"Error updating memory for user {user_id}: {e}", exc_info=True)
        # Don't raise - memory update failures shouldn't crash the system


def clear_memory(user_id: str) -> None:
    """
    Clear conversation memory for a user.

    Useful for testing or resetting user context.

    Args:
        user_id: Platform-specific user identifier
    """
    if user_id in _memory_store:
        del _memory_store[user_id]


def get_all_memory() -> Dict[str, Dict[str, any]]:
    """
    Get all conversation memory (for debugging/admin purposes).

    Returns:
        Dictionary of all user memories
    """
    return _memory_store.copy()

