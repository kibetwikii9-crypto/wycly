# 🚀 Render Deployment Guide for Curie

This guide will walk you through deploying your Curie SaaS platform to Render.

---

## 📋 **PRE-DEPLOYMENT CHECKLIST**

Before we start, I need you to provide/confirm the following:

### ✅ **1. Information I Need From You:**

- [ ] **Render Account**: Do you have a Render account? (If not, sign up at https://render.com - free tier available)
- [ ] **GitHub/GitLab Repository**: Is your code in a Git repository? (GitHub, GitLab, or Bitbucket)
  - Repository URL: `_________________`
- [ ] **Telegram Bot Token**: Your Telegram bot token (you should already have this)
  - Bot Token: `_________________`
- [ ] **Domain (Optional)**: Do you want a custom domain? (e.g., `curie.yourdomain.com`)
  - Custom Domain: `_________________` (or leave blank for Render subdomain)

### ✅ **2. What I Will Prepare For You:**

- [ ] `render.yaml` - Render configuration file
- [ ] Updated `database.py` - PostgreSQL support for Render
- [ ] Updated CORS settings - Allow Render frontend URL
- [ ] Environment variables template
- [ ] Build scripts if needed

---

## 🏗️ **DEPLOYMENT ARCHITECTURE**

We'll deploy **2 services** on Render:

1. **Backend Service** (FastAPI)
   - Type: Web Service
   - Runtime: Python 3.12
   - Database: PostgreSQL (Render managed)

2. **Frontend Service** (Next.js)
   - Type: Web Service
   - Runtime: Node.js 20
   - Build Command: `npm install && npm run build`
   - Start Command: `npm start`

---

## 📝 **STEP-BY-STEP DEPLOYMENT PROCESS**

### **Phase 1: Preparation (I'll Do This)**

1. ✅ Create `render.yaml` configuration
2. ✅ Update database configuration for PostgreSQL
3. ✅ Update CORS settings for production
4. ✅ Create environment variables template
5. ✅ Test database migration locally (if possible)

### **Phase 2: Your Actions (You'll Do This)**

#### **Step 1: Push Code to Git Repository**

```bash
# If you haven't already, initialize git and push to GitHub/GitLab
git init
git add .
git commit -m "Initial commit - Ready for Render deployment"
git remote add origin YOUR_REPO_URL
git push -u origin main
```

#### **Step 2: Create Render Account & Connect Repository**

1. Go to https://render.com
2. Sign up / Log in
3. Click **"New +"** → **"Blueprint"**
4. Connect your Git repository
5. Render will detect `render.yaml` automatically

#### **Step 3: Configure Environment Variables**

In Render dashboard, you'll need to set these environment variables:

**Backend Service:**
```
BOT_TOKEN=your_telegram_bot_token_here
PUBLIC_URL=https://your-backend-service.onrender.com
DATABASE_URL=postgresql://... (Render will provide this automatically)
LOG_LEVEL=INFO
OPENAI_API_KEY= (leave empty for now)
```

**Frontend Service:**
```
NEXT_PUBLIC_API_URL=https://your-backend-service.onrender.com
```

#### **Step 4: Deploy**

1. Render will automatically:
   - Create PostgreSQL database
   - Build and deploy backend
   - Build and deploy frontend
   - Set up environment variables

2. Wait for deployment to complete (5-10 minutes)

#### **Step 5: Create Admin User**

After deployment, you'll need to create an admin user. I'll provide a script for this.

#### **Step 6: Update Telegram Webhook**

Update your Telegram bot webhook to point to your Render backend URL:
```
https://your-backend-service.onrender.com/telegram/webhook
```

---

## 🔧 **CONFIGURATION DETAILS**

### **Database Migration**

- **Local**: SQLite (`sqlite:///./curie.db`)
- **Render**: PostgreSQL (managed by Render)
- **Migration**: Automatic via `init_db()` on startup

### **CORS Settings**

- **Local**: `http://localhost:3000`
- **Render**: Your Render frontend URL
- **Update**: I'll update `app/main.py` to support both

### **Environment Variables**

All sensitive data will be stored in Render's environment variables (secure).

---

## ⚠️ **IMPORTANT NOTES**

1. **Free Tier Limitations:**
   - Services spin down after 15 minutes of inactivity
   - First request after spin-down takes ~30 seconds
   - Consider upgrading for production

2. **Database:**
   - Render provides PostgreSQL automatically
   - Database URL is auto-injected as `DATABASE_URL`
   - No manual database setup needed

3. **File Storage:**
   - SQLite files won't persist (ephemeral filesystem)
   - Use PostgreSQL (which we'll configure)
   - Static files should be in Git or external storage

4. **Knowledge Base:**
   - `faq.json` must be in the repository
   - Or we can load it from environment variable

---

## 🎯 **NEXT STEPS**

1. **Review this guide** and confirm you have all the information
2. **Let me know when you're ready** - I'll prepare all the files
3. **Push your code to Git** (if not already done)
4. **Follow the deployment steps** above

---

## ❓ **QUESTIONS TO ANSWER**

Before I prepare the files, please confirm:

1. ✅ Do you have a Git repository set up?
2. ✅ What's your Telegram bot token? (I can help you find it if needed)
3. ✅ Do you want a custom domain or use Render's subdomain?
4. ✅ Are you ready to deploy, or do you want to test locally first?

---

**Once you confirm, I'll prepare all the deployment files! 🚀**

