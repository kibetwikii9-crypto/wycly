# Structured Logging Strategy

## Overview

Structured logging with request IDs for observability and debugging. Every request gets a unique ID that is logged throughout the request lifecycle, making it easy to trace a single conversation through the system.

---

## Logging Architecture

### Request ID System

**Implementation:** `app/logging_context.py`
- Uses `contextvars` for async-safe request context
- Each request gets a unique 8-character ID (UUID prefix)
- Request ID is automatically included in all log messages
- No manual passing of request ID needed

**Usage:**
```python
from app.logging_context import set_request_id, get_request_id

# At request entry point
request_id = set_request_id()  # Auto-generates if None

# Anywhere in the request flow
request_id = get_request_id()  # Returns current request ID
```

---

## Log Format

### Structure

```
YYYY-MM-DD HH:MM:SS LEVEL    logger_name        [request_id] - message
```

### Example Logs

```
2024-01-15 10:30:45 INFO     app.routes.telegram [a1b2c3d4] - webhook_received update_id=12345
2024-01-15 10:30:45 INFO     app.routes.telegram [a1b2c3d4] - message_normalized user_id=123 channel=telegram text_length=15
2024-01-15 10:30:45 INFO     app.services.ai_brain [a1b2c3d4] - knowledge_no_match user_id=123
2024-01-15 10:30:45 INFO     app.services.ai_brain [a1b2c3d4] - intent_detected user_id=123 intent=greeting decision_path=rule_based
2024-01-15 10:30:45 INFO     app.services.ai_brain [a1b2c3d4] - ai_processing_complete user_id=123 intent=greeting decision_path=rule_based
2024-01-15 10:30:45 INFO     app.routes.telegram [a1b2c3d4] - reply_sent chat_id=123 user_id=123
2024-01-15 10:30:45 DEBUG    app.routes.telegram [a1b2c3d4] - conversation_saved user_id=123
```

---

## Key-Value Logging Pattern

### Format
```
event_name key1=value1 key2=value2 key3=value3
```

### Benefits
- Easy to parse (grep, awk, log aggregators)
- Readable in local development
- Structured for future log analysis tools
- No JSON overhead (human-readable)

### Examples

**Incoming Message:**
```
webhook_received update_id=12345
message_normalized user_id=123 channel=telegram text_length=15
```

**AI Decision Path:**
```
knowledge_match user_id=123 decision_path=knowledge_base
knowledge_no_match user_id=123
intent_detected user_id=123 intent=greeting decision_path=rule_based
ai_processing_complete user_id=123 intent=greeting decision_path=rule_based
```

**Errors:**
```
normalization_failed error=ValueError message=invalid_format
processing_failed user_id=123 error=TypeError message=invalid_type
```

---

## Logging Points in Request Flow

### 1. Webhook Entry (`app/routes/telegram.py`)

**Logs:**
- `webhook_received update_id=X` - Incoming webhook
- `message_normalized user_id=X channel=Y text_length=Z` - Successful normalization
- `normalization_failed error=X` - Normalization error
- `empty_message user_id=X` - Empty message detected
- `response_generated user_id=X response_length=Y` - AI response ready
- `reply_sent chat_id=X user_id=Y` - Reply sent successfully
- `reply_send_failed chat_id=X user_id=Y` - Reply send failed
- `conversation_saved user_id=X` - Database save successful
- `conversation_save_failed user_id=X` - Database save failed

---

### 2. AI Brain Processing (`app/services/ai_brain.py`)

**Logs:**
- `knowledge_match user_id=X decision_path=knowledge_base` - Knowledge base match found
- `knowledge_no_match user_id=X` - No knowledge match
- `memory_read user_id=X last_intent=Y message_count=Z` - Memory retrieved
- `intent_detected user_id=X intent=Y decision_path=rule_based` - Intent detected
- `response_generated user_id=X intent=Y response_length=Z` - Response generated
- `memory_updated user_id=X intent=Y` - Memory updated
- `ai_processing_complete user_id=X intent=Y decision_path=rule_based` - Processing complete

