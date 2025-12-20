# Edge Cases Handling Strategy

## Overview

This document outlines the edge cases identified for the SaaS chatbot system and the strategies implemented to handle them gracefully. All edge cases are handled with simple, local safeguards that don't require external services or infrastructure.

---

## Edge Cases Identified

### 1. Rapid Repeated Messages (Spam)

**Problem:**
- Users sending messages too rapidly can overwhelm the system
- May indicate automated bots or accidental rapid clicking
- Can cause performance issues and resource exhaustion

**Expected System Behavior:**
- Detect rapid message patterns
- Return a polite message asking user to slow down
- Continue processing normally after spam window expires
- System remains stable and responsive

**Implementation:**
- **Location:** `app/services/edge_case_handler.py` → `is_spam()`
- **Strategy:**
  - Track message timestamps per user in memory
  - Detect if messages are sent within 2 seconds of each other
  - Detect if more than 5 messages are sent within 10 seconds
  - Clean old timestamps automatically (sliding window)
  - Return polite response: *"I notice you're sending messages very quickly. Please slow down a bit so I can help you better! How can I assist you?"*

**Configuration:**
```python
SPAM_THRESHOLD_SECONDS = 2  # Minimum seconds between messages
SPAM_MESSAGE_LIMIT = 5  # Max messages in spam window
SPAM_WINDOW_SECONDS = 10  # Time window for spam detection
```

**Error Handling:**
- Fail-open: If spam check fails, allow message through
- Logs warnings but never blocks legitimate users
- Memory-based tracking (no external dependencies)

---

### 2. Extremely Long Messages

**Problem:**
- Messages exceeding reasonable length (e.g., 2000+ characters)
- May indicate copy-paste errors or spam
- Can cause processing delays and storage issues

**Expected System Behavior:**
- Validate message length before processing
- Return polite message asking user to break down question
- Suggest specific topics (pricing, features, getting started)
- System continues to function normally

**Implementation:**
- **Location:** `app/services/edge_case_handler.py` → `validate_message_length()`
- **Strategy:**
  - Check message length against maximum (2000 characters)
  - Return early with helpful response if too long
  - Response: *"Your message is quite long! Could you break it down into smaller questions? I'm here to help with specific topics like pricing, features, or getting started. What would you like to know?"*

**Configuration:**
```python
MAX_MESSAGE_LENGTH = 2000  # Characters
```

**Error Handling:**
- Fail-open: If validation fails, allow message through
- Logs warnings for monitoring
- Never crashes on length validation errors

---

### 3. Messages with Only Emojis or Symbols

