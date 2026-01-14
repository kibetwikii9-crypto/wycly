# 🚀 Render Deployment with Supabase - Step-by-Step Instructions

This is an updated version of the deployment guide that uses **Supabase** instead of Render's PostgreSQL.

---

## 📋 **BEFORE YOU START - Information Needed**

1. ✅ **Git Repository URL**: Where is your code hosted?
   - GitHub: `https://github.com/yourusername/wycly`
   - GitLab: `https://gitlab.com/yourusername/wycly`
   - Or other: `_________________`

2. ✅ **Telegram Bot Token**: Your bot token
   - Token: `_________________`

3. ✅ **Supabase Connection String**: From Supabase setup
   - Connection String: `postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres`
   - See `SUPABASE_SETUP_GUIDE.md` for setup instructions

---

## 🎯 **DEPLOYMENT STEPS**

### **Step 1: Set Up Supabase (If Not Done)**

1. Follow `SUPABASE_SETUP_GUIDE.md` to create your Supabase project
2. Get your connection string
3. Save it securely

**✅ Checkpoint**: You have your Supabase connection string.

---

### **Step 2: Push Code to Git Repository**

If your code isn't in Git yet:

```powershell
# Navigate to project directory
cd C:\Users\Kibee\Desktop\projects\Curie

# Check if already committed
git status

# If not committed, add and commit
git add .
git commit -m "Ready for Render deployment with Supabase"

# Add remote (replace with your repository URL)
git remote add origin https://github.com/yourusername/curie.git

# Push to repository
git push -u origin main
```

**✅ Checkpoint**: Your code is in GitHub/GitLab/Bitbucket.

---

### **Step 3: Create Render Account**

1. Go to **https://render.com**
2. Click **"Get Started for Free"** or **"Sign Up"**
3. Sign up with GitHub/GitLab (recommended) or email
4. Verify your email if required

**✅ Checkpoint**: You should be logged into Render dashboard.

---

### **Step 4: Create New Blueprint**

1. In Render dashboard, click **"New +"** button (top right)
2. Select **"Blueprint"**
3. Connect your Git repository:
   - Click **"Connect account"** (GitHub/GitLab)
   - Authorize Render to access your repositories
   - Select your repository: `curie` (or whatever you named it)
   - Click **"Connect"**

**✅ Checkpoint**: Render should show your repository connected.

---

### **Step 5: Configure Blueprint**

