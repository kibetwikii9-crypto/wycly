from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.logging_config import init_logging
from app.routes import api_router
from app.services.knowledge_service import load_knowledge
from app.database import init_db
from app.models import (
    Conversation,
    User,
    Business,
    ChannelIntegration,
    Message,
    Lead,
    KnowledgeEntry,
    ConversationMemory,
    AnalyticsEvent,
    AdAsset,
)  # Import all models to register with Base

init_logging(settings.log_level)

app = FastAPI(title="Curie - Multi-Platform Messaging API", version="0.1.0")

# Add CORS middleware
# Support both local development and production (Render)
import os

cors_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Add production frontend URL from environment variable
frontend_url_env = os.getenv("FRONTEND_URL", "")
if frontend_url_env:
    cors_origins.append(frontend_url_env)

# Also add from settings if set
if settings.frontend_url:
    cors_origins.append(settings.frontend_url)

# In development (localhost), allow all origins for easier testing
# In production, FRONTEND_URL must be set explicitly
is_production = os.getenv("ENVIRONMENT", "").lower() in ["production", "prod"] or not settings.public_url.startswith("http://localhost")
if not is_production and not frontend_url_env and not settings.frontend_url:
    # Only allow all origins in local development
    cors_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    """Initialize services on application startup."""
    # Initialize database (create tables)
    try:
        init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️  Database initialization error: {e}")
    
    # Auto-create admin user if it doesn't exist
    try:
        from app.database import get_db_context
        from app.services.auth import create_user, get_user_by_email
        
        admin_email = settings.admin_email
        admin_password = settings.admin_password
        
        # Only auto-create admin if password is provided
        if admin_password:
            with get_db_context() as db:
                existing = get_user_by_email(db, admin_email)
                if not existing:
                    admin_user = create_user(
                        db,
                        email=admin_email,
                        password=admin_password,
                        full_name="Admin User",
                        role="admin"
                    )
                    print(f"✅ Admin user auto-created: {admin_email}")
                else:
                    print(f"✅ Admin user already exists: {admin_email}")
        else:
            print(f"⚠️  Admin password not set (ADMIN_PASSWORD env var). Skipping admin auto-creation.")
    except Exception as e:
        print(f"⚠️  Admin user creation error: {e}")
        # Don't fail startup if admin creation fails
    
    # Load knowledge base
    if load_knowledge("faq.json"):
        print("✅ Knowledge base loaded successfully")
    else:
        print("⚠️  Knowledge base not loaded (faq.json not found or invalid)")


