# Edge Case Handling Strategy

## Overview

Comprehensive edge case handling for production-ready chatbot system. All safeguards are simple, local, and require no external services.

---

## Edge Cases Identified & Handled

### 1. **Rapid Repeated Messages (Spam)**

**Problem:**
- User sends multiple messages in rapid succession
- Can overwhelm system or create poor user experience
- May indicate bot abuse or accidental rapid clicking

**Detection:**
- Track message timestamps per user
- Detect if messages sent < 2 seconds apart
- Detect if > 5 messages in 10-second window

**Handling:**
```python
# Location: app/services/edge_case_handler.py::is_spam()
# Returns: (is_spam: bool, reason: str)
```

**Response:**
```
"I notice you're sending messages very quickly. 
Please slow down a bit so I can help you better! 
How can I assist you?"
```

**System Behavior:**
- ✅ Spam detected → Polite response sent
- ✅ Message still processed (not blocked)
- ✅ Spam tracker auto-cleans old timestamps
- ✅ System remains stable

**Configuration:**
- `SPAM_THRESHOLD_SECONDS = 2` - Minimum seconds between messages
- `SPAM_MESSAGE_LIMIT = 5` - Max messages in window
- `SPAM_WINDOW_SECONDS = 10` - Time window for detection

---

### 2. **Extremely Long Messages**

**Problem:**
- User sends very long messages (>2000 characters)
- Can cause processing delays
- May indicate copy-paste errors or abuse

**Detection:**
- Validate message length before processing
- Check if message exceeds 2000 characters

**Handling:**
```python
# Location: app/services/edge_case_handler.py::validate_message_length()
# Also: app/services/telegram.py (normalization truncation)
```

**Response:**
```
"Your message is quite long! Could you break it down into smaller questions? 
I'm here to help with specific topics like pricing, features, or getting started. 
What would you like to know?"
```

**System Behavior:**
- ✅ Long message detected → Polite response
- ✅ Message truncated to 2000 chars for processing
- ✅ Original intent still detected (if possible)
- ✅ System remains stable

**Configuration:**
- `MAX_MESSAGE_LENGTH = 2000` - Maximum characters

---

### 3. **Messages with Only Emojis or Symbols**

