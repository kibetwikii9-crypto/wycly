"""Rule-based AI brain for generating responses based on detected intent.

This module provides a simple rule-based system that:
- Detects user intent from message text
- Uses conversation memory to provide context-aware responses
- Returns appropriate responses based on intent and memory
- Can be easily replaced with GPT/LLM later

The brain is designed to be a drop-in replacement for AI services,
maintaining the same interface while using rule-based logic.
"""
import logging
from enum import Enum
from typing import Optional

from app.schemas import NormalizedMessage
from app.services.memory import get_memory, update_memory
from app.services.knowledge_service import find_answer, load_knowledge
from app.services.edge_case_handler import (
    is_spam,
    validate_message_length,
    is_emoji_or_symbol_only,
    track_unknown_intent,
    get_unknown_intent_count,
    is_unsupported_action,
)

log = logging.getLogger(__name__)


class Intent(str, Enum):
    """Supported intent categories for rule-based responses."""

    GREETING = "greeting"
    HELP = "help"
    PRICING = "pricing"
    HUMAN = "human"
    UNKNOWN = "unknown"


def detect_intent(message: NormalizedMessage) -> Intent:
    """
    Detect user intent from message text using keyword matching.

    Intent detection logic:
    - Checks message text for keywords associated with each intent
    - Returns the first matching intent (priority order matters)
    - Falls back to UNKNOWN if no intent matches

    Args:
        message: Normalized message from any platform

    Returns:
        Detected intent (greeting, help, pricing, human, or unknown)
        Always returns a valid Intent, never None

    Error Handling:
        - Handles empty or None message_text
        - Handles non-string message_text
        - Always returns UNKNOWN on errors (never crashes)
    """
    # Safe default
    default_intent = Intent.UNKNOWN

    try:
        # Validate input
        if not message or not hasattr(message, "message_text"):
            log.warning("detect_intent received invalid message")
            return default_intent

        message_text = message.message_text
        if not message_text:
            return default_intent

        # Ensure message_text is a string
        if not isinstance(message_text, str):
            try:
                message_text = str(message_text)
            except Exception:
                log.warning(f"Could not convert message_text to string: {type(message_text)}")
                return default_intent

        message_lower = message_text.lower().strip()
        
        # If message is empty after processing, return UNKNOWN
        if not message_lower:
            return default_intent

        # Priority order matters - check more specific intents first

        # Check for human/agent requests
        try:
            human_keywords = [
                "agent",
                "human",
                "talk to someone",
                "speak to someone",
                "real person",
                "representative",
                "support agent",
                "customer service",
            ]
            if any(keyword in message_lower for keyword in human_keywords):
                return Intent.HUMAN
        except Exception as e:
            log.warning(f"Error checking human keywords: {e}")

        # Check for help/support requests
        try:
            help_keywords = [
                "help",
                "support",
                "what can you do",
                "what do you do",
                "how can you help",
                "assist",
                "guide",
                "instructions",
            ]
            if any(keyword in message_lower for keyword in help_keywords):
                return Intent.HELP
        except Exception as e:
            log.warning(f"Error checking help keywords: {e}")

        # Check for pricing inquiries
        try:
            pricing_keywords = [
                "price",
                "cost",
                "pricing",
                "how much",
                "fee",
                "charge",
                "subscription",
                "plan",
                "pricing plans",
                "costs",
            ]
            if any(keyword in message_lower for keyword in pricing_keywords):
                return Intent.PRICING
        except Exception as e:
            log.warning(f"Error checking pricing keywords: {e}")

        # Check for greetings
        try:
            greeting_keywords = [
                "hi",
                "hello",
                "hey",
                "greetings",
                "good morning",
                "good afternoon",
                "good evening",
                "hi there",
                "hello there",
            ]
            if any(keyword in message_lower for keyword in greeting_keywords):
                return Intent.GREETING
        except Exception as e:
            log.warning(f"Error checking greeting keywords: {e}")

        # Default to unknown if no intent matches
        return default_intent

    except Exception as e:
        # Catch-all for any unexpected errors
        log.error(f"Unexpected error in detect_intent: {e}", exc_info=True)
        return default_intent


