# 🔧 Telegram Bot Not Replying - Troubleshooting Guide

## 🔍 **Quick Diagnosis Steps**

### **Step 1: Verify Bot is Connected**

1. Go to your dashboard: **Integrations → Telegram**
2. Check if your bot is listed and shows as "Connected"
3. If not connected, click **"Connect Bot"** and enter your bot token

---

### **Step 2: Check Webhook Status**

You can check webhook status via the Integrations page in the dashboard, or manually:

```powershell
# Replace YOUR_BOT_TOKEN with your actual token (from @BotFather)
$botToken = "YOUR_BOT_TOKEN"
Invoke-RestMethod -Uri "https://api.telegram.org/bot$botToken/getWebhookInfo"
```

**Expected Output:**
```json
{
  "ok": true,
  "result": {
    "url": "https://wycly-backend-xxxx.onrender.com/telegram/webhook",
    "has_custom_certificate": false,
    "pending_update_count": 0
  }
}
```

**If webhook is NOT set:**
- Reconnect your bot via the dashboard (Integrations → Telegram)
- The webhook will be automatically configured

---

### **Step 3: Check Backend Logs**

In Render dashboard → Backend service → Logs tab:

**Look for:**
1. ✅ `webhook_received update_id=...` - Webhook is being received
2. ✅ `message_normalized user_id=...` - Message was processed
3. ✅ `reply_sent chat_id=...` - Reply was sent successfully

**If you see errors:**
- `reply_send_failed` → Check bot token in database (reconnect via dashboard)
- `no_chat_id` → Webhook payload issue (check logs for details)
- `HTTP error 401` → Bot token is invalid (get new token from @BotFather)
- `HTTP error 403` → Bot is blocked by user

---

### **Step 4: Test the Webhook Endpoint**

Test if the webhook endpoint is accessible:

**In Browser:**
```
https://wycly-backend-xxxx.onrender.com/health
```
Should return: `{"status":"ok"}`

**Test webhook endpoint (should return 422 - that's OK, it means endpoint exists):**
```
https://wycly-backend-xxxx.onrender.com/telegram/webhook
```
Should return: `{"detail": [...]}` (422 error is expected without a payload)

---

## 🚨 **Common Issues & Solutions**

### **Issue 1: Bot Not Connected**

**Symptoms:**
- Bot doesn't reply at all
- No bot listed in Integrations page

**Solution:**
1. Go to dashboard → **Integrations → Telegram**
2. Click **"Connect Bot"**
3. Enter your bot token (from @BotFather)
4. Click **"Connect"**
5. Webhook will be automatically configured

---

### **Issue 2: Wrong Webhook URL**

**Symptoms:**
- Webhook is set but bot doesn't reply
- Backend logs show no webhook received

**Solution:**
1. Disconnect and reconnect your bot via the dashboard
2. The webhook will be automatically set to the correct URL
3. Verify webhook URL format: `https://your-backend-url.onrender.com/telegram/webhook`
4. Must be HTTPS (not HTTP)

---

### **Issue 3: Bot Token Invalid**

**Symptoms:**
- Backend logs show: `HTTP error sending message`
- Webhook received but no reply sent
- Error 401 in logs

**Solution:**
1. Get a new bot token from @BotFather on Telegram
2. Go to dashboard → **Integrations → Telegram**
3. Disconnect old bot and connect with new token
4. Test again

---

### **Issue 4: Backend Not Running**

**Symptoms:**
- Webhook set but returns 502/503 errors
- `getWebhookInfo` shows webhook URL but `pending_update_count` > 0

**Solution:**
1. Check Render dashboard → Backend service status
2. Should be "Live" (green)
3. If not, check logs for startup errors
4. Verify DATABASE_URL is set correctly

---

### **Issue 5: Database Connection Failed**

**Symptoms:**
- Backend starts but crashes on webhook
- Logs show: `Database initialization error`

**Solution:**
1. Verify `DATABASE_URL` in Render environment variables
2. Check Supabase connection string format
3. Ensure Supabase database is accessible

---

## ✅ **Complete Setup Checklist**

- [ ] Backend service is "Live" on Render
- [ ] Bot is connected via dashboard (Integrations → Telegram)
- [ ] `DATABASE_URL` is set (Supabase connection string)
- [ ] Webhook is set (automatic when connecting bot)
- [ ] Webhook URL is HTTPS (not HTTP)
- [ ] Backend logs show "✅ Database initialized successfully"
- [ ] Test message sent to bot
- [ ] Backend logs show "webhook_received"
- [ ] Backend logs show "reply_sent"

---

## 🧪 **Quick Test**

1. **Send a message to your bot** on Telegram
2. **Check Render logs** for:
   - `webhook_received` - Webhook working
   - `reply_sent` - Bot replied successfully
3. **If no reply**, check:
   - Bot is connected via dashboard
   - Bot token is valid (test with @BotFather)
   - Backend is running and healthy

---

## 📝 **Important Notes**

- **Bot tokens are stored in the database** (per business), not in environment variables
- **Each business connects their own bot** through the dashboard
- **Webhook is automatically configured** when you connect a bot
- **No BOT_TOKEN environment variable needed**

---

**If bot still doesn't reply after checking all items, share the backend logs and I'll help debug further!**
