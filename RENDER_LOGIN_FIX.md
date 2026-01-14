# Fixing Login Issues on Render

## Problem
Login works on localhost but fails on Render. This is usually because the frontend can't connect to the backend API.

## Solution Steps

### 1. Check Environment Variable in Render Dashboard

1. Go to **Render Dashboard** → Click on **`wycly-frontend`** service
2. Go to **"Environment"** tab
3. Check if `NEXT_PUBLIC_API_URL` is set
4. It should be something like: `https://wycly-backend-xxxx.onrender.com`

### 2. If `NEXT_PUBLIC_API_URL` is Missing or Wrong

**Option A: Manual Setup (Recommended)**
1. In Render Dashboard → `wycly-frontend` → Environment tab
2. Add/Update environment variable:
   ```
   NEXT_PUBLIC_API_URL = https://wycly-backend-xxxx.onrender.com
   ```
   (Replace `xxxx` with your actual backend service ID)

**Option B: Use render.yaml (Auto-set)**
- The `render.yaml` should automatically set this via `fromService`
- If it's not working, use Option A above

### 3. Rebuild the Frontend

**Important**: Next.js environment variables are baked in at build time. After setting/changing `NEXT_PUBLIC_API_URL`, you MUST rebuild:

1. In Render Dashboard → `wycly-frontend` service
2. Click **"Manual Deploy"** → **"Clear build cache & deploy"**
3. Wait for deployment to complete (5-10 minutes)

### 4. Verify Backend is Running

1. Check backend service status: Should be **"Live"** (green)
2. Test backend health: Visit `https://wycly-backend-xxxx.onrender.com/health`
   - Should return: `{"status":"ok"}`
3. Test API docs: Visit `https://wycly-backend-xxxx.onrender.com/docs`
   - Should show FastAPI documentation

### 5. Check Browser Console

1. Open your frontend URL in browser
2. Open Developer Tools (F12) → Console tab
3. Look for these debug messages:
   - `API Base URL: https://wycly-backend-xxxx.onrender.com`
   - `Raw API URL from env: https://wycly-backend-xxxx.onrender.com`
4. If you see `wycly-backend` without `.onrender.com`, the env var is wrong

### 6. Verify CORS Settings

The backend should allow requests from your frontend URL. Check `app/main.py` - it should have:
```python
FRONTEND_URL = settings.frontend_url  # Set automatically by Render
```

### 7. Test Login Endpoint Directly

1. Go to: `https://wycly-backend-xxxx.onrender.com/docs`
2. Find `/api/auth/login` endpoint
3. Click "Try it out"
4. Enter credentials (from your registered account):
   - `username`: Your registered email
   - `password`: Your password
5. Click "Execute"
6. Should return a token if credentials are correct

### 8. Create Account (If Needed)

If you don't have an account yet:

1. Go to your frontend URL: `https://wycly-frontend-xxxx.onrender.com`
2. Click **"Sign Up"** to create your account
3. Fill in your details (email, password, name)
4. Click **"Sign Up"**
5. You'll be automatically logged in

## Common Issues

### Issue: "Cannot connect to server"
- **Cause**: Backend is not running or URL is wrong
- **Fix**: Check backend status, verify `NEXT_PUBLIC_API_URL` is correct, rebuild frontend

### Issue: "CORS error"
- **Cause**: Backend doesn't allow frontend origin
- **Fix**: Check `FRONTEND_URL` in backend environment variables

### Issue: "401 Unauthorized"
- **Cause**: Wrong credentials or user doesn't exist
- **Fix**: Create admin user or check credentials

### Issue: "404 Not Found"
- **Cause**: API URL is wrong or backend route doesn't exist
- **Fix**: Verify backend URL, check backend logs

## Quick Checklist

- [ ] Backend service is "Live" on Render
- [ ] Frontend service is "Live" on Render
- [ ] `NEXT_PUBLIC_API_URL` is set correctly in frontend environment
- [ ] Frontend was rebuilt after setting `NEXT_PUBLIC_API_URL`
- [ ] Backend health check works: `/health` endpoint
- [ ] Account created (sign up if needed)
- [ ] Browser console shows correct API URL
- [ ] No CORS errors in browser console

## Still Not Working?

1. Check Render service logs:
   - Backend: Dashboard → `wycly-backend` → Logs tab
   - Frontend: Dashboard → `wycly-frontend` → Logs tab

2. Check browser Network tab:
   - Open DevTools → Network tab
   - Try to login
   - Look for failed requests
   - Check the request URL and response

3. Verify all environment variables are set correctly in Render dashboard





