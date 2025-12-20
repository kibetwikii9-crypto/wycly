"""Edge case handler for spam, long messages, and other edge cases.

This module provides simple, local safeguards for handling edge cases
without external services or infrastructure.
"""
import logging
import re
import time
from typing import Dict, Optional, Tuple

log = logging.getLogger(__name__)

# Configuration constants
MAX_MESSAGE_LENGTH = 2000  # Characters
SPAM_THRESHOLD_SECONDS = 2  # Minimum seconds between messages
SPAM_MESSAGE_LIMIT = 5  # Max messages in spam window
SPAM_WINDOW_SECONDS = 10  # Time window for spam detection
UNKNOWN_INTENT_THRESHOLD = 3  # Consecutive unknown intents before special response

# In-memory spam tracking: {user_id: [timestamps]}
_spam_tracker: Dict[str, list] = {}

# Unknown intent tracking: {user_id: count}
_unknown_intent_tracker: Dict[str, int] = {}


def is_spam(user_id: str) -> Tuple[bool, Optional[str]]:
    """
    Check if user is sending messages too rapidly (spam detection).

    Simple rate limiting: Tracks message timestamps per user and detects
    if messages are sent too rapidly.

    Args:
        user_id: Platform-specific user identifier

    Returns:
        Tuple of (is_spam: bool, reason: Optional[str])
        - is_spam: True if spam detected, False otherwise
        - reason: Human-readable reason if spam detected, None otherwise
    """
    try:
        if not user_id or not isinstance(user_id, str):
            return False, None

        current_time = time.time()

        # Initialize tracker for user if needed
        if user_id not in _spam_tracker:
            _spam_tracker[user_id] = []

        # Clean old timestamps (outside spam window)
        _spam_tracker[user_id] = [
            ts for ts in _spam_tracker[user_id]
            if current_time - ts < SPAM_WINDOW_SECONDS
        ]

        # Check if too many messages in window
        if len(_spam_tracker[user_id]) >= SPAM_MESSAGE_LIMIT:
            return True, f"Too many messages ({len(_spam_tracker[user_id])}) in {SPAM_WINDOW_SECONDS} seconds"

        # Check time since last message
        if _spam_tracker[user_id]:
            time_since_last = current_time - _spam_tracker[user_id][-1]
            if time_since_last < SPAM_THRESHOLD_SECONDS:
                return True, f"Messages sent too rapidly ({time_since_last:.2f}s apart)"

        # Add current message timestamp
        _spam_tracker[user_id].append(current_time)

        return False, None

    except Exception as e:
        log.warning(f"spam_check_error user_id={user_id} error={type(e).__name__}")
        return False, None  # Fail open - don't block on spam check errors


def validate_message_length(message_text: str) -> Tuple[bool, Optional[str]]:
    """
    Validate message length is within acceptable limits.

    Args:
        message_text: Message text to validate

    Returns:
        Tuple of (is_valid: bool, reason: Optional[str])
        - is_valid: True if message is acceptable length, False otherwise
        - reason: Human-readable reason if invalid, None otherwise
    """
    try:
        if not message_text:
            return False, "Message is empty"

        if not isinstance(message_text, str):
            return False, "Message is not a string"

        length = len(message_text)
        if length > MAX_MESSAGE_LENGTH:
            return False, f"Message too long ({length} characters, max {MAX_MESSAGE_LENGTH})"

        return True, None

    except Exception as e:
        log.warning(f"message_length_validation_error error={type(e).__name__}")
        return True, None  # Fail open - allow message if validation fails


def is_emoji_or_symbol_only(message_text: str) -> bool:
    """
    Check if message contains only emojis, symbols, or whitespace.

    Args:
        message_text: Message text to check

    Returns:
        True if message is only emojis/symbols, False otherwise
    """
    try:
        if not message_text or not isinstance(message_text, str):
            return False

        # Remove whitespace
        text_no_whitespace = message_text.strip()

        if not text_no_whitespace:
            return False  # Empty after whitespace removal

        # Check if message has any alphanumeric characters
        has_alphanumeric = bool(re.search(r'[a-zA-Z0-9]', text_no_whitespace))

        # If no alphanumeric characters, it's likely emoji/symbol only
        return not has_alphanumeric

    except Exception as e:
        log.warning(f"emoji_check_error error={type(e).__name__}")
        return False  # Fail open - treat as normal message


def track_unknown_intent(user_id: str, intent: str) -> int:
    """
    Track consecutive unknown intents for a user.

    Args:
        user_id: Platform-specific user identifier
        intent: Detected intent

    Returns:
        Count of consecutive unknown intents
    """
    try:
        if not user_id or not isinstance(user_id, str):
            return 0

        if intent == "unknown":
            # Increment unknown count
            _unknown_intent_tracker[user_id] = _unknown_intent_tracker.get(user_id, 0) + 1
        else:
            # Reset count on any known intent
            _unknown_intent_tracker[user_id] = 0

        return _unknown_intent_tracker.get(user_id, 0)

    except Exception as e:
        log.warning(f"unknown_intent_tracking_error user_id={user_id} error={type(e).__name__}")
        return 0


def get_unknown_intent_count(user_id: str) -> int:
    """
    Get current count of consecutive unknown intents for a user.

    Args:
        user_id: Platform-specific user identifier

    Returns:
        Count of consecutive unknown intents
    """
    try:
        if not user_id or not isinstance(user_id, str):
            return 0
        return _unknown_intent_tracker.get(user_id, 0)
    except Exception:
        return 0


def reset_unknown_intent_count(user_id: str) -> None:
    """
    Reset unknown intent count for a user.

    Args:
        user_id: Platform-specific user identifier
    """
    try:
        if user_id in _unknown_intent_tracker:
            _unknown_intent_tracker[user_id] = 0
    except Exception:
        pass  # Non-critical, fail silently


def is_unsupported_action(message_text: str) -> Tuple[bool, Optional[str]]:
    """
    Detect requests for unsupported actions.

    Checks for common unsupported actions like:
    - File uploads
    - Video calls
    - Payment requests
    - Account creation
    - etc.

    Args:
        message_text: Message text to check

    Returns:
        Tuple of (is_unsupported: bool, action: Optional[str])
        - is_unsupported: True if unsupported action detected
        - action: Type of unsupported action detected
    """
    try:
        if not message_text or not isinstance(message_text, str):
            return False, None

        message_lower = message_text.lower().strip()

        # Unsupported action patterns
        unsupported_patterns = {
            "file_upload": ["upload", "send file", "attach", "share file"],
            "video_call": ["video call", "video chat", "face time", "video"],
            "payment": ["pay", "payment", "credit card", "billing", "invoice", "charge"],
            "account_creation": ["create account", "sign up", "register", "new account"],
            "admin_action": ["delete", "remove user", "ban", "admin", "moderator"],
        }

        for action_type, keywords in unsupported_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                return True, action_type

        return False, None

    except Exception as e:
        log.warning(f"unsupported_action_check_error error={type(e).__name__}")
        return False, None  # Fail open