1. Render will automatically detect `render.yaml` in your repository
2. You'll see a preview of the services:
   - `wycly-backend` (FastAPI)
   - `wycly-frontend` (Next.js)
   - **Note**: No database service (we're using Supabase!)
3. Click **"Apply"** to create the services

**✅ Checkpoint**: Render will start creating your services (this takes 5-10 minutes).

---

### **Step 6: Set Environment Variables**

While services are deploying, set environment variables:

#### **For Backend Service (`wycly-backend`):**

1. Go to your **Dashboard** → Click on **`wycly-backend`** service
2. Go to **"Environment"** tab
3. Add/Update these variables:

```
DATABASE_URL = postgresql://postgres:yourpassword@db.xxxxx.supabase.co:5432/postgres
SECRET_KEY = your_strong_secret_key_here
LOG_LEVEL = INFO
OPENAI_API_KEY = (leave empty)
```

**⚠️ Important**: 
- Replace `yourpassword` with your Supabase database password
- Replace `xxxxx` with your Supabase project reference
- Get the full connection string from Supabase dashboard (Settings → Database → Connection string → URI)
- Generate a strong `SECRET_KEY` (use: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)

**Note:** BOT_TOKEN and ADMIN credentials are NOT needed. Users connect their own Telegram bots through the dashboard and create accounts through registration.

**Note**: These are auto-set by Render:
- `PUBLIC_URL` (your backend URL)
- `FRONTEND_URL` (your frontend URL)

#### **For Frontend Service (`wycly-frontend`):**

1. Go to **Dashboard** → Click on **`wycly-frontend`** service
2. Go to **"Environment"** tab
3. `NEXT_PUBLIC_API_URL` is automatically set by Render (no action needed)

**✅ Checkpoint**: Environment variables are set.

---

### **Step 7: Wait for Deployment**

1. Monitor the **"Events"** tab in each service
2. Wait for **"Live"** status (green checkmark)
3. This typically takes 5-10 minutes for first deployment

**✅ Checkpoint**: All services show "Live" status.

---

### **Step 8: Get Your Service URLs**

After deployment, you'll get URLs like:

- **Backend**: `https://wycly-backend-xxxx.onrender.com`
- **Frontend**: `https://wycly-frontend-xxxx.onrender.com`

**Save these URLs!** You'll need them.

---

### **Step 9: Verify Database Connection**

1. Check backend logs (Render dashboard → Backend service → "Logs" tab)
2. Look for: `✅ Database initialized successfully`
3. If you see errors, verify your `DATABASE_URL` is correct

**✅ Checkpoint**: Database connection is working.

---

### **Step 10: Create Admin User**

After backend is live, create an admin user:

1. Go to your backend service → **"Shell"** tab
2. Run this command:

1. Go to your frontend URL: `https://wycly-frontend-xxxx.onrender.com`
2. Click **"Sign Up"** to create your account
3. Fill in your details (email, password, name)
4. Click **"Sign Up"**
5. You'll be automatically logged in

**✅ Checkpoint**: Account created and logged in.

---

### **Step 11: Update Telegram Webhook**

1. Get your backend URL: `https://wycly-backend-xxxx.onrender.com`
2. Update Telegram webhook:

**Connect Telegram Bot via Dashboard:**
1. Go to your frontend: `https://wycly-frontend-xxxx.onrender.com`
2. Login to your account (create one if needed)
3. Go to **Integrations → Telegram**
4. Click **"Connect Bot"**
5. Enter your bot token (from @BotFather)
6. Click **"Connect"**
7. Webhook will be automatically configured

**✅ Checkpoint**: Telegram bot connected.

---

### **Step 12: Test Your Deployment**

1. **Test Backend**: Visit `https://wycly-backend-xxxx.onrender.com/health`
   - Should return: `{"status":"ok"}`

2. **Test Frontend**: Visit `https://wycly-frontend-xxxx.onrender.com`
   - Should show login page

3. **Create Account and Login**:
   - Go to frontend URL
   - Click **"Sign Up"** to create your account
   - Fill in your details and register
   - You'll be automatically logged in

4. **Test Telegram Bot**: Send a message to your Telegram bot
   - Should receive a response

5. **Test Database**: Check Supabase dashboard → Table Editor
   - Should see tables created (users, conversations, etc.)

**✅ Checkpoint**: Everything works!

---

## 🔧 **TROUBLESHOOTING**

### **Issue: Database connection failed**

**Solution**: 
1. Verify `DATABASE_URL` is correct in Render environment variables
2. Check Supabase dashboard → Settings → Database → Connection string
3. Make sure password doesn't have special characters that need URL encoding
4. Check backend logs for specific error messages

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

### **Issue: Tables not created**

**Solution**:
1. Check backend logs for database initialization errors
2. Verify `DATABASE_URL` is correct
3. Manually run `init_db()` via Render Shell if needed

---

## 📝 **POST-DEPLOYMENT CHECKLIST**

- [ ] All services are "Live"
- [ ] Backend health check works
- [ ] Frontend loads correctly
- [ ] Database connection verified
- [ ] Tables created in Supabase
- [ ] Admin user created
- [ ] Can log in to dashboard
- [ ] Telegram webhook set
- [ ] Bot responds to messages

---

## 🎉 **YOU'RE DONE!**

Your Curie platform is now live on Render with Supabase!

**Next Steps**:
- Monitor logs for any issues
- Consider upgrading from free tier for production
- Set up custom domain (optional)
- Configure Supabase backups (automatic on paid plans)

---

## ❓ **NEED HELP?**

If you encounter issues:
1. Check Render logs
2. Check Supabase dashboard
3. Review `SUPABASE_SETUP_GUIDE.md` for database setup
4. Review this guide for deployment steps

---

## 🔄 **DIFFERENCES FROM RENDER POSTGRESQL**

**What Changed:**
- ✅ No Render database service (using Supabase instead)
- ✅ `DATABASE_URL` must be set manually (from Supabase)
- ✅ More control over database (Supabase dashboard)
- ✅ Better free tier (Supabase free tier is more generous)

**What Stayed the Same:**
- ✅ Same application code (no changes needed)
- ✅ Same deployment process
- ✅ Same environment variables (except DATABASE_URL)

---

**Ready to deploy! 🚀**

