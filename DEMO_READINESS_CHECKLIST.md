# Demo Readiness Checklist

## 🎯 Pre-Demo Verification (Run 1 hour before demo)

### System Health Checks

#### Backend Server
- [ ] Backend server is running
- [ ] No error logs in console
- [ ] Health endpoint responds: `curl http://localhost:8000/health`
- [ ] Database is accessible
- [ ] Knowledge base is loaded (check logs for "Knowledge base loaded successfully")

**Command to verify:**
```bash
# Check backend health
curl http://localhost:8000/health

# Check if server is running
# Should see: {"status": "ok"}
```

#### Frontend Server
- [ ] Frontend server is running
- [ ] Dashboard loads at http://localhost:3000
- [ ] No console errors in browser
- [ ] Login page works
- [ ] Can log in with admin credentials

**Credentials:**
- Email: `admin@curie.com`
- Password: `admin123`

#### Telegram Bot
- [ ] Telegram bot is connected
- [ ] Webhook is configured correctly
- [ ] Bot responds to test messages
- [ ] Can send and receive messages

**Test Command:**
```bash
# Send test message via Telegram
# Bot should respond within 1-2 seconds
```

#### Database
- [ ] Database file exists (`curie.db`)
- [ ] Tables are created
- [ ] Can query conversations (optional: pre-populate with sample data)

**Verify:**
```python
# Quick database check
python -c "from app.database import get_db_context; from app.models import Conversation; db = next(get_db_context()); print(f'Conversations: {db.query(Conversation).count()}')"
```

---

### Feature Verification

#### AI Brain
- [ ] Intent detection works (greeting, pricing, help, human, unknown)
- [ ] Knowledge base lookup works
- [ ] Memory system works (remembers previous intents)
- [ ] Edge case handling works (spam, long messages, emojis)

**Test Messages:**
1. "Hello" → Should detect greeting intent
2. "What's your pricing?" → Should use knowledge base
3. "Hi again" → Should recognize returning user
4. "Help me" → Should detect help intent

#### Dashboard
- [ ] Overview page loads
- [ ] Conversations page shows data
- [ ] Analytics display correctly
- [ ] Real-time updates work (new conversations appear)

**Verify:**
- Navigate to http://localhost:3000/dashboard
- Check all sections load
- Send test message, verify it appears in dashboard

#### Knowledge Base
- [ ] `faq.json` file exists
- [ ] Knowledge base is loaded on startup
- [ ] Questions match knowledge base entries
- [ ] Answers are accurate

**Test:**
- Send: "What is your pricing?" → Should return FAQ answer
- Send: "How do I get started?" → Should return FAQ answer

---

### Data Preparation (Optional but Recommended)

#### Sample Conversations
- [ ] Create 5-10 sample conversations in database
- [ ] Mix of different intents (greeting, pricing, help)
- [ ] Different timestamps (some recent, some older)
- [ ] Various channels (if multi-channel)

**Why:** Makes dashboard look more realistic and populated

#### Sample Leads
- [ ] Create 3-5 sample leads
- [ ] Different statuses (new, contacted, qualified)
- [ ] Various channels

**Why:** Shows lead tracking functionality

---

### Environment Setup

#### Browser
- [ ] Chrome/Firefox updated
- [ ] Browser console closed (clean presentation)
- [ ] Bookmarks ready (dashboard, Telegram)
- [ ] No distracting extensions visible

#### Screen Sharing (if remote)
- [ ] Screen sharing software tested
- [ ] Audio clear
- [ ] Screen resolution appropriate
- [ ] Backup plan if connection fails

#### Local Environment
- [ ] Desktop clean (no personal files visible)
- [ ] Terminal/console windows minimized
- [ ] Only necessary applications open
- [ ] Notifications disabled

---

### Demo Materials

#### Script
- [ ] Demo script reviewed
- [ ] Talking points memorized
- [ ] Timing practiced
- [ ] Backup plans ready

#### Backup Materials
- [ ] Screenshots of key features
- [ ] Pre-recorded video (optional)
- [ ] Architecture diagrams (if needed)
- [ ] Product overview document

---

## 🧪 Quick Test Run (30 minutes before demo)

### Test Flow

1. **Login to Dashboard** (10 seconds)
   - [ ] Login works
   - [ ] Dashboard loads
   - [ ] No errors

2. **Send Test Message** (30 seconds)
   - [ ] Open Telegram
   - [ ] Send "Hello"
   - [ ] Bot responds correctly
   - [ ] Response time < 2 seconds

3. **Check Dashboard Update** (20 seconds)
   - [ ] Refresh dashboard
   - [ ] New conversation appears
   - [ ] Statistics updated

4. **Test Knowledge Base** (30 seconds)
   - [ ] Send "What's your pricing?"
   - [ ] Bot returns knowledge base answer
   - [ ] Answer is accurate

5. **Test Memory** (30 seconds)
   - [ ] Send "Hi again"
   - [ ] Bot recognizes returning user
   - [ ] Response is context-aware

6. **Verify Analytics** (20 seconds)
   - [ ] Check intent distribution
   - [ ] Check conversation count
   - [ ] All data accurate

**Total Test Time:** ~2 minutes

---

## 🚨 Emergency Fixes

### If Backend Crashes
```bash
# Restart backend
cd /path/to/Curie
.venv\Scripts\activate  # Windows
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### If Frontend Crashes
```bash
# Restart frontend
cd frontend
npm run dev
```

### If Database Issues
```bash
# Reinitialize database
python -c "from app.database import init_db; init_db()"
```

### If Telegram Bot Not Responding
1. Check webhook configuration
2. Verify bot token in `.env`
3. Test webhook manually
4. Use backup plan (show existing conversations)

---

## ✅ Final Pre-Demo Checklist (5 minutes before)

- [ ] All servers running
- [ ] No error logs
- [ ] Test message sent and responded to
- [ ] Dashboard shows data
- [ ] Browser tabs ready
- [ ] Screen sharing ready (if remote)
- [ ] Demo script reviewed
- [ ] Backup plans ready
- [ ] Notifications disabled
- [ ] Phone on silent

---

## 📊 Success Criteria

### Technical
- ✅ All systems operational
- ✅ Response times < 2 seconds
- ✅ No errors or crashes
- ✅ Data accuracy verified

### Presentation
- ✅ Smooth flow
- ✅ Professional appearance
- ✅ Clear communication
- ✅ Confident delivery

---

## 🎯 Post-Demo Notes

After the demo, note:
- Questions asked
- Features that generated interest
- Concerns raised
- Technical issues encountered
- Follow-up items

---

**You're ready! Good luck! 🚀**


