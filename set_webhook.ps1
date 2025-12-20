# Telegram Webhook Setup Script
# This script helps you set your Telegram webhook URL

Write-Host "=== Telegram Webhook Setup ===" -ForegroundColor Green
Write-Host ""

# Get bot token from .env file
$envPath = ".env"
if (Test-Path $envPath) {
    $envContent = Get-Content $envPath
    $botTokenLine = $envContent | Where-Object { $_ -match "^BOT_TOKEN=" }
    if ($botTokenLine) {
        $botToken = $botTokenLine -replace "BOT_TOKEN=", "" -replace '"', ""
        Write-Host "✅ Found bot token in .env" -ForegroundColor Green
    } else {
        Write-Host "❌ BOT_TOKEN not found in .env" -ForegroundColor Red
        $botToken = Read-Host "Enter your bot token manually"
    }
} else {
    Write-Host "⚠️  .env file not found" -ForegroundColor Yellow
    $botToken = Read-Host "Enter your bot token"
}

Write-Host ""
Write-Host "Enter your webhook URL (must be HTTPS):" -ForegroundColor Cyan
Write-Host "  Example: https://abc123.ngrok.io/telegram/webhook" -ForegroundColor Gray
Write-Host "  Or: https://your-domain.com/telegram/webhook" -ForegroundColor Gray
Write-Host ""
$webhookUrl = Read-Host "Webhook URL"

if (-not $webhookUrl) {
    Write-Host "❌ Webhook URL is required" -ForegroundColor Red
    exit 1
}

# Ensure URL ends with /telegram/webhook
if (-not $webhookUrl.EndsWith("/telegram/webhook")) {
    if ($webhookUrl.EndsWith("/")) {
        $webhookUrl = $webhookUrl + "telegram/webhook"
    } else {
        $webhookUrl = $webhookUrl + "/telegram/webhook"
    }
}

Write-Host ""
Write-Host "Setting webhook to: $webhookUrl" -ForegroundColor Yellow

try {
    $setUrl = "https://api.telegram.org/bot$botToken/setWebhook?url=$webhookUrl"
    $response = Invoke-RestMethod -Uri $setUrl -Method Get
    
    if ($response.ok) {
        Write-Host "✅ Webhook set successfully!" -ForegroundColor Green
        Write-Host ($response | ConvertTo-Json -Depth 3)
    } else {
        Write-Host "❌ Failed to set webhook" -ForegroundColor Red
        Write-Host ($response | ConvertTo-Json)
    }
    
    Write-Host ""
    Write-Host "Verifying webhook..." -ForegroundColor Cyan
    $infoUrl = "https://api.telegram.org/bot$botToken/getWebhookInfo"
    $info = Invoke-RestMethod -Uri $infoUrl -Method Get
    
    Write-Host ""
    Write-Host "Current webhook info:" -ForegroundColor Green
    Write-Host ($info.result | ConvertTo-Json -Depth 3)
    
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
    Write-Host "Make sure:" -ForegroundColor Yellow
    Write-Host "  1. Bot token is correct" -ForegroundColor White
    Write-Host "  2. Webhook URL is accessible (use ngrok for local dev)" -ForegroundColor White
    Write-Host "  3. Webhook URL uses HTTPS" -ForegroundColor White
}



