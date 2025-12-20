# Quick ngrok Setup

## Option 1: Download and Run (Easiest)

1. **Download ngrok:**
   - Go to: https://ngrok.com/download
   - Download the Windows version (ZIP file)

2. **Extract and run:**
   - Extract the ZIP file
   - Copy `ngrok.exe` to your project folder: `C:\Users\Kibee\Desktop\projects\Curie\`
   - Or run it from wherever you extracted it

3. **Run ngrok:**
   ```powershell
   # If you put it in the project folder:
   .\ngrok.exe http 8000
   
   # Or use full path:
   C:\path\to\ngrok.exe http 8000
   ```

## Option 2: Install via Chocolatey (If you have it)

```powershell
choco install ngrok
```

Then run:
```powershell
ngrok http 8000
```

## Option 3: Use ngrok Cloud (No Installation)

If you have an ngrok account:
1. Sign up at: https://dashboard.ngrok.com/signup
2. Get your authtoken
3. Run: `ngrok config add-authtoken YOUR_TOKEN`
4. Then: `ngrok http 8000`

## What to Do After Starting ngrok

Once ngrok starts, you'll see:
```
Forwarding  https://xxxxx.ngrok-free.dev -> http://localhost:8000
```

**Important:** Make sure the URL matches your webhook:
- Your webhook: `https://sixta-unenriching-angelica.ngrok-free.dev`
- If ngrok gives you a DIFFERENT URL, you need to update the webhook:
  ```powershell
  .\set_webhook.ps1
  ```

## Quick Test

After starting ngrok:
1. Keep your FastAPI server running
2. Keep ngrok running
3. Send a message to your bot
4. Watch your server logs - you should see all the pending updates!