**Error Logs:**
- `knowledge_lookup_error user_id=X error=Y action=fallback_to_intent`
- `memory_read_failed user_id=X error=Y action=using_defaults`
- `intent_detection_failed user_id=X error=Y action=using_unknown`
- `response_generation_failed user_id=X error=Y action=using_default`
- `ai_processing_error user_id=X error=Y decision_path=fallback`

---

### 3. Knowledge Service (`app/services/knowledge_service.py`)

**Logs:**
- `knowledge_keyword_match keyword=X` - Keyword match found (DEBUG)
- `knowledge_question_match question_length=X` - Question match found (DEBUG)
- `knowledge_reverse_match` - Reverse match found (DEBUG)

**Note:** Knowledge service logs are at DEBUG level since they're called frequently.

---

### 4. Conversation Service (`app/services/conversation_service.py`)

**Logs:**
- `intent_detected_for_save user_id=X intent=Y` - Intent detected for saving (DEBUG)
- `conversation_saved user_id=X channel=Y intent=Z` - Save successful (DEBUG)
- `conversation_save_validation_failed user_id=X reason=missing_fields` - Validation failed
- `conversation_save_error user_id=X channel=Y error=Z` - Save error

---

## Decision Path Tracking

### Decision Path Values

The `decision_path` field tracks how the AI generated the response:

1. **`knowledge_base`** - Answer found in knowledge base (FAQ)
2. **`rule_based`** - Intent-based rule response
3. **`fallback`** - Safe default response (error occurred)

### Example Flow

```
# Knowledge match
knowledge_match user_id=123 decision_path=knowledge_base
ai_processing_complete user_id=123 intent=pricing decision_path=knowledge_base

# No knowledge match, using intent
knowledge_no_match user_id=123
intent_detected user_id=123 intent=greeting decision_path=rule_based
ai_processing_complete user_id=123 intent=greeting decision_path=rule_based

# Error occurred
ai_processing_error user_id=123 error=TypeError decision_path=fallback
```

---

## Log Levels

### INFO
- Request lifecycle events (webhook received, message normalized, reply sent)
- AI decision points (knowledge match, intent detected, processing complete)
- Important state changes

### DEBUG
- Detailed operation info (memory reads, knowledge matches, conversation saves)
- Verbose debugging information
- Not needed for normal operation

### WARNING
- Recoverable errors (normalization failures, empty responses, memory failures)
- Fallback actions taken
- Non-critical issues

### ERROR
- Unexpected exceptions
- System failures
- Critical errors (with stack traces)

---

## Security: No Secrets Logged

### ✅ Safe to Log
- User IDs (platform-specific, not sensitive)
- Channel names (telegram, whatsapp, etc.)
- Intent values (greeting, pricing, etc.)
- Message lengths (not content)
- Request IDs
- Error types and messages

### ❌ Never Logged
- Bot tokens
- API keys
- Passwords
- Full message content (only length)
- Personal information (names, emails, phone numbers)
- Database credentials

### Message Content
- **Only log:** `text_length=X` (length of message)
- **Never log:** Full message text (may contain sensitive data)

---

## Performance Considerations

### Logging Overhead
- **Request ID:** Context variable lookup (negligible)
- **Structured logs:** String formatting (minimal)
- **No external services:** All logging is local (fast)

### Optimization
- DEBUG logs only enabled in development
- INFO logs for production monitoring
- ERROR logs always enabled
- No blocking I/O (stdout only)

---

## Local Development

### Reading Logs

**Filter by request ID:**
```bash
# Follow logs and filter by request ID
tail -f app.log | grep "\[a1b2c3d4\]"
```

**Filter by user:**
```bash
# Find all logs for a user
grep "user_id=123" app.log
```

**Filter by decision path:**
```bash
# Find all knowledge base matches
grep "decision_path=knowledge_base" app.log

# Find all fallbacks
grep "decision_path=fallback" app.log
```

