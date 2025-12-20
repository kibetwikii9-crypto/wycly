"""AI service module for generating text responses.

This module provides a clean abstraction layer for AI/LLM functionality.
It contains NO business logic and NO platform-specific logic.

Currently uses rule-based brain (ai_brain.py) but can be swapped
with GPT/LLM providers (OpenAI, Anthropic, etc.) without affecting business logic.

The AI module is a pure function that:
- Takes a prompt string
- Returns a text response
- Can be swapped out with any LLM provider without affecting business logic
"""
import logging

from app.schemas import NormalizedMessage
from app.services.ai_brain import process_message as rule_based_process

log = logging.getLogger(__name__)


async def generate_response(prompt: str) -> str:
    """
    Generate a text response from a prompt using rule-based brain.

    This is a pure AI abstraction function with no business logic.
    It accepts a prompt string and returns a text response.

    Currently uses rule-based intent detection and responses.
    Can be replaced with GPT/LLM by changing this function's implementation.

    IMPORTANT: This function ALWAYS returns a non-empty string.
    If any error occurs, a safe fallback message is returned.

    Args:
        prompt: The input prompt string to generate a response for

    Returns:
        Generated text response (never None or empty string)

    Example:
        >>> response = await generate_response("Hello, how are you?")
        >>> assert response and response.strip()  # Always non-empty

    Current Implementation:
        Uses rule-based brain (ai_brain.py) that:
        - Detects intent from message text
        - Returns appropriate responses based on intent
        - No external APIs required
        - Fast and reliable

    Future Implementation:
        This function can be replaced with GPT/LLM by:
        1. Importing OpenAI/Anthropic client
        2. Replacing rule-based logic with LLM API call
        3. Keeping the same function signature
        4. No changes needed to calling code (processor.py)
    """
    try:
        # Convert prompt string to NormalizedMessage for rule-based brain
        # The rule-based brain expects NormalizedMessage, but we only have prompt text
        # Create a minimal NormalizedMessage wrapper
        from datetime import datetime
        from app.schemas import MessageChannel

        # Create a temporary NormalizedMessage from prompt
        # This allows rule-based brain to work with the same interface
        temp_message = NormalizedMessage(
            channel=MessageChannel.TELEGRAM,  # Default, not used by brain
            user_id="temp",  # Not used by brain
            message_text=prompt,
            timestamp=datetime.utcnow(),
        )

        # Call rule-based brain
        response = await rule_based_process(temp_message)

        # Validate response is not empty
        if not response or not response.strip():
            log.warning("Rule-based brain returned empty response")
            return _get_fallback_response()

        return response.strip()

    except Exception as e:
        log.error(f"Error in AI generation: {e}")
        return _get_fallback_response()


def _get_fallback_response() -> str:
    """
    Get a safe fallback response when AI generation fails.

    This is an internal helper function that ensures the AI module
    always returns a non-empty string, even in error cases.

    Returns:
        Safe fallback message that is clearly identifiable
    """
    return "I'm having trouble processing your request right now. Please try again in a moment."

