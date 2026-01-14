# Changes Tracker - Since Brand Name Change

This document tracks all changes and fixes made since the brand name change from "Automify" to "Curie".

---

## 📋 Summary of Changes

### 1. **Brand Name Changes** (Automify → Curie)

#### Backend Files:
- **`app/main.py`**: 
  - Line 24: FastAPI title changed to `"Curie - Multi-Platform Messaging API"`

- **`app/config.py`**:
  - Line 15: `admin_email` default changed to `"admin@curie.com"`

- **`create_admin_auto.py`**:
  - Line 5: Email changed to `admin@curie.com`
  - Line 14: Email variable updated

#### Frontend Files:
- **`frontend/components/Header.tsx`**: 
  - Brand name updated from "Automify" to "Curie"

- **`frontend/components/Sidebar.tsx`**: 
  - Brand name updated from "Automify" to "Curie"

- **`frontend/lib/api.ts`**: 
  - Comments updated to reflect "Curie" naming

#### Documentation Files:
- Multiple `.md` files updated with "Curie" branding
- `ENV_EXAMPLE.txt`: Updated admin email to `admin@curie.com`

---

### 2. **CORS Configuration Fixes**

#### File: `app/main.py`

**Added:**
- Lines 35-52: `fix_render_url()` function to automatically fix incomplete Render URLs
- Lines 54-75: Enhanced CORS origin configuration with:
  - Automatic protocol detection (`http://` or `https://`)
  - Automatic `.onrender.com` suffix addition for incomplete URLs
  - Support for both `FRONTEND_URL` env var and `settings.frontend_url`
- Lines 77-93: Production fallback logic:
  - Always adds `https://automify-ai-frontend.onrender.com` in production
  - Safety fallback to allow all origins if no frontend URL detected
- Lines 97-105: Enhanced CORS middleware configuration:
  - Explicit HTTP methods: `["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]`
  - Added `expose_headers=["*"]`
  - Added debug logging for CORS origins

**Changed:**
- CORS middleware now explicitly lists methods instead of `["*"]`
- Added production detection logic
- Added multiple fallback mechanisms for CORS

---

### 3. **Database Configuration Fixes**

#### File: `app/database.py`

**Added:**
- Line 46: `"prepare_threshold": 0` in `connect_args` to disable prepared statements
  - **Purpose**: Fixes `DuplicatePreparedStatement` errors with psycopg3

---

### 4. **Database Initialization Fixes**

#### File: `app/main.py`

**Changed:**
- Lines 117-125: Enhanced error handling for database initialization:
  - Catches `DuplicatePreparedStatement` errors gracefully
  - Shows friendly message: "✅ Database tables already exist (skipping initialization)"
  - Only shows warnings for actual errors

---

### 5. **Admin User Auto-Creation Fixes** ⚠️ **HISTORICAL - REMOVED**

**Note:** Admin auto-creation has been completely removed. Users now create accounts through the registration endpoint.

#### File: `app/main.py` (Historical)

**Changed (Now Removed):**
- Lines 127-158: Simplified admin user creation (REMOVED):
  - Removed complex connection handling
  - Back to simple `get_db_context()` approach
  - Added graceful error handling for `DuplicatePreparedStatement`
  - Only attempts creation if `ADMIN_PASSWORD` is set
  - Non-blocking: startup continues even if admin creation fails

**Added (Now Removed):**
- Line 151: Warning message if `ADMIN_PASSWORD` not set (REMOVED)
- Lines 153-157: Error handling that doesn't fail startup (REMOVED)

**Current Status:** Admin auto-creation completely removed. Users register through `/api/auth/register` endpoint.

---

### 6. **Security Configuration** ⚠️ **UPDATED**

#### File: `app/config.py`

**Current Settings:**
- `secret_key`: JWT secret key (with warning if default used)
- `admin_email`: REMOVED - No longer needed
- `admin_password`: REMOVED - No longer needed

**Historical (Removed):**
- `admin_email`: Admin user email (default: `admin@curie.com`) - REMOVED
- `admin_password`: Admin user password (required for auto-creation) - REMOVED

- Lines 20-28: `__init__` method with warning for insecure default `SECRET_KEY`