**Problem:**
- Messages containing only emojis (😊, ❤️, 👍) or symbols (!@#$)
- No text content for intent detection
- Cannot generate meaningful responses

**Expected System Behavior:**
- Detect emoji/symbol-only messages
- Return friendly response acknowledging emojis
- Politely ask user to use text
- System continues normally

**Implementation:**
- **Location:** `app/services/edge_case_handler.py` → `is_emoji_or_symbol_only()`
- **Strategy:**
  - Check if message has any alphanumeric characters
  - If no alphanumeric characters found, treat as emoji/symbol-only
  - Response: *"I see you sent emojis! 😊 While I love emojis, I work best with text. Could you tell me in words how I can help you today?"*

**Detection Logic:**
- Remove whitespace
- Check for presence of `[a-zA-Z0-9]` characters
- If none found → emoji/symbol-only

**Error Handling:**
- Fail-open: If check fails, treat as normal message
- Logs info-level events (not errors)
- Never blocks legitimate emoji usage in text messages

---

### 4. Repeated Unknown Intents

**Problem:**
- User sends multiple messages that don't match any known intent
- System keeps returning generic "unknown" responses
- User may feel frustrated or confused

**Expected System Behavior:**
- Track consecutive unknown intents per user
- After 3 consecutive unknown intents, provide more helpful guidance
- Suggest specific topics user can ask about
- Reset count when known intent is detected

**Implementation:**
- **Location:** 
  - `app/services/edge_case_handler.py` → `track_unknown_intent()`, `get_unknown_intent_count()`
  - `app/services/memory.py` → Tracks `unknown_intent_count` in memory
  - `app/services/ai_brain.py` → Uses count in response generation
- **Strategy:**
  - Track consecutive unknown intents per user
  - After 3 consecutive unknowns, return enhanced response
  - Enhanced response: *"I'm having trouble understanding what you're looking for. Could you try rephrasing your question? I can help with: pricing information, getting started, features, or connecting you with support. What would be most helpful?"*
  - Reset count when any known intent is detected

**Configuration:**
```python
UNKNOWN_INTENT_THRESHOLD = 3  # Consecutive unknown intents before special response
```

**Error Handling:**
- Fail-open: If tracking fails, use default unknown response
- Memory-based tracking (no external dependencies)
- Never crashes on tracking errors

---

### 5. Requests for Unsupported Actions

**Problem:**
- Users request actions the bot cannot perform:
  - File uploads
  - Video calls
  - Payment processing
  - Account creation
  - Admin actions
- System should politely decline and redirect

**Expected System Behavior:**
- Detect unsupported action requests
- Return polite, helpful response explaining limitation
- Suggest alternative actions or next steps
- System continues normally

**Implementation:**
- **Location:** `app/services/edge_case_handler.py` → `is_unsupported_action()`
- **Strategy:**
  - Keyword-based detection for common unsupported actions
  - Return action-specific responses:
    - **File upload:** *"I can't receive files right now, but I can help answer questions! What information are you looking for?"*
    - **Video call:** *"I'm a text-based assistant, so I can't do video calls. But I'm here to help with any questions you have! What can I assist you with?"*
    - **Payment:** *"I can provide information about our pricing plans, but I can't process payments. For payment questions, please visit our website or contact support. Would you like to know more about our pricing?"*
    - **Account creation:** *"I can help you get started! For account creation, please visit our website. I'm here to answer questions about our service. What would you like to know?"*
    - **Generic:** *"I understand you're looking for help, but I can't perform that action. I can assist with questions about pricing, features, getting started, or support. What would be most helpful?"*

**Detected Actions:**
- `file_upload`: upload, send file, attach, share file
- `video_call`: video call, video chat, face time, video
- `payment`: pay, payment, credit card, billing, invoice, charge
- `account_creation`: create account, sign up, register, new account
- `admin_action`: delete, remove user, ban, admin, moderator

**Error Handling:**
- Fail-open: If detection fails, process as normal message
- Logs info-level events (not errors)
- Never blocks legitimate requests

---

## Integration Points

### Request Flow

1. **Webhook Entry** (`app/routes/telegram.py`)
   - Receives message
   - Normalizes message
   - Passes to processor

2. **Processor** (`app/services/processor.py`)
   - Validates message
   - Delegates to AI brain

3. **AI Brain** (`app/services/ai_brain.py`)
   - **Edge Case Checks (in order):**
     1. Spam detection
     2. Message length validation
     3. Emoji/symbol-only detection
     4. Unsupported action detection
   - If any edge case detected → Return early with appropriate response
   - Otherwise → Continue with normal processing (knowledge → intent → memory)

4. **Intent Detection** (`app/services/ai_brain.py` → `detect_intent()`)
   - Detects intent from message
   - Returns UNKNOWN if no match

5. **Response Generation** (`app/services/ai_brain.py` → `generate_response_for_intent()`)
   - Uses unknown intent count for enhanced responses
   - Generates context-aware response

6. **Memory Update** (`app/services/memory.py`)
   - Tracks unknown intent count
   - Updates last intent and message count

---

## System Stability Guarantees

### 1. Fail-Open Strategy
- All edge case checks fail-open (allow message through if check fails)
- Never blocks legitimate users due to edge case check errors
- Logs warnings for monitoring but continues processing

### 2. No External Dependencies
- All edge case handling uses in-memory data structures
- No rate-limiting services required
- No database queries for edge case checks
- Simple, fast, local safeguards

### 3. Graceful Degradation
- If spam check fails → Allow message
- If length check fails → Allow message
- If emoji check fails → Process as normal
- If unsupported action check fails → Process as normal
- If unknown intent tracking fails → Use default response

### 4. Always Respond
- System ALWAYS returns a response to the user
- Edge cases return polite, helpful responses
- Never crashes or hangs on edge case detection
- Safe defaults ensure user always receives a reply

### 5. Performance
- Edge case checks are fast (O(1) or O(n) where n is small)
- In-memory tracking (no I/O)
- Automatic cleanup of old spam timestamps
- No blocking operations

---

## Configuration

All edge case thresholds are configurable constants in `app/services/edge_case_handler.py`:

```python
MAX_MESSAGE_LENGTH = 2000  # Characters
SPAM_THRESHOLD_SECONDS = 2  # Minimum seconds between messages
SPAM_MESSAGE_LIMIT = 5  # Max messages in spam window
SPAM_WINDOW_SECONDS = 10  # Time window for spam detection
UNKNOWN_INTENT_THRESHOLD = 3  # Consecutive unknown intents before special response
```

**Adjustment Guidelines:**
- **MAX_MESSAGE_LENGTH:** Adjust based on platform limits (Telegram: 4096, WhatsApp: 4096)
- **SPAM_THRESHOLD_SECONDS:** Lower = stricter (may block fast typers), Higher = more lenient
- **SPAM_MESSAGE_LIMIT:** Adjust based on expected user behavior
- **SPAM_WINDOW_SECONDS:** Should be longer than SPAM_THRESHOLD_SECONDS
- **UNKNOWN_INTENT_THRESHOLD:** Lower = more helpful guidance, Higher = more patience

---

## Testing Scenarios

### 1. Spam Detection
- **Test:** Send 6 messages within 5 seconds
- **Expected:** 6th message triggers spam response
- **Verify:** System remains responsive, polite response sent

### 2. Long Message
- **Test:** Send message with 2500 characters
- **Expected:** Length validation triggers, helpful response sent
- **Verify:** Message not processed, user receives guidance

### 3. Emoji-Only Message
- **Test:** Send message with only "😊❤️👍"
- **Expected:** Emoji detection triggers, friendly response sent
- **Verify:** User asked to use text, system continues

### 4. Repeated Unknown Intents
- **Test:** Send 4 messages with no known keywords
- **Expected:** 4th message gets enhanced guidance response
- **Verify:** Count resets when known intent detected

### 5. Unsupported Action
- **Test:** Send "I want to upload a file"
- **Expected:** Unsupported action detected, helpful response sent
- **Verify:** User redirected to alternative actions

---

## Monitoring and Logging

All edge cases are logged with structured logging:

- **Spam:** `spam_detected user_id=X reason=Y`
- **Long Message:** `message_too_long user_id=X reason=Y`
- **Emoji-Only:** `emoji_only_message user_id=X`
- **Unknown Intent:** `unknown_intent_tracked user_id=X intent=unknown count=Y`
- **Unsupported Action:** `unsupported_action user_id=X action=Y`

**Log Levels:**
- **INFO:** Normal edge case detection (emoji, unsupported action)
- **WARNING:** Spam, long messages, repeated unknowns
- **DEBUG:** Detailed tracking information

---

## Summary

✅ **All 5 edge cases identified and handled**
✅ **System remains stable under all edge cases**
✅ **Users always receive polite, helpful responses**
✅ **No external services or infrastructure required**
✅ **Simple, local safeguards only**
✅ **Fail-open strategy ensures no false positives**
✅ **Comprehensive logging for monitoring**

The system is production-ready and handles all identified edge cases gracefully while maintaining stability and user experience.