**Trace a conversation:**
```bash
# Get request ID from first log
grep "webhook_received" app.log | tail -1

# Trace entire request
grep "\[a1b2c3d4\]" app.log
```

---

## Log Structure Examples

### Successful Flow

```
2024-01-15 10:30:45 INFO     app.routes.telegram [a1b2c3d4] - webhook_received update_id=12345
2024-01-15 10:30:45 INFO     app.routes.telegram [a1b2c3d4] - message_normalized user_id=123 channel=telegram text_length=15
2024-01-15 10:30:45 DEBUG    app.services.ai_brain [a1b2c3d4] - knowledge_no_match user_id=123
2024-01-15 10:30:45 DEBUG    app.services.ai_brain [a1b2c3d4] - memory_read user_id=123 last_intent=None message_count=0
2024-01-15 10:30:45 INFO     app.services.ai_brain [a1b2c3d4] - intent_detected user_id=123 intent=greeting decision_path=rule_based
2024-01-15 10:30:45 DEBUG    app.services.ai_brain [a1b2c3d4] - response_generated user_id=123 intent=greeting response_length=45
2024-01-15 10:30:45 DEBUG    app.services.ai_brain [a1b2c3d4] - memory_updated user_id=123 intent=greeting
2024-01-15 10:30:45 INFO     app.services.ai_brain [a1b2c3d4] - ai_processing_complete user_id=123 intent=greeting decision_path=rule_based
2024-01-15 10:30:45 INFO     app.routes.telegram [a1b2c3d4] - reply_sent chat_id=123 user_id=123
2024-01-15 10:30:45 DEBUG    app.routes.telegram [a1b2c3d4] - conversation_saved user_id=123
```

### Knowledge Base Match

```
2024-01-15 10:30:45 INFO     app.routes.telegram [a1b2c3d4] - webhook_received update_id=12345
2024-01-15 10:30:45 INFO     app.routes.telegram [a1b2c3d4] - message_normalized user_id=123 channel=telegram text_length=20
2024-01-15 10:30:45 DEBUG    app.services.knowledge_service [a1b2c3d4] - knowledge_keyword_match keyword=pricing
2024-01-15 10:30:45 INFO     app.services.ai_brain [a1b2c3d4] - knowledge_match user_id=123 decision_path=knowledge_base
2024-01-15 10:30:45 INFO     app.routes.telegram [a1b2c3d4] - reply_sent chat_id=123 user_id=123
```

### Error Flow

```
2024-01-15 10:30:45 INFO     app.routes.telegram [a1b2c3d4] - webhook_received update_id=12345
2024-01-15 10:30:45 ERROR    app.routes.telegram [a1b2c3d4] - normalization_failed error=ValueError message=invalid_format
2024-01-15 10:30:45 INFO     app.routes.telegram [a1b2c3d4] - fallback_response_sent chat_id=123
```

---

## Where Logs Are Added

### Request Entry
- ✅ `app/routes/telegram.py` - Webhook handler

### Normalization
- ✅ `app/services/telegram.py` - Message normalization

### Processing
- ✅ `app/services/processor.py` - Message processor
- ✅ `app/services/ai_brain.py` - AI brain (knowledge, memory, intent, response)

### Knowledge
- ✅ `app/services/knowledge_service.py` - Knowledge base lookup

### Memory
- ✅ `app/services/memory.py` - Memory operations (via ai_brain)

### Persistence
- ✅ `app/services/conversation_service.py` - Database save

### Sending
- ✅ `app/services/telegram.py` - Telegram API send

---

## Summary

**✅ Implemented:**
- Request ID system (async-safe contextvars)
- Structured logging format (key-value pairs)
- Decision path tracking (knowledge/rule/fallback)
- Comprehensive error logging with context
- Readable format for local development
- No secrets logged
- Minimal performance overhead

**✅ Guarantees:**
- Every request has a unique ID
- All key decision points are logged
- Errors include context (not just stack traces)
- Logs are human-readable
- Easy to trace conversations end-to-end

The logging system is production-ready and provides full observability without external dependencies.



