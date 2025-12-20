# Diagnostic Checklist - Why No Telegram Replies?

## Step 1: Verify Webhook is Being Called

**Check server logs for:**
```
INFO: Received Telegram update: update_id=...
```

**If you DON'T see this:**
- Telegram webhook URL might not be configured correctly
- Webhook URL should be: `https://your-domain.com/telegram/webhook`
- Check Telegram Bot API: `https://api.telegram.org/bot<YOUR_TOKEN>/getWebhookInfo`

## Step 2: Check Normalization

**Look for in logs:**
```
WARNING: Received Telegram update that could not be normalized
```

**If you see this, check:**
- Does the message have text? (photos/stickers are skipped)
- Is the update structure correct?
- Check the `extra` fields in the warning log

## Step 3: Check chat_id Extraction

**Look for in logs:**
```
INFO: Extracted reply destination (chat_id=..., chat_id_type=...)
```

**If chat_id is None:**
- Check metadata structure
- Verify `chat.id` exists in Telegram payload

**If chat_id_type is not 'int':**
- The code now converts it automatically
- But check if conversion is working

## Step 4: Check Processor

**Look for in logs:**
```
INFO: Processor generated reply: Hello 👋 Your message was received. [FROM PROCESSOR]
INFO: Reply text from processor: ...
```

**If you see this:** Processor is working ✅

## Step 5: Check Telegram API Call

**Look for in logs:**
```
INFO: Attempting to send reply to chat_id: ...
INFO: Sending Telegram message (chat_id=..., text_length=...)
```

**If you see errors:**
```
ERROR: HTTP error sending message to chat_id ...
```

**Common errors:**
- `401 Unauthorized` → Bot token is invalid
- `400 Bad Request` → chat_id format issue
- `403 Forbidden` → Bot blocked by user
- `429 Too Many Requests` → Rate limit

## Step 6: Verify Bot Token

**Check your `.env` file:**
```
BOT_TOKEN=your_actual_token_here
```

**Test token validity:**
```bash
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

## Quick Test

Send a message to your bot and check logs in this order:

1. ✅ "Received Telegram update" → Webhook is working
2. ✅ "Processing normalized message" → Normalization worked
3. ✅ "Reply text from processor" → Processor generated reply
4. ✅ "Extracted reply destination" → chat_id found
5. ✅ "Sending Telegram message" → Attempting to send
6. ✅ "Message sent successfully" → SUCCESS!

**If any step fails, that's where the issue is.**



