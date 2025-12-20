# 🚀 Quick Deploy Checklist - Curie to Render

## ✅ **STEP 1: Supabase Setup** (Do this first)

- [ ] Created Supabase account at https://supabase.com
- [ ] Created new project named `curie`
- [ ] Saved database password securely
- [ ] Got connection string from: **Settings → Database → Connection string → URI tab**
- [ ] Replaced `[YOUR-PASSWORD]` in connection string with actual password
- [ ] Connection string looks like: `postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres`

**Your Supabase Connection String:**
```
_________________________________________________________
```

---

## ✅ **STEP 2: Render Account Setup**

- [ ] Created Render account at https://render.com
- [ ] Logged into Render dashboard

---

## ✅ **STEP 3: Deploy to Render**

### **3.1: Create Blueprint**

1. [ ] Click **"New +"** → **"Blueprint"**
2. [ ] Connect GitHub account (authorize Render)
3. [ ] Select repository: `kibetwikii9-crypto/curie`
4. [ ] Click **"Apply"** (Render will detect `render.yaml`)

### **3.2: Set Environment Variables**

**Backend Service (`curie-backend`):**

Go to: **Dashboard → curie-backend → Environment tab**

Add these variables:

```
BOT_TOKEN = your_telegram_bot_token_here
DATABASE_URL = postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres
LOG_LEVEL = INFO
OPENAI_API_KEY = (leave empty)
```

**⚠️ Important:**
- Replace `your_telegram_bot_token_here` with your actual Telegram bot token
- Replace the `DATABASE_URL` with your Supabase connection string (from Step 1)

**Frontend Service (`curie-frontend`):**
- [ ] No manual variables needed (auto-configured)

### **3.3: Wait for Deployment**

- [ ] Monitor **"Events"** tab in each service
- [ ] Wait for **"Live"** status (green checkmark)
- [ ] Takes 5-10 minutes for first deployment

### **3.4: Get Your URLs**

After deployment, save these URLs:

**Backend URL:**
```
https://curie-backend-xxxx.onrender.com
```

**Frontend URL:**
```
https://curie-frontend-xxxx.onrender.com
```

---

## ✅ **STEP 4: Verify Deployment**

- [ ] Test backend: Visit `https://curie-backend-xxxx.onrender.com/health`
  - Should return: `{"status":"ok"}`

- [ ] Test frontend: Visit `https://curie-frontend-xxxx.onrender.com`
  - Should show login page

- [ ] Check backend logs for: `✅ Database initialized successfully`

---

## ✅ **STEP 5: Create Admin User**

1. [ ] Go to backend service → **"Shell"** tab
2. [ ] Run: `python create_admin_auto.py`
3. [ ] Verify admin user created

**Login Credentials:**
- Email: `admin@curie.com`
- Password: `admin123`

---

## ✅ **STEP 6: Update Telegram Webhook**

1. [ ] Get your backend URL: `https://curie-backend-xxxx.onrender.com`
2. [ ] Update webhook using this URL (replace YOUR_BOT_TOKEN):

```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://curie-backend-xxxx.onrender.com/telegram/webhook
```

Or use PowerShell:
```powershell
$botToken = "your_bot_token_here"
$webhookUrl = "https://curie-backend-xxxx.onrender.com/telegram/webhook"
Invoke-WebRequest -Uri "https://api.telegram.org/bot$botToken/setWebhook?url=$webhookUrl"
```

---

## ✅ **STEP 7: Final Testing**

- [ ] Login to dashboard: `admin@curie.com` / `admin123`
- [ ] Send message to Telegram bot
- [ ] Verify bot responds
- [ ] Check Supabase dashboard → Table Editor → See tables created

---

## 🎉 **YOU'RE LIVE!**

Your Curie platform is now deployed and running!

---

## ❓ **NEED HELP?**

If you get stuck at any step, let me know which step and I'll help!

