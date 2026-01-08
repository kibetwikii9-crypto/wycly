# 🚀 Render Deployment - Step-by-Step Instructions

## 📋 **BEFORE YOU START - Information I Need**

Please provide the following:

1. ✅ **Git Repository URL**: Where is your code hosted?
   - GitHub: `https://github.com/yourusername/curie`
   - GitLab: `https://gitlab.com/yourusername/curie`
   - Or other: `_________________`

2. ✅ **Telegram Bot Token**: Your bot token (you should have this)
   - Token: `_________________`

3. ✅ **Custom Domain** (Optional): Do you want a custom domain?
   - Domain: `_________________` (or leave blank)

---

## 🎯 **DEPLOYMENT STEPS**

### **Step 1: Push Code to Git Repository**

If your code isn't in Git yet:

```powershell
# Navigate to project directory
cd C:\Users\Kibee\Desktop\projects\Curie

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Ready for Render deployment"

# Add remote (replace with your repository URL)
git remote add origin https://github.com/yourusername/curie.git

# Push to repository
git push -u origin main
```

**✅ Checkpoint**: Your code should now be in GitHub/GitLab/Bitbucket.

---

### **Step 2: Create Render Account**

1. Go to **https://render.com**
2. Click **"Get Started for Free"** or **"Sign Up"**
3. Sign up with GitHub/GitLab (recommended) or email
4. Verify your email if required

**✅ Checkpoint**: You should be logged into Render dashboard.

---

### **Step 3: Create New Blueprint**

1. In Render dashboard, click **"New +"** button (top right)
2. Select **"Blueprint"**
3. Connect your Git repository:
   - Click **"Connect account"** (GitHub/GitLab)
   - Authorize Render to access your repositories
   - Select your repository: `curie` (or whatever you named it)
   - Click **"Connect"**

**✅ Checkpoint**: Render should show your repository connected.

---

### **Step 4: Configure Blueprint**

1. Render will automatically detect `render.yaml` in your repository
2. You'll see a preview of the services:
   - `automify-ai-backend` (FastAPI)
   - `automify-ai-frontend` (Next.js)
   - **Note**: No database service (we're using Supabase!)
3. Click **"Apply"** to create the services

**✅ Checkpoint**: Render will start creating your services (this takes 5-10 minutes).

---

### **Step 5: Set Environment Variables**

While services are deploying, set environment variables:

#### **For Backend Service (`automify-ai-backend`):**

1. Go to your **Dashboard** → Click on **`automify-ai-backend`** service
2. Go to **"Environment"** tab
3. Add/Update these variables:

```
BOT_TOKEN = your_telegram_bot_token_here
DATABASE_URL = postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres
SECRET_KEY = your_strong_secret_key_here
ADMIN_PASSWORD = your_secure_admin_password
LOG_LEVEL = INFO
OPENAI_API_KEY = (leave empty)
```

**Note**: `PUBLIC_URL` and `FRONTEND_URL` are automatically set by Render. `DATABASE_URL` must be set manually (Supabase connection string).

#### **For Frontend Service (`automify-ai-frontend`):**

1. Go to **Dashboard** → Click on **`automify-ai-frontend`** service
2. Go to **"Environment"** tab
3. `NEXT_PUBLIC_API_URL` is automatically set by Render (no action needed)

**✅ Checkpoint**: Environment variables are set.

---

### **Step 6: Wait for Deployment**

1. Monitor the **"Events"** tab in each service
2. Wait for **"Live"** status (green checkmark)
3. This typically takes 5-10 minutes for first deployment

**✅ Checkpoint**: All services show "Live" status.

---

### **Step 7: Get Your Service URLs**

After deployment, you'll get URLs like:

- **Backend**: `https://automify-ai-backend-xxxx.onrender.com`
- **Frontend**: `https://automify-ai-frontend-xxxx.onrender.com`

**Save these URLs!** You'll need them.

---

### **Step 8: Create Admin User**

After backend is live, create an admin user:

1. Go to your backend service → **"Shell"** tab
2. Run this command:

```bash
python create_admin_auto.py
```

Or use the Render **"Shell"** feature to run:

```bash
cd /opt/render/project/src
python create_admin_auto.py
```

**✅ Checkpoint**: Admin user created.

---

### **Step 9: Update Telegram Webhook**

1. Get your backend URL: `https://automify-ai-backend-xxxx.onrender.com`
2. Update Telegram webhook:

**Option A: Using Browser**
```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://automify-ai-backend-xxxx.onrender.com/telegram/webhook
```

**Option B: Using PowerShell**
```powershell
$botToken = "your_bot_token_here"
$webhookUrl = "https://automify-ai-backend-xxxx.onrender.com/telegram/webhook"
Invoke-WebRequest -Uri "https://api.telegram.org/bot$botToken/setWebhook?url=$webhookUrl"
```

**✅ Checkpoint**: Telegram webhook updated.

---

### **Step 10: Test Your Deployment**

1. **Test Backend**: Visit `https://automify-ai-backend-xxxx.onrender.com/health`
   - Should return: `{"status":"ok"}`

2. **Test Frontend**: Visit `https://automify-ai-frontend-xxxx.onrender.com`
   - Should show login page

3. **Test Login**:
   - Email: `admin@curie.com` (or your ADMIN_EMAIL env var)
   - Password: (your ADMIN_PASSWORD env var)

4. **Test Telegram Bot**: Send a message to your Telegram bot
   - Should receive a response

**✅ Checkpoint**: Everything works!

---

## 🔧 **TROUBLESHOOTING**

### **Issue: Services won't start**

**Solution**: Check the **"Logs"** tab for errors. Common issues:
- Missing environment variables
- Database connection issues
- Build errors

### **Issue: Frontend can't connect to backend**

**Solution**: 
1. Check `NEXT_PUBLIC_API_URL` in frontend environment variables
2. Verify backend URL is correct
3. Check CORS settings in backend

### **Issue: Database connection failed**

**Solution**:
1. Verify `DATABASE_URL` is set (must be set manually with Supabase connection string)
2. Check Supabase database is accessible
3. Verify `psycopg[binary]` is in `requirements.txt`

### **Issue: Telegram webhook not working**

**Solution**:
1. Verify webhook URL is correct
2. Check backend logs for errors
3. Test webhook: `https://api.telegram.org/bot<TOKEN>/getWebhookInfo`

---

## 📝 **POST-DEPLOYMENT CHECKLIST**

- [ ] All services are "Live"
- [ ] Backend health check works
- [ ] Frontend loads correctly
- [ ] Admin user created
- [ ] Can log in to dashboard
- [ ] Telegram webhook set
- [ ] Bot responds to messages
- [ ] Database is accessible

---

## 🎉 **YOU'RE DONE!**

Your Curie platform is now live on Render!

**Next Steps**:
- Monitor logs for any issues
- Consider upgrading from free tier for production
- Set up custom domain (optional)
- Configure backups for database

---

## ❓ **NEED HELP?**

If you encounter issues:
1. Check Render logs
2. Check this guide
3. Review `RENDER_DEPLOYMENT_GUIDE.md` for more details

