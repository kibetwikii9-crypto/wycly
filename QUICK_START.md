# 🚀 Quick Start Guide

## Step 1: Install Dependencies

### Backend:
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Frontend:
```powershell
cd frontend
npm install
```

---

## Step 2: Initialize Database

The database will auto-create tables when you start the server. But first, let's create an admin user.

### Create Admin User:

**Option A: Using Python Script**
```powershell
python create_admin_user.py
```

**Option B: Using API (after server starts)**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123",
    "full_name": "Admin User",
    "role": "admin"
  }'
```

---

## Step 3: Start Servers

### Terminal 1 - Backend:
```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Terminal 2 - Frontend:
```powershell
cd frontend
npm run dev
```

---

## Step 4: Access Dashboard

1. **Open browser:** http://localhost:3000
2. **Login** with your admin credentials
3. **Explore dashboard:**
   - Overview: http://localhost:3000/dashboard
   - Conversations: http://localhost:3000/dashboard/conversations
   - Analytics: http://localhost:3000/dashboard/analytics
   - Knowledge Base: http://localhost:3000/dashboard/knowledge

---

## Step 5: Test Telegram Bot (Optional)

If you want to test the chatbot:

1. **Start ngrok** (in a new terminal):
   ```powershell
   .\ngrok.exe http 8000
   ```

2. **Set webhook** (use the ngrok URL):
   ```powershell
   .\set_webhook.ps1
   ```

3. **Send a message** to your Telegram bot

4. **View conversation** in dashboard: http://localhost:3000/dashboard/conversations

---

## ✅ What's Working

- ✅ Authentication (Login/Register)
- ✅ Dashboard Overview
- ✅ Conversations List
- ✅ Analytics Charts
- ✅ Knowledge Base UI
- ✅ Dark Mode
- ✅ Responsive Layout

---

## 🔧 Troubleshooting

### Backend won't start:
- Check if port 8000 is available
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check database file exists: `curie.db`

### Frontend won't start:
- Check if port 3000 is available
- Verify dependencies: `cd frontend && npm install`
- Check Node.js version (requires Node 18+)

### Can't login:
- Verify user was created: Check database or create new user
- Check backend is running on port 8000
- Check browser console for errors

### No data in dashboard:
- Send some messages via Telegram bot
- Or manually insert test data into database

---

## 📚 Documentation

- **Platform Setup:** See `SAAS_PLATFORM_SETUP.md`
- **Build Summary:** See `PLATFORM_BUILD_SUMMARY.md`
- **AI Engine:** See `AI_ENGINE_SUMMARY.md`
- **API Docs:** http://localhost:8000/docs (when backend is running)

---

## 🎉 You're Ready!

The platform foundation is complete. Start both servers and login to explore the dashboard!



