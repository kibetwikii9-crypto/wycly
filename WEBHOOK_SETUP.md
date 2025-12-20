# Telegram Webhook Setup Guide

## Problem: No Logs Appearing

If you're not seeing any logs when messaging your bot, **Telegram is not calling your webhook**. This is because:
- Your server is running on `localhost:8000` (only accessible on your computer)
- Telegram needs a **public HTTPS URL** to send webhooks to

## Solution: Use ngrok (for local development)

### Step 1: Install ngrok

Download from: https://ngrok.com/download
Or install via package manager:
```powershell
# Using Chocolatey
choco install ngrok

# Or download from https://ngrok.com/download
```

### Step 2: Start ngrok tunnel

In a **new terminal window**, run:
```powershell
ngrok http 8000
```

You'll see output like:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8000
```

**Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)

### Step 3: Set Telegram Webhook

Replace `YOUR_BOT_TOKEN` and `YOUR_NGROK_URL` with your actual values:

```powershell
# Get your bot token from .env file or Telegram BotFather
$BOT_TOKEN = "YOUR_BOT_TOKEN"
$WEBHOOK_URL = "YOUR_NGROK_URL/telegram/webhook"

# Set the webhook
Invoke-RestMethod -Uri "https://api.telegram.org/bot$BOT_TOKEN/setWebhook?url=$WEBHOOK_URL"
```

**Example:**
```powershell
Invoke-RestMethod -Uri "https://api.telegram.org/bot123456:ABC-DEF/setWebhook?url=https://abc123.ngrok.io/telegram/webhook"
```

### Step 4: Verify Webhook is Set

Check webhook status:
```powershell
$BOT_TOKEN = "YOUR_BOT_TOKEN"
Invoke-RestMethod -Uri "https://api.telegram.org/bot$BOT_TOKEN/getWebhookInfo"
```

You should see:
```json
{
  "ok": true,
  "result": {
    "url": "https://abc123.ngrok.io/telegram/webhook",
    "has_custom_certificate": false,
    "pending_update_count": 0
  }
}
```

### Step 5: Test Your Bot

1. Keep your FastAPI server running (`python -m uvicorn app.main:app --reload`)
2. Keep ngrok running (in separate terminal)
3. Send a message to your Telegram bot
4. **Watch your server logs** - you should now see:
   ```
   INFO: Received Telegram update: update_id=...
   ```

## Alternative: Production Deployment

For production, deploy your server to:
- Heroku
- Railway
- DigitalOcean
- AWS/GCP/Azure
- Any cloud provider with HTTPS

Then set webhook to: `https://your-domain.com/telegram/webhook`

## Quick Test Script

Save this as `set_webhook.ps1`:

```powershell
# Get bot token from .env
$env:Path += ";$PWD"
$envFile = Get-Content .env
$botToken = ($envFile | Where-Object { $_ -match "BOT_TOKEN=" }) -replace "BOT_TOKEN=", ""

# Get ngrok URL (you need to set this manually)
$ngrokUrl = Read-Host "Enter your ngrok HTTPS URL (e.g., https://abc123.ngrok.io)"

# Set webhook
$webhookUrl = "$ngrokUrl/telegram/webhook"
Write-Host "Setting webhook to: $webhookUrl" -ForegroundColor Yellow

$response = Invoke-RestMethod -Uri "https://api.telegram.org/bot$botToken/setWebhook?url=$webhookUrl"
Write-Host ($response | ConvertTo-Json) -ForegroundColor Green

# Verify
Write-Host "`nVerifying webhook..." -ForegroundColor Yellow
$info = Invoke-RestMethod -Uri "https://api.telegram.org/bot$botToken/getWebhookInfo"
Write-Host ($info | ConvertTo-Json) -ForegroundColor Cyan
```