**Problem:**
- User sends only emojis (😊🎉👍) or symbols (!@#$)
- Intent detection fails (no keywords)
- System can't understand user intent

**Detection:**
- Check if message has any alphanumeric characters
- If no alphanumeric → emoji/symbol only

**Handling:**
```python
# Location: app/services/edge_case_handler.py::is_emoji_or_symbol_only()
```

**Response:**
```
"I see you sent emojis! 😊 While I love emojis, I work best with text. 
Could you tell me in words how I can help you today?"
```

**System Behavior:**
- ✅ Emoji-only detected → Friendly response
- ✅ Intent set to UNKNOWN
- ✅ User guided to use text
- ✅ System remains stable

---

### 4. **Repeated Unknown Intents**

**Problem:**
- User sends multiple messages that don't match any intent
- System keeps responding with generic "unknown" message
- User may get frustrated

**Detection:**
- Track consecutive unknown intents per user
- Count resets on any known intent
- Special response after 3+ consecutive unknowns

**Handling:**
```python
# Location: 
# - app/services/edge_case_handler.py::track_unknown_intent()
# - app/services/ai_brain.py::generate_response_for_intent()
```

**Response (after 3+ unknowns):**
```
"I'm having trouble understanding what you're looking for. 
Could you try rephrasing your question? I can help with: 
pricing information, getting started, features, or connecting you with support. 
What would be most helpful?"
```

**System Behavior:**
- ✅ Unknown intent tracked in memory
- ✅ After 3 consecutive → More helpful response
- ✅ Count resets on any known intent
- ✅ User gets guidance instead of generic response

**Configuration:**
- `UNKNOWN_INTENT_THRESHOLD = 3` - Consecutive unknowns before special response

---

### 5. **Requests for Unsupported Actions**

**Problem:**
- User requests actions system can't perform:
  - File uploads
  - Video calls
  - Payment processing
  - Account creation
  - Admin actions
- System should politely decline and redirect

**Detection:**
- Keyword matching for unsupported action patterns
- Categories: file_upload, video_call, payment, account_creation, admin_action

**Handling:**
```python
# Location: app/services/edge_case_handler.py::is_unsupported_action()
```

**Responses by Action Type:**

**File Upload:**
```
"I can't receive files right now, but I can help answer questions! 
What information are you looking for?"
```

**Video Call:**
```
"I'm a text-based assistant, so I can't do video calls. 
But I'm here to help with any questions you have! What can I assist you with?"
```

**Payment:**
```
"I can provide information about our pricing plans, but I can't process payments. 
For payment questions, please visit our website or contact support. 
Would you like to know more about our pricing?"
```

**Account Creation:**
```
"I can help you get started! For account creation, please visit our website. 
I'm here to answer questions about our service. What would you like to know?"
```

**System Behavior:**
- ✅ Unsupported action detected → Appropriate response
- ✅ User redirected to correct channel
- ✅ Intent still tracked for analytics
- ✅ System remains stable

---

## Implementation Details

### Edge Case Handler Module

**File:** `app/services/edge_case_handler.py`

**Functions:**
- `is_spam(user_id)` - Spam detection
- `validate_message_length(message_text)` - Length validation
- `is_emoji_or_symbol_only(message_text)` - Emoji detection
- `track_unknown_intent(user_id, intent)` - Unknown intent tracking
- `is_unsupported_action(message_text)` - Unsupported action detection

**Storage:**
- In-memory dictionaries (no external services)
- Auto-cleanup of old spam timestamps
- Memory-efficient tracking

---

### Integration Points

**1. Webhook Entry** (`app/routes/telegram.py`)
- No edge case checks here (handled in processing)

**2. Normalization** (`app/services/telegram.py`)
- Message length truncation (if > 2000 chars)

**3. AI Brain Processing** (`app/services/ai_brain.py`)
- Spam check (before processing)
- Length validation (before processing)
- Emoji check (before processing)
- Unsupported action check (before processing)
- Unknown intent tracking (during processing)

**4. Memory** (`app/services/memory.py`)
- Extended to track `unknown_intent_count`

---

## Edge Case Flow

```
User Message
    ↓
1. Spam Check
   → If spam: Return polite spam response ✅
   → If not spam: Continue
    ↓
2. Length Validation
   → If too long: Return polite length response ✅
   → If valid: Continue (truncate if needed)
    ↓
3. Emoji Check
   → If emoji-only: Return friendly emoji response ✅
   → If has text: Continue
    ↓
4. Unsupported Action Check
   → If unsupported: Return appropriate redirect response ✅
   → If supported: Continue
    ↓
5. Normal Processing
   → Knowledge lookup
   → Intent detection
   → Unknown intent tracking
   → Response generation
    ↓
6. Unknown Intent Special Handling
   → If 3+ consecutive unknowns: Return helpful guidance ✅
   → Otherwise: Normal response
```

---

## System Stability Guarantees

### ✅ All Edge Cases Handled

1. **Spam:**
   - ✅ Detected and responded to
   - ✅ System continues operating
   - ✅ No blocking or crashes

2. **Long Messages:**
   - ✅ Detected and truncated
   - ✅ User gets helpful response
   - ✅ System processes safely

3. **Emoji-Only:**
   - ✅ Detected and handled
   - ✅ User guided to use text
   - ✅ System remains stable

4. **Repeated Unknowns:**
   - ✅ Tracked and responded to
   - ✅ User gets helpful guidance
   - ✅ System learns from patterns

5. **Unsupported Actions:**
   - ✅ Detected and redirected
   - ✅ User gets appropriate response
   - ✅ System remains stable

### ✅ Error Handling

- All edge case checks wrapped in try-catch
- Fail-open: If check fails, continue processing
- Errors logged but never crash system
- User always receives a response

### ✅ Performance

- In-memory tracking (fast)
- Minimal overhead (simple checks)
- Auto-cleanup (memory efficient)
- No external API calls

---

## Configuration

### Adjustable Constants

```python
# app/services/edge_case_handler.py

MAX_MESSAGE_LENGTH = 2000  # Characters
SPAM_THRESHOLD_SECONDS = 2  # Min seconds between messages
SPAM_MESSAGE_LIMIT = 5  # Max messages in window
SPAM_WINDOW_SECONDS = 10  # Time window for spam detection
UNKNOWN_INTENT_THRESHOLD = 3  # Consecutive unknowns before special response
```

**To Adjust:**
- Edit constants in `app/services/edge_case_handler.py`
- No code changes needed elsewhere
- Changes take effect on next request

---

## Testing Scenarios

### Test Case 1: Spam Detection
```
Input: 10 messages in 5 seconds
Expected: Spam response after threshold
Result: ✅ Polite spam response sent
```

### Test Case 2: Long Message
```
Input: 3000 character message
Expected: Length response + truncation
Result: ✅ Message truncated, helpful response sent
```

### Test Case 3: Emoji-Only
```
Input: "😊🎉👍"
Expected: Emoji-friendly response
Result: ✅ Friendly response guiding to text
```

### Test Case 4: Repeated Unknowns
```
Input: 4 messages with no matching intents
Expected: Special guidance after 3rd
Result: ✅ Helpful guidance response on 4th message
```

### Test Case 5: Unsupported Action
```
Input: "Can I upload a file?"
Expected: File upload redirect response
Result: ✅ Appropriate redirect response
```

---

## Summary

**✅ All Edge Cases Handled:**
1. Spam → Polite rate-limiting response
2. Long messages → Helpful truncation response
3. Emoji-only → Friendly text guidance
4. Repeated unknowns → Helpful guidance after threshold
5. Unsupported actions → Appropriate redirect responses

**✅ System Stability:**
- All checks fail-open (continue on error)
- No blocking operations
- No external dependencies
- Memory-efficient tracking

**✅ User Experience:**
- All responses are polite and helpful
- Users are guided, not blocked
- System remains responsive
- No crashes or errors exposed

The system is production-ready with comprehensive edge case handling!

