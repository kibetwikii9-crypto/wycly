# Viewing Database with DB Browser for SQLite

## 📍 Database File Location

**File:** `curie.db`

**Location:** Project root directory
```
C:\Users\Kibee\Desktop\projects\Curie\curie.db
```

---

## 🔧 How to Open in DB Browser for SQLite

### Step 1: Open DB Browser for SQLite
- Launch DB Browser for SQLite application

### Step 2: Open Database
1. Click **"Open Database"** button (or File → Open Database)
2. Navigate to your project folder:
   ```
   C:\Users\Kibee\Desktop\projects\Curie
   ```
3. Select `curie.db` file
4. Click **"Open"**

### Step 3: View Data
1. Click on the **"Browse Data"** tab
2. Select **"conversations"** table from the dropdown
3. You'll see all saved conversations!

---

## 📊 What You'll See

### Conversations Table Structure:

| Column       | Type     | Description                    |
|--------------|----------|--------------------------------|
| id           | INTEGER  | Primary key (auto-increment)   |
| user_id      | TEXT     | Platform-specific user ID      |
| channel      | TEXT     | Messaging platform             |
| user_message | TEXT     | Original user message          |
| bot_reply    | TEXT     | AI-generated response          |
| intent       | TEXT     | Detected intent                |
| created_at   | DATETIME | Conversation timestamp         |

### Example Data:

| id | user_id    | channel  | user_message      | bot_reply                    | intent   | created_at           |
|----|------------|----------|-------------------|------------------------------|----------|----------------------|
| 1  | 123456789  | telegram | "What's the price?" | "We offer flexible plans..." | pricing  | 2024-01-15 10:30:00 |
| 2  | 123456789  | telegram | "Hello"           | "Hello! 👋 Welcome!..."       | greeting | 2024-01-15 10:31:00 |

---

## 🔍 Useful Queries

### View All Conversations:
```sql
SELECT * FROM conversations;
```

### View Recent Conversations:
```sql
SELECT * FROM conversations 
ORDER BY created_at DESC 
LIMIT 10;
```

### Count Conversations by Intent:
```sql
SELECT intent, COUNT(*) as count 
FROM conversations 
GROUP BY intent;
```

### View Conversations for a Specific User:
```sql
SELECT * FROM conversations 
WHERE user_id = '123456789' 
ORDER BY created_at DESC;
```

### View Conversations by Channel:
```sql
SELECT * FROM conversations 
WHERE channel = 'telegram' 
ORDER BY created_at DESC;
```

---

## 💡 Tips

1. **Database Created On First Save:**
   - The database file is created when the server starts
   - Tables are created when `init_db()` runs
   - Data appears when first conversation is saved

2. **Refresh Data:**
   - Click **"Refresh"** button in DB Browser to see new data
   - Or close and reopen the database

3. **Export Data:**
   - Use **File → Export → Export to CSV** to export data
   - Useful for analysis or backups

4. **Edit Data (if needed):**
   - Switch to **"Browse Data"** tab
   - Click on a cell to edit
   - Click **"Write Changes"** to save

---

## 🎯 Quick Access

**Full Path:**
```
C:\Users\Kibee\Desktop\projects\Curie\curie.db
```

**To Open:**
1. Open DB Browser for SQLite
2. File → Open Database
3. Navigate to: `C:\Users\Kibee\Desktop\projects\Curie`
4. Select: `curie.db`
5. Click Open

---

## ✅ Verification

After opening the database, you should see:
- ✅ `conversations` table in the table list
- ✅ Table structure with all columns
- ✅ Data rows (if any conversations have been saved)

If the table doesn't exist yet:
- The database will be created when the server starts
- Tables will be created automatically
- Data will appear after first conversation is saved



