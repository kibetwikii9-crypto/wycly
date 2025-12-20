# 👤 Create Admin User - Step by Step

## 🎯 **Why You Need This**

The admin user doesn't exist automatically. You need to create it once after deploying to Render.

---

## ✅ **Step-by-Step Instructions**

### **Step 1: Open Render Shell**

1. Go to **Render Dashboard**: https://dashboard.render.com
2. Click on your **Backend Service** (`curie-backend`)
3. Click on the **"Shell"** tab (in the left sidebar)
4. Click **"Connect"** to open a shell session

---

### **Step 2: Run the Admin Creation Script**

In the Render Shell, run:

```bash
python create_admin_auto.py
```

**Expected Output:**
```
🔧 Initializing database...
✅ Database initialized
✅ Admin user created successfully!
   Email: admin@curie.com
   Password: admin123
   Role: admin

📝 Login credentials:
   Email: admin@curie.com
   Password: admin123
```

**If user already exists:**
```
✅ Admin user already exists: admin@curie.com
   You can login with this account
```

---

### **Step 3: Verify User Was Created**

You can verify by checking the database or trying to login.

---

## 🔑 **Login Credentials**

After creating the admin user:

- **Email:** `admin@curie.com`
- **Password:** `admin123`
- **Role:** `admin`

---

## 🚨 **Troubleshooting**

### **Issue: "Module not found" or "No such file"**

**Solution:** Make sure you're in the project root directory:
```bash
cd /opt/render/project/src
python create_admin_auto.py
```

### **Issue: "Database connection failed"**

**Solution:** 
1. Check that `DATABASE_URL` is set in Render environment variables
2. Verify the connection string is correct (Supabase format)
3. Check backend logs for database errors

### **Issue: "User already exists"**

**Solution:** This is fine! The user already exists. Just use the login credentials.

---

## ✅ **After Creating Admin User**

1. Go to your frontend: `https://curie-frontend-8hvz.onrender.com/login`
2. Login with:
   - Email: `admin@curie.com`
   - Password: `admin123`
3. You should be redirected to the dashboard

---

## 📝 **Quick Command Reference**

```bash
# In Render Shell
python create_admin_auto.py
```

That's it! The script handles everything automatically.

---

**Once the admin user is created, you can login to the dashboard! 🎉**

