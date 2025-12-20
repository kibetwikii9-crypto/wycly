# SaaS Platform Setup Guide

## 🎯 Project Overview

This is a fully functional, production-ready SaaS platform for multi-channel AI chatbot, support, and marketing automation.

**Current Status:** Phase 1 - SQLite + Rule-Based AI

---

## 📁 Project Structure

```
Curie/
├── app/                    # FastAPI Backend
│   ├── models.py          # Database models (SQLAlchemy)
│   ├── database.py        # Database configuration
│   ├── routes/            # API routes
│   │   ├── auth.py        # Authentication endpoints
│   │   ├── dashboard.py   # Dashboard API endpoints
│   │   └── telegram.py    # Telegram webhook
│   ├── services/          # Business logic
│   │   ├── ai_brain.py    # Rule-based AI engine
│   │   ├── auth.py        # Authentication service
│   │   ├── conversation_service.py
│   │   ├── knowledge_service.py
│   │   └── memory.py
│   └── schemas.py         # Pydantic models
│
├── frontend/               # Next.js Frontend
│   ├── app/               # Next.js App Router
│   │   ├── dashboard/     # Dashboard pages
│   │   ├── login/         # Login page
│   │   └── layout.tsx     # Root layout
│   ├── components/        # React components
│   ├── lib/               # Utilities & API client
│   └── package.json
│
└── curie.db               # SQLite database
```

---

## 🗄️ Database Models

### Core Tables:

1. **users** - Authentication & access control
2. **businesses** - Multi-tenant workspaces
3. **channel_integrations** - Platform connections
4. **conversations** - User-bot interactions
5. **messages** - Individual messages
6. **leads** - Lead tracking
7. **knowledge_entries** - FAQ/knowledge base
8. **conversation_memory** - User context
9. **analytics_events** - System events
10. **ad_assets** - Ad & video assets

---

## 🚀 Getting Started

### Backend Setup:

```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start server
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend Setup:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

---

## 🔐 Authentication

### Create First User:

The system uses JWT authentication. To create your first user:

1. **Via API:**
   ```bash
   curl -X POST http://localhost:8000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{
       "email": "admin@example.com",
       "password": "yourpassword",
       "full_name": "Admin User",
       "role": "admin"
     }'
   ```

2. **Or add directly to database** (for initial setup)

### Roles:
- `admin` - Full access
- `business_owner` - Business management
- `agent` - Support agent access

---

## 📊 Dashboard Modules

### 1. Overview (`/dashboard`)
- Total conversations
- Active chats
- Leads captured
- Most common intents
- Channel distribution

### 2. Conversations (`/dashboard/conversations`)
- Unified inbox
- Filter by channel/intent
- Pagination
- Full conversation history

### 3. Knowledge Base (`/dashboard/knowledge`)
- FAQ management
- Document upload
- Intent linking

### 4. AI Rules (`/dashboard/ai-rules`)
- Intent rule editor
- Response rules
- Context conditions

### 5. Analytics (`/dashboard/analytics`)
- Intent frequency charts
- Timeline analytics
- Channel performance

### 6. Ad Studio (`/dashboard/ads`)
- Ad copy creation
- Video creation workflow
- Campaign management

### 7. Settings (`/dashboard/settings`)
- Channel integrations
- User management
- Security settings

---

## 🔌 API Endpoints

### Authentication:
- `POST /api/auth/login` - Login
- `POST /api/auth/register` - Register
- `GET /api/auth/me` - Get current user

### Dashboard:
- `GET /api/dashboard/overview` - Overview stats
- `GET /api/dashboard/conversations` - List conversations
- `GET /api/dashboard/analytics/intents` - Intent analytics
- `GET /api/dashboard/analytics/channels` - Channel analytics
- `GET /api/dashboard/analytics/timeline` - Timeline data
- `GET /api/dashboard/leads` - List leads

---

## 🧠 AI Engine

### Current: Rule-Based
- **Location:** `app/services/ai_brain.py`
- **Type:** Keyword-based intent detection
- **No Paid APIs:** All local logic
- **Components:**
  - Intent detection
  - Knowledge base (RAG-lite)
  - Conversation memory
  - Context-aware responses

### Future: LLM Integration
- Can be swapped by updating `app/services/ai.py`
- Same interface, different implementation
- No changes to dashboard or database

---

## 🎨 Frontend Features

- ✅ Next.js 14 with App Router
- ✅ Tailwind CSS styling
- ✅ Dark mode support
- ✅ Responsive design
- ✅ React Query for data fetching
- ✅ JWT authentication
- ✅ Protected routes

---

## 📝 Next Steps

1. **Create first user** (via API or database)
2. **Start backend server**
3. **Start frontend server**
4. **Login at** `http://localhost:3000/login`
5. **Access dashboard at** `http://localhost:3000/dashboard`

---

## 🔧 Configuration

### Backend:
- Database: SQLite (`curie.db`)
- Port: `8000`
- API docs: `http://localhost:8000/docs`

### Frontend:
- Port: `3000`
- API proxy: Configured in `next.config.js`

---

## ✅ Status

**Completed:**
- ✅ Database models
- ✅ Authentication system
- ✅ Dashboard API endpoints
- ✅ Frontend structure
- ✅ Login page
- ✅ Overview dashboard
- ✅ Conversations page
- ✅ Analytics page
- ✅ Knowledge base page

**In Progress:**
- 🔄 Remaining dashboard modules
- 🔄 WebSocket real-time updates
- 🔄 Mobile optimization

The platform foundation is ready! Start both servers and access the dashboard.



