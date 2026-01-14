# Localhost Setup Guide

## Quick Start

### 1. Backend Setup

Your `.env` file should have these values for localhost:
```env
PUBLIC_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
DATABASE_URL=your_supabase_postgresql_url
SECRET_KEY=your-secret-key-here
LOG_LEVEL=INFO
OPENAI_API_KEY=

# Note: BOT_TOKEN and ADMIN credentials are NOT needed.
# Users connect their own Telegram bots through the dashboard.
# Users create their own accounts through the registration endpoint.
```

### 2. Frontend Setup

Create `frontend/.env.local` file with:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Backend

In the project root directory:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Start Frontend

In a new terminal, go to frontend directory:
```bash
cd frontend
npm run dev
```

### 5. Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### 6. Create Account and Login

1. Go to http://localhost:3000
2. Click **"Sign Up"** to create your account
3. Fill in your details and register
4. You'll be automatically logged in after registration
5. You can then connect your Telegram bot through the dashboard (Integrations page)

## Troubleshooting

### CORS Errors
- Make sure `FRONTEND_URL=http://localhost:3000` is in your `.env`
- Check that backend is running on port 8000
- Check that frontend is running on port 3000

### Database Connection
- Make sure `DATABASE_URL` is set correctly
- Test connection: The backend will show errors if database is unreachable

### Port Already in Use
- Backend: Change port in uvicorn command: `--port 8001`
- Frontend: Change port: `npm run dev -- -p 3001`
- Update `NEXT_PUBLIC_API_URL` accordingly







