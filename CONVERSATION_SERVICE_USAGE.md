# Conversation Service Usage

## ✅ Created `conversation_service.py`

### File: `app/services/conversation_service.py`

This module provides a simple service to save conversations to the database.
It handles errors gracefully and never crashes the application.

---

## 🔧 Functions

### 1. **`save_conversation()`**

```python
async def save_conversation(
    user_message: str,
    bot_reply: str,
    channel: str,
    user_id: str,
    intent: str = None,
) -> bool:
```

**What it does:**
- Saves conversation to database
- Detects intent if not provided
- Handles all errors gracefully
- Returns True on success, False on failure

**Parameters:**
- `user_message`: Original message from user
- `bot_reply`: Response from AI brain
- `channel`: Platform (telegram, whatsapp, instagram)
- `user_id`: Platform-specific user ID
- `intent`: Optional detected intent (auto-detected if not provided)

**Returns:**
- `True` if saved successfully
- `False` if error occurred (logged, not raised)

---

### 2. **`save_conversation_from_normalized()`**

```python
async def save_conversation_from_normalized(
    normalized_message: NormalizedMessage,
    bot_reply: str,
    intent: str = None,
) -> bool:
```

**What it does:**
- Convenience function that extracts data from NormalizedMessage
- Calls `save_conversation()` internally
- Easier to use in routes that already have NormalizedMessage

**Parameters:**
- `normalized_message`: Normalized message object
- `bot_reply`: Response from AI brain
- `intent`: Optional detected intent

**Returns:**
- `True` if saved successfully
- `False` if error occurred (logged, not raised)

---

## 🛡️ Error Handling

### Safe Error Handling Strategy:

1. **All errors are caught:**
   ```python
   try:
       # Save conversation
   except Exception as e:
       log.error(f"Failed to save conversation: {e}", exc_info=True)
       return False
   ```

2. **Never raises exceptions:**
   - All errors are logged
   - Function returns False on error
   - Application continues normally

3. **Validation:**
   - Checks for required fields
   - Handles missing data gracefully
   - Falls back to "unknown" intent if detection fails

4. **Database errors:**
   - Connection errors logged
   - Transaction errors logged
   - Never crashes the application

---

## 📝 How to Use

### Example 1: In Telegram Webhook (After Reply Sent)

```python
from app.services.conversation_service import save_conversation_from_normalized

@router.post("/webhook")
async def telegram_webhook(update: TelegramUpdate):
    # Normalize message
    normalized_message = normalize_telegram_message(update)
    if not normalized_message:
        return {"ok": True}

    # Process message and get reply
    reply_text = await process_message(normalized_message)

    # Send reply
    chat_id = normalized_message.metadata.get("chat_id")
    if chat_id:
        await telegram_service.send_message(int(chat_id), reply_text)

    # Save conversation AFTER reply is sent (non-blocking, error-safe)
    await save_conversation_from_normalized(
        normalized_message=normalized_message,
        bot_reply=reply_text,
    )

    return {"ok": True}
```

**Key Points:**
- ✅ Called AFTER reply is sent
- ✅ Does NOT block message sending
- ✅ Errors are logged but don't crash
- ✅ Non-blocking (async)

---

### Example 2: With Explicit Intent

```python
from app.services.conversation_service import save_conversation
from app.services.ai_brain import detect_intent, Intent

# Detect intent first
intent = detect_intent(normalized_message)
intent_value = intent.value

# Save with explicit intent
await save_conversation(
    user_message=normalized_message.message_text,
    bot_reply=reply_text,
    channel=normalized_message.channel.value,
    user_id=normalized_message.user_id,
    intent=intent_value,
)
```

**When to use:**
- When you already have the intent
- When you want to avoid re-detecting intent
- For better performance

---

### Example 3: Manual Save (Outside Routes)