---

### 7. **Render Deployment Configuration** ⚠️ **UPDATED**

#### File: `render.yaml`

**Current Configuration:**
- Service names: `automify-ai-backend` and `automify-ai-frontend`
- `SECRET_KEY` - Required (manually set)
- `DATABASE_URL` - Required (Supabase connection string)
- `BOT_TOKEN` - REMOVED - Users connect via dashboard
- `ADMIN_EMAIL` - REMOVED - Users create accounts via registration
- `ADMIN_PASSWORD` - REMOVED - Users create accounts via registration

**Historical (Removed):**
- Lines 27-30: Added `ADMIN_EMAIL` and `ADMIN_PASSWORD` to backend env vars - REMOVED
- `BOT_TOKEN` environment variable - REMOVED

**Note:** Service names were initially changed to `curie-*` but reverted to `automify-ai-*` to prevent duplicate services on Render.

---

### 8. **Documentation Files Created/Updated**

**Created:**
- `LOCALHOST_SETUP.md`: Guide for running locally
- `ENV_EXAMPLE.txt`: Environment variables documentation
- `CHANGES_TRACKER.md`: This file

**Updated:**
- Multiple deployment guides updated with `automify-ai-*` service names
- All references to admin email updated to `admin@curie.com`

---

### 9. **Files Deleted**

- Old database files have been removed

---

## 🔧 Technical Details

### CORS Fix Details:
1. **Problem**: CORS errors when frontend tried to access backend API
2. **Root Cause**: Incomplete `FRONTEND_URL` environment variable (missing `.onrender.com`)
3. **Solution**: 
   - Auto-fix incomplete Render URLs
   - Multiple fallback mechanisms
   - Explicit production frontend URL
   - Enhanced logging for debugging

### Database Fix Details:
1. **Problem**: `DuplicatePreparedStatement` errors during startup
2. **Root Cause**: psycopg3 prepared statements conflicting with connection pooling
3. **Solution**: 
   - Disable prepared statements with `prepare_threshold: 0`
   - Graceful error handling for non-critical errors

### Admin User Creation Fix Details:
1. **Problem**: Admin user creation failing with database errors
2. **Root Cause**: Complex connection handling causing prepared statement conflicts
3. **Solution**: 
   - Simplified to use standard `get_db_context()`
   - Added error handling that doesn't block startup
   - Historical: Only runs if `ADMIN_PASSWORD` is provided (REMOVED)

---

## 📝 Files Modified

### Backend:
1. `app/main.py` - CORS, database init, admin creation
2. `app/config.py` - Security settings, admin config
3. `app/database.py` - Prepared statements fix

### Frontend:
1. `frontend/components/Header.tsx` - Brand name
2. `frontend/components/Sidebar.tsx` - Brand name
3. `frontend/lib/api.ts` - Comments updated

### Configuration:
1. `render.yaml` - Environment variables, service names

### Documentation:
1. Multiple `.md` files - Branding and service name updates
2. `ENV_EXAMPLE.txt` - Environment variables guide
3. `LOCALHOST_SETUP.md` - Local development guide

---

## 🎯 Key Improvements

1. **CORS**: Robust configuration with multiple fallbacks
2. **Database**: Fixed prepared statement conflicts
3. **Admin Creation**: Simplified and more reliable
4. **Security**: Added warnings for insecure defaults
5. **Documentation**: Comprehensive guides for setup and deployment

---

## ⚠️ Important Notes

1. **Service Names**: Kept as `automify-ai-*` on Render to match existing services
2. **Database**: Uses Supabase PostgreSQL
3. **Admin User**: REMOVED - Users create accounts through registration endpoint
4. **CORS**: Production fallback ensures frontend always works even if env vars are incomplete
5. **Bot Tokens**: REMOVED from env vars - Users connect their own bots via dashboard

---

## 📅 Change Timeline

- **Brand Name Change**: Initial request
- **CORS Fixes**: Multiple iterations to handle incomplete URLs
- **Database Fixes**: Added `prepare_threshold: 0` and error handling
- **Admin Creation**: Simplified from complex connection handling
- **Documentation**: Created guides and updated references

---

*Last Updated: Current session*







