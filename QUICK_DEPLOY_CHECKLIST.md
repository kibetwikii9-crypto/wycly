# 🚀 Quick Deploy Checklist - Wycly to Render

## ✅ **STEP 1: Supabase Setup** (Do this first)

- [ ] Created Supabase account at https://supabase.com
- [ ] Created new project named `wycly`
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
3. [ ] Select repository: `kibetwikii9-crypto/wycly`
4. [ ] Click **"Apply"** (Render will detect `render.yaml`)

### **3.2: Set Environment Variables**

**Backend Service (`wycly-backend`):**

Go to: **Dashboard → wycly-backend → Environment tab**

Add these variables:

```
DATABASE_URL = postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres
SECRET_KEY = your_strong_secret_key_here
LOG_LEVEL = INFO
OPENAI_API_KEY = (leave empty)
```

**⚠️ Important:**
- Replace the `DATABASE_URL` with your Supabase connection string (from Step 1)
- Generate a strong `SECRET_KEY` (use: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)

**Note:** BOT_TOKEN and ADMIN credentials are NOT needed. Users connect their own Telegram bots through the dashboard and create accounts through registration.

**Frontend Service (`wycly-frontend`):**
- [ ] No manual variables needed (auto-configured)

### **3.3: Wait for Deployment**

- [ ] Monitor **"Events"** tab in each service
- [ ] Wait for **"Live"** status (green checkmark)
- [ ] Takes 5-10 minutes for first deployment

### **3.4: Get Your URLs**

After deployment, save these URLs:

**Backend URL:**
```
https://wycly-backend-xxxx.onrender.com
```

**Frontend URL:**
```
https://wycly-frontend-xxxx.onrender.com
```

---

## ✅ **STEP 4: Verify Deployment**

- [ ] Test backend: Visit `https://wycly-backend-xxxx.onrender.com/health`
  - Should return: `{"status":"ok"}`

- [ ] Test frontend: Visit `https://wycly-frontend-xxxx.onrender.com`
  - Should show login page

- [ ] Check backend logs for: `✅ Database initialized successfully`

---

## ✅ **STEP 5: Create Account**

1. [ ] Go to your frontend URL: `https://wycly-frontend-xxxx.onrender.com`
2. [ ] Click **"Sign Up"** to create your account
3. [ ] Fill in your details (email, password, name)
4. [ ] Click **"Sign Up"**
5. [ ] You'll be automatically logged in

---

## ✅ **STEP 6: Connect Telegram Bot**

1. [ ] Login to your dashboard
2. [ ] Go to **Integrations → Telegram**
3. [ ] Click **"Connect Bot"**
4. [ ] Enter your Telegram bot token (from @BotFather)
5. [ ] Click **"Connect"**
6. [ ] Webhook will be automatically configured

---

## ✅ **STEP 7: Final Testing**

- [ ] Login to dashboard with your account
- [ ] Verify Telegram bot is connected (Integrations page)
- [ ] Send message to Telegram bot
- [ ] Verify bot responds
- [ ] Check Supabase dashboard → Table Editor → See tables created

---

## 🎉 **YOU'RE LIVE!**

Your Wycly platform is now deployed and running!

---

## ❓ **NEED HELP?**

If you get stuck at any step, let me know which step and I'll help!

