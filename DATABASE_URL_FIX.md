# 🔧 Database URL Format Fix

## ❌ **Current Error:**

```
failed to resolve host '2023@db.hukdnuglzeoieyfsigqx.supabase.co'
```

This means your `DATABASE_URL` is incorrectly formatted.

---

## ✅ **Correct Format:**

Your Supabase connection string should look like this:

```
postgresql://postgres:YOUR_PASSWORD@db.PROJECT_REF.supabase.co:5432/postgres
```

**Example:**
```
postgresql://postgres:MySecurePassword123@db.abcdefghijklmnop.supabase.co:5432/postgres
```

---

## 🔍 **How to Get the Correct Connection String:**

1. Go to **Supabase Dashboard** → Your Project
2. Click **Settings** (gear icon) → **Database**
3. Scroll to **Connection string** section
4. Select **URI** tab
5. Copy the connection string
6. **Important:** Replace `[YOUR-PASSWORD]` with your actual database password

---

## ⚠️ **Common Issues:**

### **Issue 1: Password Not Replaced**
If you see `[YOUR-PASSWORD]` in the connection string, replace it with your actual password.

### **Issue 2: Special Characters in Password**
If your password has special characters (`@`, `#`, `%`, etc.), they need to be URL-encoded:
- `@` → `%40`
- `#` → `%23`
- `%` → `%25`
- `&` → `%26`
- `+` → `%2B`
- `=` → `%3D`

**Example:**
- Password: `My@Pass#123`
- URL-encoded: `My%40Pass%23123`
- Connection string: `postgresql://postgres:My%40Pass%23123@db.xxxxx.supabase.co:5432/postgres`

### **Issue 3: Wrong Format**
Make sure the format is exactly:
```
postgresql://postgres:PASSWORD@db.PROJECT_REF.supabase.co:5432/postgres
```

Not:
- `postgresql://2023@db...` ❌
- `postgresql://postgres@2023@db...` ❌
- `postgresql://postgres:2023@db...` ✅ (if password is "2023")

---

## 🔧 **Fix in Render:**

1. Go to **Render Dashboard** → **Backend Service** → **Environment** tab
2. Find `DATABASE_URL`
3. Update it with the correct format:
   ```
   postgresql://postgres:YOUR_ACTUAL_PASSWORD@db.xxxxx.supabase.co:5432/postgres
   ```
4. **Save** and **restart** the service

---

## ✅ **Verify:**

After updating, check backend logs. You should see:
```
✅ Database initialized successfully
```

Instead of:
```
⚠️  Database initialization error
```

---

## 🧪 **Test Connection String:**

You can test if your connection string is correct by using this Python script:

```python
import psycopg
from urllib.parse import urlparse

# Your connection string
conn_string = "postgresql://postgres:PASSWORD@db.xxxxx.supabase.co:5432/postgres"

try:
    # Parse to check format
    parsed = urlparse(conn_string)
    print(f"Host: {parsed.hostname}")
    print(f"Port: {parsed.port}")
    print(f"Database: {parsed.path[1:]}")
    print(f"User: {parsed.username}")
    
    # Try to connect
    conn = psycopg.connect(conn_string)
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

---

**Fix your DATABASE_URL in Render and restart the service!**