```python
from app.services.conversation_service import save_conversation

# Save conversation manually
success = await save_conversation(
    user_message="What's the price?",
    bot_reply="We offer flexible pricing plans...",
    channel="telegram",
    user_id="123456789",
    intent="pricing",
)

if success:
    print("Conversation saved!")
else:
    print("Failed to save (check logs)")
```

---

## 🔄 Integration Flow

### Current Flow (Without Saving):

```
1. Receive webhook
2. Normalize message
3. Process message → Get reply
4. Send reply
5. Return {"ok": True}
```

### Updated Flow (With Saving):

```
1. Receive webhook
2. Normalize message
3. Process message → Get reply
4. Send reply
5. Save conversation (non-blocking, error-safe)
6. Return {"ok": True}
```

**Key Points:**
- ✅ Saving happens AFTER reply is sent
- ✅ Does NOT affect message sending
- ✅ Errors don't crash the application
- ✅ Non-blocking operation

---

## 🎯 Best Practices

### 1. **Call After Reply is Sent**

```python
# ✅ GOOD: Save after reply is sent
await telegram_service.send_message(chat_id, reply_text)
await save_conversation_from_normalized(normalized_message, reply_text)

# ❌ BAD: Save before reply is sent (could delay response)
await save_conversation_from_normalized(normalized_message, reply_text)
await telegram_service.send_message(chat_id, reply_text)
```

### 2. **Don't Wait for Result**

```python
# ✅ GOOD: Fire and forget (non-blocking)
await save_conversation_from_normalized(normalized_message, reply_text)
return {"ok": True}

# ❌ BAD: Waiting for result (blocks response)
success = await save_conversation_from_normalized(normalized_message, reply_text)
if not success:
    # Don't handle errors - they're already logged
    pass
return {"ok": True}
```

### 3. **Trust Error Handling**

```python
# ✅ GOOD: Service handles errors internally
await save_conversation_from_normalized(normalized_message, reply_text)

# ❌ BAD: Trying to handle errors (service already does this)
try:
    await save_conversation_from_normalized(normalized_message, reply_text)
except Exception:
    # Don't do this - service already handles errors
    pass
```

---

## 📊 What Gets Saved

### Database Record:

```python
Conversation(
    user_id="123456789",              # From normalized_message.user_id
    channel="telegram",                # From normalized_message.channel.value
    user_message="What's the price?",  # From normalized_message.message_text
    bot_reply="We offer flexible...",   # From process_message() response
    intent="pricing",                  # Detected or provided
    created_at=datetime.utcnow()        # Auto-set by database
)
```

---

## ✅ Benefits

1. **Non-Blocking:**
   - ✅ Does NOT affect message sending
   - ✅ Async operation
   - ✅ Fast execution

2. **Error-Safe:**
   - ✅ All errors caught and logged
   - ✅ Never crashes application
   - ✅ Graceful degradation

3. **Simple:**
   - ✅ Just save data, no business logic
   - ✅ Easy to use
   - ✅ Clear interface

4. **Flexible:**
   - ✅ Can provide intent or auto-detect
   - ✅ Works with NormalizedMessage or raw data
   - ✅ Platform-agnostic

---

## 🚀 Next Steps

1. **Integrate in Telegram Route:**
   - Add call after reply is sent
   - Test that errors don't affect sending

2. **Monitor Logs:**
   - Check for any save errors
   - Verify conversations are being saved

3. **Add Analytics (Future):**
   - Query saved conversations
   - Generate reports
   - Track user interactions

---

## 🎯 Summary

**Conversation Service:**
- ✅ Saves user_message + bot_reply
- ✅ Stores channel, user_id, intent
- ✅ Called AFTER bot reply is generated
- ✅ Does NOT affect message sending
- ✅ Handles errors safely (log, don't crash)
- ✅ No business logic (just save data)

**Usage:**
```python
# After reply is sent
await save_conversation_from_normalized(
    normalized_message=normalized_message,
    bot_reply=reply_text,
)
```

The service is ready to use and will safely save all conversations without affecting message delivery!



