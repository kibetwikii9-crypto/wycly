"""Routes package - exports all API routers."""
from fastapi import APIRouter

from app.routes import auth, dashboard, health, telegram

# Create main router and include all sub-routers
api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(telegram.router, prefix="/telegram", tags=["telegram"])
api_router.include_router(auth.router)
api_router.include_router(dashboard.router)


