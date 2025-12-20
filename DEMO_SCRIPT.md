# 5-Minute Demo Script - Curie SaaS Platform

## 🎯 Demo Objective

Showcase a production-ready, AI-powered multi-channel chatbot platform with real-time analytics and intelligent conversation management.

**Target Audience:** Potential clients, investors, stakeholders  
**Duration:** 5 minutes  
**Focus:** Core features working, future roadmap

---

## 📋 Pre-Demo Checklist

### ✅ System Readiness

- [ ] Backend server running (`python -m uvicorn app.main:app --reload`)
- [ ] Frontend server running (`npm run dev` in frontend/)
- [ ] Telegram bot connected and webhook configured
- [ ] Database initialized with sample data (optional)
- [ ] Knowledge base loaded (`faq.json` exists)
- [ ] Admin user created (email: admin@curie.com, password: admin123)
- [ ] Browser tabs ready:
  - [ ] Telegram web/desktop app open
  - [ ] Dashboard open (http://localhost:3000)
  - [ ] Dashboard logged in as admin

### ✅ Test Accounts

- [ ] Telegram test account ready (or use your own)
- [ ] Test messages prepared (see script below)

### ✅ Demo Environment

- [ ] Screen sharing ready (if remote)
- [ ] Audio clear
- [ ] Backup plan if something fails (screenshots/video)
- [ ] Browser console closed (clean presentation)

---

## 🎬 Demo Script (5 Minutes)

### **Segment 1: Introduction & Overview** (30 seconds)

**Action:**
- Open dashboard (http://localhost:3000)
- Show login page briefly, then log in
- Navigate to Overview dashboard

**Talking Points:**
> "Today I'm excited to show you Curie - our AI-powered chatbot platform that helps businesses engage with customers across multiple messaging channels. Let me start by showing you the dashboard where everything is managed in real-time."

**What to Show:**
- Clean, professional dashboard interface
- Overview statistics (conversations, active chats, leads)
- Real-time data visualization

**Success Criteria:**
- ✅ Dashboard loads quickly
- ✅ Data displays correctly
- ✅ Interface looks professional

---

### **Segment 2: Live Chat Demonstration** (1 minute 30 seconds)

**Action:**
- Switch to Telegram (or show side-by-side)
- Send first message: **"Hello"**

**Talking Points:**
> "Let me show you how the bot interacts with a real customer. I'll send a greeting message through Telegram."

**Expected Bot Response:**
> "Hello! 👋 Welcome! I'm here to help you. How can I assist you today?"

**What to Check:**
- ✅ Bot responds within 1-2 seconds
- ✅ Response is friendly and professional
- ✅ Message appears in Telegram

**Action:**
- Send second message: **"What's your pricing?"**

**Talking Points:**
> "Now I'm asking about pricing. Notice how the bot recognizes this as a pricing question and provides a detailed answer from our knowledge base."

**Expected Bot Response:**
> "We offer flexible pricing plans to suit different needs. Our basic plan starts at $9/month, our professional plan is $29/month, and our enterprise plan is $99/month..."

**What to Check:**
- ✅ Bot responds with knowledge base answer
- ✅ Answer is accurate and helpful
- ✅ Response time is fast

**Action:**
- Send third message: **"Tell me more about the professional plan"**

**Talking Points:**
> "The bot remembers our conversation context. Even though I didn't say 'pricing' again, it knows we're still discussing pricing and provides a contextual response."

**Expected Bot Response:**
> Context-aware response acknowledging previous pricing discussion

**What to Check:**
- ✅ Bot remembers conversation context
- ✅ Response is contextually relevant
- ✅ Memory is working correctly

---

### **Segment 3: AI Memory Demonstration** (1 minute)

**Action:**
- Send message: **"Hi again"**

**Talking Points:**
> "This is where the AI memory really shines. I'm greeting the bot again, but notice how it recognizes I'm a returning user and adjusts its response accordingly."

**Expected Bot Response:**
> "Hello again! 👋 How can I help you today?" (or similar context-aware greeting)

**What to Check:**
- ✅ Bot recognizes returning user
- ✅ Response is personalized
- ✅ Memory persists across messages

**Action:**
- Send message: **"What features do you have?"**

**Talking Points:**
> "The bot can answer questions from our knowledge base. This question about features will trigger a knowledge base lookup, and you'll see a comprehensive answer."

**Expected Bot Response:**
> Knowledge base answer about features

**What to Check:**
- ✅ Knowledge base lookup works
- ✅ Answer is comprehensive
- ✅ Response is accurate

---

### **Segment 4: Real-Time Dashboard Updates** (1 minute)

**Action:**
- Switch back to dashboard
- Navigate to Conversations page
- Show the conversation we just had

**Talking Points:**
> "Now let's see how this conversation appears in real-time on the dashboard. Every interaction is automatically captured, analyzed, and displayed here."

**What to Show:**
- ✅ Conversation list showing recent messages
- ✅ User message and bot reply pairs
- ✅ Intent detection (greeting, pricing, etc.)
- ✅ Timestamps
- ✅ Channel information (Telegram)

**Action:**
- Navigate to Analytics/Overview
- Show updated statistics

**Talking Points:**
> "The dashboard updates in real-time. You can see our conversation count increased, the intent distribution shows what customers are asking about, and we can track engagement across different channels."

**What to Show:**
- ✅ Updated conversation count
- ✅ Intent distribution chart
- ✅ Channel statistics
- ✅ Timeline analytics

**Success Criteria:**
- ✅ Dashboard shows new conversation
- ✅ Statistics updated correctly
- ✅ Data is accurate and timely

---

### **Segment 5: Future Features & Roadmap** (1 minute)

**Action:**
- Navigate to different dashboard sections
- Show "Coming Soon" indicators or mention features

**Talking Points:**
> "What you're seeing today is our Phase 1 platform - fully functional and production-ready. But we're just getting started. Here's what's coming next:"

**Future Features to Highlight:**

1. **Multi-Channel Expansion:**
   > "We currently support Telegram, and WhatsApp and Instagram integrations are coming in Phase 2. This will give you a unified inbox across all major messaging platforms."

2. **Advanced AI:**
   > "Our current rule-based AI is smart and efficient. In Phase 2, we'll integrate advanced LLM models like GPT-4 for even more natural conversations and better understanding of customer intent."

3. **Advanced Analytics:**
   > "We're building advanced analytics including sentiment analysis, conversation quality scoring, and predictive insights to help you understand your customers better."

4. **Custom Integrations:**
   > "Phase 2 will include custom integrations with CRM systems, marketing automation tools, and custom webhooks for seamless workflow integration."

5. **Team Collaboration:**
   > "We're adding team features like agent handoff, conversation assignment, and collaborative tools for larger support teams."

**What to Show:**
- ✅ Current working features
- ✅ Professional interface
- ✅ Clear roadmap vision

**Success Criteria:**
- ✅ Demo ends on high note
- ✅ Future vision is clear
- ✅ Platform feels complete but evolving

---

## 🎯 Key Talking Points Summary

### Opening (30 sec)
- Professional dashboard
- Real-time analytics
- Multi-channel support

### Live Demo (1.5 min)
- Fast, intelligent responses
- Knowledge base integration
- Context-aware conversations

### Memory Demo (1 min)
- Returning user recognition
- Conversation continuity
- Personalized responses

### Dashboard (1 min)
- Real-time updates
- Comprehensive analytics
- Actionable insights

### Future (1 min)
- Clear roadmap
- Exciting enhancements
- Production-ready foundation

---

## 📊 Success Metrics

### During Demo:
- ✅ No errors or crashes
- ✅ Fast response times (< 2 seconds)
- ✅ Smooth transitions between screens
- ✅ Professional presentation

### Post-Demo:
- ✅ Questions answered confidently
- ✅ Clear value proposition communicated
- ✅ Technical capabilities demonstrated
- ✅ Future vision understood

---

## 🚨 Backup Plans

### If Telegram Bot Doesn't Respond:
**Plan A:** Use pre-recorded screenshots/video  
**Plan B:** Show dashboard with existing conversations  
**Talking Point:** "Let me show you how conversations appear in the dashboard..."

### If Dashboard Doesn't Load:
**Plan A:** Show API documentation (FastAPI /docs)  
**Plan B:** Show code structure and architecture  
**Talking Point:** "The platform is built on modern, scalable architecture..."

### If Knowledge Base Doesn't Work:
**Plan A:** Show intent-based responses  
**Talking Point:** "The bot uses intelligent intent detection to understand customer needs..."

### If Memory Doesn't Work:
**Plan A:** Show different intents (greeting, pricing, help)  
**Talking Point:** "The bot can handle multiple conversation types..."

---

## 📝 Post-Demo Checklist

- [ ] Thank audience for their time
- [ ] Ask for questions
- [ ] Provide contact information
- [ ] Offer follow-up materials
- [ ] Note any questions/concerns for follow-up

---

## 💡 Pro Tips

1. **Practice the flow** - Run through the demo 2-3 times before the actual presentation
2. **Have backup data** - Pre-populate database with sample conversations if needed
3. **Keep it simple** - Don't try to show everything, focus on key features
4. **Be confident** - You built this, show it with pride!
5. **Handle questions gracefully** - If you don't know something, note it for follow-up
6. **Time management** - Keep to 5 minutes, leave time for questions
7. **Show enthusiasm** - Your excitement is contagious!

---

## 🎬 Demo Flow Diagram

```
[0:00] Introduction & Dashboard Overview
   ↓
[0:30] Switch to Telegram
   ↓
[0:45] Send "Hello" → Show greeting response
   ↓
[1:15] Send "What's your pricing?" → Show knowledge base answer
   ↓
[1:45] Send "Tell me more" → Show memory/context
   ↓
[2:15] Send "Hi again" → Show returning user recognition
   ↓
[2:45] Send "What features?" → Show knowledge base
   ↓
[3:15] Switch back to Dashboard
   ↓
[3:30] Show Conversations page with new conversation
   ↓
[4:00] Show Analytics/Overview with updated stats
   ↓
[4:30] Highlight Future Features
   ↓
[5:00] Closing & Questions
```

---

## 📧 Follow-Up Materials

After the demo, be ready to provide:
- Product overview document
- Technical architecture summary
- Pricing information
- Roadmap timeline
- Contact information for questions

---

**Good luck with your demo! 🚀**


