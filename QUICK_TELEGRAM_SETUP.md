# Quick Telegram Setup Guide

## Step 1: Connect Your Telegram Bot

1. **Create a Telegram Bot** (if you haven't already):
   - Open Telegram and search for **@BotFather**
   - Send `/newbot` command
   - Follow the instructions to create your bot
   - Copy the bot token you receive

2. **Connect Bot in Dashboard**:
   - Go to your dashboard: **Integrations → Telegram**
   - Click **"Connect Bot"** button
   - Enter your Telegram bot token (from @BotFather)
   - Click **"Connect"**
   - The webhook will be automatically configured

---

## Step 2: Test the Bot

1. **Send a message to your bot** on Telegram
2. **Check Render logs:**
   - Go to: https://dashboard.render.com → `wycly-backend` → **Logs** tab
   - Look for these log messages:
     - ✅ `webhook_received update_id=...` - Webhook is working
     - ✅ `message_normalized user_id=...` - Message was processed
     - ✅ `attempting_reply chat_id=...` - Bot is trying to reply
     - ✅ `reply_sent chat_id=...` - Reply was sent successfully

**If you see errors:**
- `reply_send_failed` → Check bot token in database (reconnect via dashboard)
- `no_chat_id` → Webhook payload issue (check logs for details)
- `HTTP error 401` → Bot token is invalid (get new token from @BotFather)
- `HTTP error 403` → Bot is blocked by user

---

## Step 3: Test Endpoint (Optional)

You can test if the bot can send messages using the test endpoint:

```powershell
# Replace YOUR_CHAT_ID with your actual Telegram chat ID
# (You'll see it in the logs when you send a message)
$chatId = YOUR_CHAT_ID
$backendUrl = "https://wycly-backend.onrender.com"
Invoke-RestMethod -Uri "$backendUrl/telegram/test-send?chat_id=$chatId&message=Test from Automify"
```

**To find your chat ID:**
1. Send a message to your bot
2. Check Render logs
3. Look for `webhook_received` or `chat_id=` in the logs
4. The number after `chat_id=` is your chat ID

---

## Troubleshooting

### Bot not replying?
1. Check Render logs for errors
2. Verify bot is connected via dashboard (Integrations → Telegram)
3. Make sure webhook is set correctly (should be automatic when connecting)
4. Check if bot is blocked by user (unblock if needed)
5. Verify bot token is valid (test with @BotFather)

### Webhook not working?
- Make sure your backend is deployed and "Live" on Render
- Check that the URL is accessible: https://wycly-backend.onrender.com/health
- Verify bot is connected through the dashboard (Integrations page)

### Still not working?
1. Disconnect and reconnect your bot via the dashboard
2. Check Render logs for detailed error messages
3. Verify your bot token is correct (get new one from @BotFather if needed)

---

## Important Notes

- **Bot tokens are stored in the database** (per business), not in environment variables
- **Each business can connect their own bot** through the dashboard
- **Webhook is automatically configured** when you connect a bot
- **No environment variables needed** for Telegram integration
