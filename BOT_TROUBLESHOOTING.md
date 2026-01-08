# 🔧 Telegram Bot Not Replying - Troubleshooting Guide

## 🔍 **Quick Diagnosis Steps**

### **Step 1: Check if Webhook is Set**

Run this in PowerShell (replace `YOUR_BOT_TOKEN` with your actual token):

```powershell
$botToken = "YOUR_BOT_TOKEN"
Invoke-RestMethod -Uri "https://api.telegram.org/bot$botToken/getWebhookInfo"
```

**Expected Output:**
```json
{
  "ok": true,
  "result": {
    "url": "https://automify-ai-backend-xxxx.onrender.com/telegram/webhook",
    "has_custom_certificate": false,
    "pending_update_count": 0
  }
}
```

**If webhook is NOT set:**
- The `url` field will be empty
- You need to set the webhook (see Step 2)

---

### **Step 2: Set the Webhook**

**Get your backend URL from Render:**
- Go to Render dashboard → Backend service (`automify-ai-backend`)
- Copy the service URL (e.g., `https://automify-ai-backend-xxxx.onrender.com`)

**Set the webhook:**

```powershell
$botToken = "YOUR_BOT_TOKEN"
$backendUrl = "https://automify-ai-backend-xxxx.onrender.com"  # Replace with your actual backend URL
$webhookUrl = "$backendUrl/telegram/webhook"

Invoke-RestMethod -Uri "https://api.telegram.org/bot$botToken/setWebhook?url=$webhookUrl"
```

**Expected Response:**
```json
{
  "ok": true,
  "result": true,
  "description": "Webhook was set"
}
```

---

### **Step 3: Verify Backend Environment Variables**

In Render dashboard → Backend service → Environment tab, verify:

- ✅ **BOT_TOKEN** is set (your Telegram bot token)
- ✅ **DATABASE_URL** is set (your Supabase connection string)
- ✅ **PUBLIC_URL** is set (your backend URL)

**If BOT_TOKEN is missing or wrong:**
- The bot won't be able to send replies
- Check Render logs for authentication errors

---

### **Step 4: Check Backend Logs**

In Render dashboard → Backend service → Logs tab:

**Look for:**
1. ✅ `webhook_received update_id=...` - Webhook is being received
2. ✅ `message_normalized user_id=...` - Message was processed
3. ✅ `reply_sent chat_id=...` - Reply was sent successfully

**If you see errors:**
- `ModuleNotFoundError` - Missing dependencies
- `Database connection failed` - DATABASE_URL issue
- `HTTP error sending message` - BOT_TOKEN issue

---

### **Step 5: Test the Webhook Endpoint**

Test if the webhook endpoint is accessible:

**In Browser:**
```
https://automify-ai-backend-xxxx.onrender.com/health
```
Should return: `{"status":"ok"}`

**Test webhook endpoint (should return 422 - that's OK, it means endpoint exists):**
```
https://automify-ai-backend-xxxx.onrender.com/telegram/webhook
```
Should return: `{"detail": [...]}` (422 error is expected without a payload)

---

## 🚨 **Common Issues & Solutions**

### **Issue 1: Webhook Not Set**

**Symptoms:**
- Bot doesn't reply at all
- No logs in backend
- `getWebhookInfo` shows empty URL

**Solution:**
```powershell
$botToken = "YOUR_BOT_TOKEN"
$backendUrl = "https://automify-ai-backend-xxxx.onrender.com"
Invoke-RestMethod -Uri "https://api.telegram.org/bot$botToken/setWebhook?url=$backendUrl/telegram/webhook"
```

---

### **Issue 2: Wrong Webhook URL**

**Symptoms:**
- Webhook is set but bot doesn't reply
- Backend logs show no webhook received

**Solution:**
1. Verify webhook URL format: `https://your-backend-url.onrender.com/telegram/webhook`
2. Must be HTTPS (not HTTP)
3. Must end with `/telegram/webhook`
4. Re-set the webhook with correct URL

---

### **Issue 3: BOT_TOKEN Not Set or Wrong**

**Symptoms:**
- Backend logs show: `HTTP error sending message`
- Webhook received but no reply sent

**Solution:**
1. Go to Render → Backend service → Environment
2. Verify `BOT_TOKEN` is set correctly
3. Get token from Telegram BotFather if needed
4. Restart backend service after updating

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
- [ ] `BOT_TOKEN` is set in Render environment variables
- [ ] `DATABASE_URL` is set (Supabase connection string)
- [ ] Webhook is set to: `https://your-backend-url.onrender.com/telegram/webhook`
- [ ] Webhook URL is HTTPS (not HTTP)
- [ ] Backend logs show "✅ Database initialized successfully"
- [ ] Test message sent to bot
- [ ] Backend logs show "webhook_received"
- [ ] Backend logs show "reply_sent"

---

## 🧪 **Quick Test Script**

Save this as `test_bot.ps1`:

```powershell
# Test Telegram Bot Setup
$botToken = "YOUR_BOT_TOKEN"
$backendUrl = "https://automify-ai-backend-xxxx.onrender.com"

Write-Host "=== Testing Telegram Bot Setup ===" -ForegroundColor Green
Write-Host ""

# 1. Check webhook
Write-Host "1. Checking webhook..." -ForegroundColor Yellow
$webhookInfo = Invoke-RestMethod -Uri "https://api.telegram.org/bot$botToken/getWebhookInfo"
Write-Host "   Webhook URL: $($webhookInfo.result.url)" -ForegroundColor Cyan
Write-Host "   Pending updates: $($webhookInfo.result.pending_update_count)" -ForegroundColor Cyan

# 2. Test backend health
Write-Host ""
Write-Host "2. Testing backend health..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$backendUrl/health"
    Write-Host "   ✅ Backend is healthy: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Backend is not responding: $_" -ForegroundColor Red
}

# 3. Test webhook endpoint
Write-Host ""
Write-Host "3. Testing webhook endpoint..." -ForegroundColor Yellow
try {
    $webhookTest = Invoke-WebRequest -Uri "$backendUrl/telegram/webhook" -Method POST -ErrorAction SilentlyContinue
    Write-Host "   ✅ Webhook endpoint exists (status: $($webhookTest.StatusCode))" -ForegroundColor Green
} catch {
    if ($_.Exception.Response.StatusCode -eq 422) {
        Write-Host "   ✅ Webhook endpoint exists (422 is expected without payload)" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Webhook endpoint error: $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== Test Complete ===" -ForegroundColor Green
```

---

## 📝 **Next Steps**

1. **Run the test script** above
2. **Check each item** in the checklist
3. **Review backend logs** for any errors
4. **Send a test message** to your bot
5. **Check logs again** to see if webhook was received

---

**If bot still doesn't reply after checking all items, share the backend logs and I'll help debug further!**