def generate_response_for_intent(
    intent: Intent,
    last_intent: Optional[str] = None,
    message_count: int = 0,
    unknown_intent_count: int = 0,
) -> str:
    """
    Generate a friendly response based on detected intent and conversation memory.

    Each intent has a specific, friendly response that addresses
    the user's likely need. Responses are adjusted based on:
    - Current detected intent
    - Last intent (conversation context)
    - Message count (new vs returning user)

    Responses are designed to be:
    - Friendly and welcoming
    - Helpful and informative
    - Professional yet conversational
    - Context-aware (uses memory)
    - Clear about next steps

    Args:
        intent: Detected user intent
        last_intent: Previous intent from memory (None if first message)
        message_count: Total number of messages from user
        unknown_intent_count: Count of consecutive unknown intents

    Returns:
        Friendly text response for the intent (adjusted based on memory)
    """
    # Base responses for each intent
    base_responses = {
        Intent.GREETING: "Hello! 👋 Welcome! I'm here to help you. How can I assist you today?",
        Intent.HELP: "I'm here to help! I can assist you with information about our services, pricing, and more. What would you like to know?",
        Intent.PRICING: "I'd be happy to help you with pricing information! We offer flexible plans to suit different needs. Would you like to know more about our features and which plan might work best for you?",
        Intent.HUMAN: "I understand you'd like to speak with a human agent. Let me connect you with our support team. Someone will be with you shortly!",
        Intent.UNKNOWN: "Thanks for reaching out! I'm here to help. Could you tell me a bit more about what you're looking for? I want to make sure I can assist you in the best way possible.",
    }

    # Get base response
    response = base_responses.get(intent, base_responses[Intent.UNKNOWN])

    # Adjust response based on memory context
    if last_intent is not None:
        # User has previous conversation history
        if intent == Intent.GREETING and last_intent == Intent.GREETING:
            # User greeted again - acknowledge return
            response = "Hello again! 👋 How can I help you today?"
        elif intent == last_intent:
            # Same intent repeated - acknowledge continuation
            if intent == Intent.PRICING:
                response = "Still thinking about pricing? I'm here to help! Would you like more details about our plans?"
            elif intent == Intent.HELP:
                response = "I'm still here to help! What specific information can I provide?"
        elif last_intent == Intent.PRICING and intent == Intent.HELP:
            # Transition from pricing to help - acknowledge context
            response = "I'd be happy to help! Since you were asking about pricing, would you like to know more about our features or have other questions?"
        elif last_intent == Intent.HELP and intent == Intent.PRICING:
            # Transition from help to pricing - acknowledge context
            response = "Great! Let's talk about pricing. We offer flexible plans to suit different needs. What would you like to know?"

    # Adjust for returning users (message_count > 1)
    if message_count > 1 and intent == Intent.GREETING:
        # Returning user greeting
        response = f"Welcome back! 👋 I remember we've chatted before. How can I assist you today?"

    # Special handling for repeated unknown intents
    if intent == Intent.UNKNOWN and unknown_intent_count >= 3:
        response = (
            "I'm having trouble understanding what you're looking for. "
            "Could you try rephrasing your question? I can help with: "
            "pricing information, getting started, features, or connecting you with support. "
            "What would be most helpful?"
        )

    return response


