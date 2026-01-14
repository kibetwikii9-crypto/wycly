# 🚀 Deploy to Render - New Service Setup Guide

This guide will help you deploy your project to Render as a **NEW service** (not updating existing ones).

---

## 📋 **PREREQUISITES**

Before starting, make sure you have:

1. ✅ **Git Repository** - Your code pushed to GitHub/GitLab/Bitbucket
2. ✅ **Supabase Database** - Your new Supabase connection string ready
3. ✅ **Render Account** - Sign up at https://render.com (free tier available)

---

## 🔧 **STEP 1: Commit Your Changes**

First, commit the cleanup changes we made:

```powershell
# Add all changes
git add .

# Commit with message
git commit -m "Clean up old database references and prepare for new deployment"

# Push to repository
git push origin main
```

**✅ Checkpoint**: Your code is committed and pushed to Git.

---

## 🎯 **STEP 2: Prepare Your Environment Variables**

Before deploying, gather these values:

### **Required:**
1. **DATABASE_URL** - Your Supabase connection string
   ```
   postgresql://postgres.fmgbnxvgticaljxizwat:%23Kibee%402023@aws-1-eu-central-1.pooler.supabase.com:5432/postgres
   ```

2. **SECRET_KEY** - Generate a strong random key:
   ```powershell
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   Copy the output - you'll need it!

3. **ADMIN_PASSWORD** - Password for your admin user
   - This will auto-create admin user on first startup

### **Optional:**
4. **BOT_TOKEN** - If you're using Telegram bot features
5. **OPENAI_API_KEY** - If you want to use OpenAI features

---

## 🚀 **STEP 3: Deploy to Render**

### **3.1 Create New Blueprint**

1. Go to **https://render.com** and log in
2. Click **"New +"** button (top right)
3. Select **"Blueprint"**
4. Connect your Git repository:
   - Click **"Connect account"** (GitHub/GitLab)
   - Authorize Render to access your repositories
   - Select your repository: `wycly` (or your repo name)
   - Click **"Connect"**

### **3.2 Configure Services**

Render will detect `render.yaml` and show you 2 services:
- `automify-ai-backend` (FastAPI backend)
- `automify-ai-frontend` (Next.js frontend)

**⚠️ IMPORTANT**: If you want different service names, update `render.yaml` first!

Click **"Apply"** to create the services.

**⏱️ Wait**: This takes 5-10 minutes for initial build.

---

## ⚙️ **STEP 4: Set Environment Variables**

After services are created, you need to set environment variables:

### **4.1 Backend Service (`automify-ai-backend`)**

1. Go to Render dashboard
2. Click on **`automify-ai-backend`** service
3. Go to **"Environment"** tab
4. Add these variables:

| Variable | Value | Notes |
|----------|-------|-------|
| `DATABASE_URL` | `postgresql://postgres.fmgbnxvgticaljxizwat:%23Kibee%402023@aws-1-eu-central-1.pooler.supabase.com:5432/postgres` | Your Supabase connection string |
| `SECRET_KEY` | `[generated key]` | The key you generated in Step 2 |
| `ADMIN_EMAIL` | `admin@yourdomain.com` | Your admin email (or leave default) |
| `ADMIN_PASSWORD` | `[your password]` | Password for admin user |
| `BOT_TOKEN` | `[optional]` | Only if using Telegram |
| `OPENAI_API_KEY` | `[optional]` | Only if using OpenAI |

**⚠️ CRITICAL**: Make sure `DATABASE_URL` is set correctly!

5. Click **"Save Changes"**
6. Service will automatically restart

### **4.2 Frontend Service (`automify-ai-frontend`)**

The frontend should automatically get `NEXT_PUBLIC_API_URL` from `render.yaml`, but verify:

1. Click on **`automify-ai-frontend`** service
2. Go to **"Environment"** tab
3. Check that `NEXT_PUBLIC_API_URL` is set (should be auto-set)
4. If missing, add it manually:
   ```
   https://automify-ai-backend.onrender.com
   ```
   (Replace with your actual backend URL)

---

## 🗄️ **STEP 5: Initialize Database**

After backend is running, initialize your database:

### **Option A: Automatic (Recommended)**

The backend will automatically create tables on first startup if `ADMIN_PASSWORD` is set.

Check logs:
1. Go to backend service → **"Logs"** tab
2. Look for: `✅ Database initialized successfully`
3. Look for: `✅ Admin user auto-created: [your email]`

### **Option B: Manual Migration**

If automatic doesn't work, run migration script:

1. Go to backend service → **"Shell"** tab
2. Run:
   ```bash
   python create_all_tables_migration.py
   ```

---

## ✅ **STEP 6: Verify Deployment**

### **6.1 Check Backend**

1. Go to backend service → **"Logs"** tab
2. Should see: `Application startup complete`
3. Visit: `https://[your-backend-url].onrender.com/health`
4. Should return: `{"status":"ok"}`

### **6.2 Check Frontend**

1. Go to frontend service → **"Logs"** tab
2. Should see: `Ready on http://localhost:3000`
3. Visit your frontend URL
4. Should see landing page

### **6.3 Test Login**

1. Go to frontend URL
2. Click **"Sign In"**
3. Use your admin credentials:
   - Email: `admin@yourdomain.com` (or `admin@automify.com`)
   - Password: `[your ADMIN_PASSWORD]`

---

## 🔍 **TROUBLESHOOTING**

### **Backend won't start:**
- Check `DATABASE_URL` is correct
- Check logs for error messages
- Verify Supabase database is accessible

### **Frontend can't connect to backend:**
- Check `NEXT_PUBLIC_API_URL` is set correctly
- Should be: `https://[backend-url].onrender.com`
- Make sure backend is running

### **Database connection errors:**
- Verify `DATABASE_URL` format is correct
- Check Supabase dashboard - is database active?
- Check if password needs URL encoding (special characters)

### **Admin user not created:**
- Check `ADMIN_PASSWORD` is set
- Check logs for error messages
- Verify `ADMIN_EMAIL` is set

---

## 📝 **NEXT STEPS**

After successful deployment:

1. ✅ **Update Service Names** (if needed) - Edit `render.yaml`
2. ✅ **Set Up Custom Domain** (optional) - In Render dashboard
3. ✅ **Configure Monitoring** - Set up alerts
4. ✅ **Backup Strategy** - Supabase has automatic backups
5. ✅ **Scale Up** - Upgrade from free tier when ready

---

## 🎉 **SUCCESS!**

Your application should now be live on Render!

- **Backend**: `https://automify-ai-backend.onrender.com`
- **Frontend**: `https://automify-ai-frontend.onrender.com`

---

## 📚 **Additional Resources**

- `RENDER_DEPLOYMENT_STEPS_SUPABASE.md` - Detailed Supabase setup
- `SUPABASE_SETUP_GUIDE.md` - Supabase configuration
- `DATABASE_URL_FIX.md` - Troubleshooting database connection

