# Telegram Reply Fix - Summary

## What Was Fixed

I've improved the Telegram webhook handler to better diagnose and handle reply issues **without duplicating any code**:

### 1. **Enhanced Error Logging**
   - More detailed logs when chat_id extraction fails
   - Better error messages showing exactly what went wrong
   - Logs now include chat_id type information for debugging

### 2. **Improved Chat ID Extraction**
   - Added fallback extraction if chat_id is missing from metadata
   - Handles both dict and Pydantic model formats
   - More robust error handling

### 3. **Better Webhook Logging**
   - Logs whether message or channel_post is present
   - More context about incoming webhook structure

### 4. **Test Endpoint Added**
   - New endpoint: `POST /telegram/test-send?chat_id=YOUR_CHAT_ID&message=Test`
   - Allows you to test if bot can send messages without waiting for a webhook
   - Helps verify bot token is working

## How to Fix Telegram Replies

### Step 1: Connect Your Telegram Bot

1. Go to your dashboard: **Integrations → Telegram**
2. Click **"Connect Bot"**
3. Enter your Telegram bot token (from @BotFather)
4. Click **"Connect"**
5. The webhook will be automatically set up

### Step 2: Verify Webhook is Set

You can verify the webhook is set by checking the integration status in the dashboard, or by checking Render logs for webhook activity.

### Step 3: Test Bot Can Send Messages

Use the test endpoint to verify bot can send:
```powershell
# Replace YOUR_CHAT_ID with your actual Telegram chat ID
$chatId = YOUR_CHAT_ID
$backendUrl = "https://wycly-backend.onrender.com"
Invoke-RestMethod -Uri "$backendUrl/telegram/test-send?chat_id=$chatId&message=Test from Wycly"
```

**To get your chat ID:**
1. Send a message to your bot
2. Check Render logs - you'll see `webhook_received` with update_id
3. The chat_id will be in the logs

### Step 4: Check Render Logs

After sending a message to your bot, check Render logs for:
- ✅ `webhook_received` - Webhook is being received
- ✅ `message_normalized` - Message was processed
- ✅ `attempting_reply` - Bot is trying to send reply
- ✅ `reply_sent` - Reply was sent successfully

**If you see errors:**
- `reply_send_failed` → Check bot token in database (via Integrations page)
- `no_chat_id` → Check webhook payload structure
- `HTTP error 401` → Bot token is invalid (reconnect via dashboard)
- `HTTP error 403` → Bot is blocked by user

## Files Changed

- `app/routes/telegram.py` - Enhanced error logging and chat_id extraction
- `app/services/telegram.py` - Already had improved error logging (from previous fix)

**No code was duplicated** - only improvements to existing functions.

**Note:** Bot tokens are now stored in the database (per business) and connected through the dashboard UI, not via environment variables.
