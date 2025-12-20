# 🗄️ Supabase Setup Guide for Curie

This guide will help you set up Supabase as your PostgreSQL database for the Curie platform.

---

## 📋 **STEP 1: Create Supabase Account**

1. Go to **https://supabase.com**
2. Click **"Start your project"** or **"Sign Up"**
3. Sign up with GitHub (recommended) or email
4. Verify your email if required

**✅ Checkpoint**: You should be logged into Supabase dashboard.

---

## 📋 **STEP 2: Create a New Project**

1. Click **"New Project"** button
2. Fill in the project details:
   - **Name**: `curie` (or any name you prefer)
   - **Database Password**: Create a strong password (save this!)
   - **Region**: Choose closest to your users
   - **Pricing Plan**: Free tier is fine to start
3. Click **"Create new project"**
4. Wait 2-3 minutes for project to be created

**✅ Checkpoint**: Your project should be created and ready.

---

## 📋 **STEP 3: Get Your Database Connection String**

1. In your Supabase project dashboard, go to **"Settings"** (gear icon)
2. Click **"Database"** in the left sidebar
3. Scroll down to **"Connection string"** section
4. Select **"URI"** tab
5. Copy the connection string (it looks like this):

```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
```

**⚠️ Important**: Replace `[YOUR-PASSWORD]` with the password you set when creating the project.

**Example**:
```
postgresql://postgres:MySecurePassword123@db.abcdefghijklmnop.supabase.co:5432/postgres
```

**✅ Checkpoint**: You have your Supabase connection string.

---

## 📋 **STEP 4: Update Connection String Format**

Supabase uses PostgreSQL, but the connection string format might need adjustment. 

**If your connection string has `[YOUR-PASSWORD]` placeholder:**
- Replace it with your actual password
- The final string should look like: `postgresql://postgres:actualpassword@db.xxxxx.supabase.co:5432/postgres`

**✅ Checkpoint**: You have a complete connection string with your password.

---

## 📋 **STEP 5: Test Connection (Optional)**

You can test the connection using a PostgreSQL client or Python:

```python
# Test script (optional)
import psycopg2

conn_string = "postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres"
try:
    conn = psycopg2.connect(conn_string)
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

---

## 📋 **STEP 6: Set Up Database Tables**

Your application will automatically create tables on first startup, but you can also do it manually:

1. Go to Supabase dashboard → **"SQL Editor"**
2. The tables will be created automatically when your backend starts
3. Or you can run the `init_db()` function manually

---

## 🔧 **CONFIGURATION FOR RENDER**

When deploying to Render, you'll set the `DATABASE_URL` environment variable:

1. In Render dashboard → Your backend service → **"Environment"** tab
2. Add/Update:
   ```
   DATABASE_URL = postgresql://postgres:yourpassword@db.xxxxx.supabase.co:5432/postgres
   ```
3. Replace `yourpassword` and `xxxxx` with your actual values

---

## 🔒 **SECURITY BEST PRACTICES**

1. **Never commit your connection string to Git**
   - It contains your password
   - Always use environment variables

2. **Use Connection Pooling** (Supabase provides this)
   - Supabase connection strings support connection pooling
   - For production, consider using the pooler URL

3. **Rotate Passwords Regularly**
   - Update password in Supabase dashboard
   - Update `DATABASE_URL` in Render environment variables

---

## 📝 **SUPABASE CONNECTION STRING FORMATS**

### **Direct Connection** (for migrations, admin tasks):
```
postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### **Connection Pooler** (for production apps):
```
postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

**For now, use the Direct Connection format.**

---

## ✅ **VERIFICATION CHECKLIST**

- [ ] Supabase account created
- [ ] Project created
- [ ] Database password saved securely
- [ ] Connection string copied
- [ ] Connection string has actual password (not placeholder)
- [ ] Ready to add to Render environment variables

---

## 🚀 **NEXT STEPS**

1. **Save your connection string** securely
2. **Add it to Render** when deploying (see `RENDER_DEPLOYMENT_STEPS.md`)
3. **Test the connection** after deployment

---

## ❓ **TROUBLESHOOTING**

### **Issue: Connection refused**
- Check if your IP is allowed in Supabase (Settings → Database → Connection Pooling)
- Supabase allows all IPs by default, but check firewall settings

### **Issue: Authentication failed**
- Verify password is correct
- Make sure you replaced `[YOUR-PASSWORD]` with actual password

### **Issue: Database not found**
- Default database name is `postgres`
- Don't change it unless you created a custom database

---

## 📚 **ADDITIONAL RESOURCES**

- Supabase Docs: https://supabase.com/docs
- PostgreSQL Connection Strings: https://supabase.com/docs/guides/database/connecting-to-postgres

---

**Your Supabase database is ready! 🎉**

