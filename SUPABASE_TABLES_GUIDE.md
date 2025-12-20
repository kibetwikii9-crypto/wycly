# 📊 Supabase Tables - Creation & Verification Guide

## ✅ **Tables Are Created Automatically!**

Your tables are **automatically created** when the backend starts!

### **How It Works:**

1. When backend starts → calls `init_db()`
2. `init_db()` creates all tables from `app/models.py`
3. Tables are created in your Supabase database
4. **No manual SQL needed!**

**Check backend logs for:**
```
✅ Database initialized successfully
```

This means all tables were created.

---

## 📋 **All Tables (10 Total)**

Your application automatically creates these tables:

1. **users** - User accounts (admin, agents, etc.)
2. **businesses** - Business/workspace information
3. **channel_integrations** - Telegram, WhatsApp integrations
4. **conversations** - Chat conversations
5. **messages** - Individual messages
6. **leads** - Lead tracking
7. **knowledge_entries** - FAQ/knowledge base
8. **conversation_memory** - AI conversation context
9. **analytics_events** - Analytics tracking
10. **ad_assets** - Ad and video assets

---

## 🔍 **How to Verify Tables in Supabase**

### **Method 1: Table Editor (Easiest)**

1. Go to **Supabase Dashboard** → Your Project
2. Click **"Table Editor"** in left sidebar
3. You should see all 10 tables listed
4. Click any table to view its data

**If you see the tables:** ✅ They're created!

**If tables are empty:** That's normal! They'll fill up as you use the app.

---

### **Method 2: SQL Editor**

1. Go to **Supabase Dashboard** → **SQL Editor**
2. Click **"New query"**
3. Run this SQL:

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE'
ORDER BY table_name;
```

**Expected output (10 tables):**
```
ad_assets
analytics_events
channel_integrations
conversation_memory
conversations
knowledge_entries
leads
messages
businesses
users
```

---

### **Method 3: Check Backend Logs**

In Render Dashboard → Backend Service → Logs:

Look for:
```
✅ Database initialized successfully
```

If you see this, tables were created!

---

## 🚨 **If Tables Don't Exist**

### **Solution 1: Restart Backend (Recommended)**

1. Go to Render Dashboard → Backend Service
2. Click **"Manual Deploy"** → **"Clear build cache & deploy"**
3. Wait for deployment (2-3 minutes)
4. Check logs for: `✅ Database initialized successfully`

This will trigger table creation.

---

### **Solution 2: Verify Database Connection**

If tables aren't being created, check:

1. **DATABASE_URL is set correctly** in Render environment variables
2. **Backend logs** show database connection success
3. **Supabase project is active** (not paused)

---

## 📝 **Verify Admin User**

After tables are created, check if admin user exists:

**In Supabase SQL Editor:**
```sql
SELECT id, email, role, is_active 
FROM users 
WHERE email = 'admin@curie.com';
```

**Expected result:**
```
id | email            | role  | is_active
---|------------------|-------|----------
1  | admin@curie.com  | admin | true
```

**If no rows:** Admin user wasn't created yet (check backend logs for auto-creation message).

---

## ✅ **Quick Checklist**

- [ ] Backend logs show: `✅ Database initialized successfully`
- [ ] Supabase Table Editor shows all 10 tables
- [ ] `users` table exists (check in Table Editor)
- [ ] Admin user exists in `users` table (after auto-creation)

---

## 🎯 **Summary**

**You don't need to create tables manually!**

✅ **Tables are created automatically** when backend starts
✅ **Just verify** they exist in Supabase Table Editor
✅ **Admin user is created automatically** on startup

**Everything is automatic - just check Supabase dashboard to verify! 📊**