async def process_message(message: NormalizedMessage) -> str:
    """
    Process a normalized message and return a rule-based response with memory and knowledge.

    This function maintains the same signature as the AI layer,
    making it a drop-in replacement. It:
    1. Checks knowledge base for matching answer (RAG-lite)
    2. Reads conversation memory for the user
    3. Detects intent from message text
    4. Generates context-aware response based on intent, memory, and knowledge
    5. Updates memory with new intent
    6. Returns friendly, helpful response

    IMPORTANT: This function ALWAYS returns a non-empty string.
    All errors are caught and handled gracefully with safe fallbacks.

    Args:
        message: Normalized message from any platform (Telegram, WhatsApp, Instagram)

    Returns:
        Friendly text response based on detected intent, memory, and knowledge (never None or empty string)

    Error Handling:
        - Knowledge base failures → Fall back to intent-based responses
        - Memory failures → Reset memory and continue
        - Intent detection failures → Use UNKNOWN intent
        - Response generation failures → Use safe default
        - Memory update failures → Log but continue
    """
    # Safe default response
    SAFE_DEFAULT = "I'm here to help! How can I assist you today?"

    # Validate input
    if not message or not hasattr(message, "message_text"):
        log.warning("ai_brain.process_message received invalid message")
        return SAFE_DEFAULT

    if not message.message_text or not message.message_text.strip():
        log.warning("ai_brain.process_message received empty message text")
        return SAFE_DEFAULT

    if not message.user_id:
        log.warning("ai_brain.process_message received message with no user_id")
        return SAFE_DEFAULT

    # Edge Case 1: Check for spam (rapid repeated messages)
    try:
        is_spam_detected, spam_reason = is_spam(message.user_id)
        if is_spam_detected:
            log.warning(f"spam_detected user_id={message.user_id} reason={spam_reason}")
            return (
                "I notice you're sending messages very quickly. "
                "Please slow down a bit so I can help you better! "
                "How can I assist you?"
            )
    except Exception as e:
        log.warning(f"spam_check_failed user_id={message.user_id} error={type(e).__name__}")
        # Continue processing - spam check failure shouldn't block

    # Edge Case 2: Validate message length
    try:
        is_valid_length, length_reason = validate_message_length(message.message_text)
        if not is_valid_length:
            log.warning(f"message_too_long user_id={message.user_id} reason={length_reason}")
            return (
                "Your message is quite long! Could you break it down into smaller questions? "
                "I'm here to help with specific topics like pricing, features, or getting started. "
                "What would you like to know?"
            )
    except Exception as e:
        log.warning(f"length_validation_failed user_id={message.user_id} error={type(e).__name__}")
        # Continue processing - length check failure shouldn't block

    # Edge Case 3: Check for emoji/symbol-only messages
    try:
        if is_emoji_or_symbol_only(message.message_text):
            log.info(f"emoji_only_message user_id={message.user_id}")
            return (
                "I see you sent emojis! 😊 While I love emojis, I work best with text. "
                "Could you tell me in words how I can help you today?"
            )
    except Exception as e:
        log.warning(f"emoji_check_failed user_id={message.user_id} error={type(e).__name__}")
        # Continue processing - emoji check failure shouldn't block

    # Edge Case 4: Check for unsupported actions
    try:
        is_unsupported, action_type = is_unsupported_action(message.message_text)
        if is_unsupported:
            log.info(f"unsupported_action user_id={message.user_id} action={action_type}")
            if action_type == "file_upload":
                return (
                    "I can't receive files right now, but I can help answer questions! "
                    "What information are you looking for?"
                )
            elif action_type == "video_call":
                return (
                    "I'm a text-based assistant, so I can't do video calls. "
                    "But I'm here to help with any questions you have! What can I assist you with?"
                )
            elif action_type == "payment":
                return (
                    "I can provide information about our pricing plans, but I can't process payments. "
                    "For payment questions, please visit our website or contact support. "
                    "Would you like to know more about our pricing?"
                )
            elif action_type == "account_creation":
                return (
                    "I can help you get started! For account creation, please visit our website. "
                    "I'm here to answer questions about our service. What would you like to know?"
                )
            else:
                return (
                    "I understand you're looking for help, but I can't perform that action. "
                    "I can assist with questions about pricing, features, getting started, or support. "
                    "What would be most helpful?"
                )
    except Exception as e:
        log.warning(f"unsupported_action_check_failed user_id={message.user_id} error={type(e).__name__}")
        # Continue processing - action check failure shouldn't block

    try:
        # Step 1: Check knowledge base first (RAG-lite)
        # If knowledge lookup fails, continue to intent-based response
        knowledge_answer = None
        try:
            knowledge_answer = find_answer(message.message_text)
            if knowledge_answer and isinstance(knowledge_answer, str) and knowledge_answer.strip():
                # Found valid answer in knowledge base - use it
                log.info(
                    f"knowledge_match user_id={message.user_id} "
                    f"decision_path=knowledge_base"
                )
                # Still update memory for context tracking (non-blocking)
                try:
                    intent = detect_intent(message)
                    intent_value = intent.value if hasattr(intent, "value") else "unknown"
                    update_memory(message.user_id, intent_value)
                except Exception as e:
                    log.warning(f"memory_update_failed user_id={message.user_id} error={type(e).__name__}")
                    # Continue - memory update failure doesn't block response
                
                return knowledge_answer.strip()
            else:
                log.debug(f"knowledge_no_match user_id={message.user_id}")
        except Exception as e:
            log.warning(f"knowledge_lookup_error user_id={message.user_id} error={type(e).__name__} action=fallback_to_intent")

        # Step 2: Read conversation memory for this user
        # If memory read fails, use safe defaults
        memory = {}
        last_intent = None
        message_count = 0
        unknown_intent_count = 0
        try:
            memory = get_memory(message.user_id)
            if isinstance(memory, dict):
                last_intent = memory.get("last_intent")
                message_count = memory.get("message_count", 0)
                unknown_intent_count = memory.get("unknown_intent_count", 0)
                # Validate counts are numbers
                if not isinstance(message_count, (int, float)):
                    message_count = 0
                if not isinstance(unknown_intent_count, (int, float)):
                    unknown_intent_count = 0
                log.debug(
                    f"memory_read user_id={message.user_id} "
                    f"last_intent={last_intent} message_count={message_count} "
                    f"unknown_intent_count={unknown_intent_count}"
                )
            else:
                log.warning(f"memory_invalid_format user_id={message.user_id} type={type(memory).__name__}")
                memory = {}
        except Exception as e:
            log.warning(f"memory_read_failed user_id={message.user_id} error={type(e).__name__} action=using_defaults")
            memory = {}

        # Step 3: Detect intent from message text
        # If intent detection fails, use UNKNOWN intent
        intent = Intent.UNKNOWN
        intent_value = "unknown"
        try:
            intent = detect_intent(message)
            if not isinstance(intent, Intent):
                log.warning(f"intent_invalid_type user_id={message.user_id} type={type(intent).__name__}")
                intent = Intent.UNKNOWN
            intent_value = intent.value if hasattr(intent, "value") else "unknown"
            log.info(
                f"intent_detected user_id={message.user_id} "
                f"intent={intent_value} decision_path=rule_based"
            )
        except Exception as e:
            log.warning(f"intent_detection_failed user_id={message.user_id} error={type(e).__name__} action=using_unknown")
            intent = Intent.UNKNOWN
            intent_value = "unknown"

        # Edge Case 4: Track unknown intents for special handling
        try:
            unknown_intent_count = track_unknown_intent(message.user_id, intent_value)
            log.debug(f"unknown_intent_tracked user_id={message.user_id} intent={intent_value} count={unknown_intent_count}")
        except Exception as e:
            log.warning(f"unknown_intent_tracking_failed user_id={message.user_id} error={type(e).__name__}")
            unknown_intent_count = get_unknown_intent_count(message.user_id)

        # Step 4: Generate context-aware response based on intent and memory
        # If response generation fails, use safe default
        response = SAFE_DEFAULT
        try:
            response = generate_response_for_intent(intent, last_intent, message_count, unknown_intent_count)
            if not response or not isinstance(response, str) or not response.strip():
                log.warning(f"response_generation_empty user_id={message.user_id} action=using_default")
                response = SAFE_DEFAULT
            else:
                log.debug(
                    f"response_generated user_id={message.user_id} "
                    f"intent={intent_value} response_length={len(response)}"
                )
        except Exception as e:
            log.warning(f"response_generation_failed user_id={message.user_id} error={type(e).__name__} action=using_default")
            response = SAFE_DEFAULT

        # Step 5: Update memory with new intent and increment message count
        # Memory update failures are non-blocking
        try:
            update_memory(message.user_id, intent_value)
            log.debug(f"memory_updated user_id={message.user_id} intent={intent_value} unknown_count={unknown_intent_count}")
        except Exception as e:
            log.warning(f"memory_update_failed user_id={message.user_id} error={type(e).__name__} action=continuing")
            # Continue - memory update failure doesn't block response

        # Step 6: Ensure response is never empty (final safety check)
        if not response or not isinstance(response, str) or not response.strip():
            log.warning(f"response_validation_failed user_id={message.user_id} action=using_default decision_path=fallback")
            return SAFE_DEFAULT

        log.info(
            f"ai_processing_complete user_id={message.user_id} "
            f"intent={intent_value} decision_path=rule_based"
        )
        return response.strip()

    except Exception as e:
        # Catch-all for any unexpected errors
        log.error(
            f"ai_processing_error user_id={message.user_id if message else 'unknown'} "
            f"error={type(e).__name__} message={str(e)} decision_path=fallback",
            exc_info=True
        )
        return SAFE_DEFAULT

