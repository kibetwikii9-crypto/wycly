"""Routes package - exports all API routers."""
from fastapi import APIRouter

from app.routes import auth, dashboard, health, telegram, integrations, diagnostics, users, handoff, notifications, security, sales, onboarding, finance, crm, inventory, purchasing, projects, messaging, email, automation

# Create main router and include all sub-routers
api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(telegram.router, prefix="/telegram", tags=["telegram"])
api_router.include_router(auth.router)
api_router.include_router(dashboard.router)
api_router.include_router(integrations.router, prefix="/api/integrations", tags=["integrations"])
api_router.include_router(diagnostics.router)
api_router.include_router(users.router)
api_router.include_router(handoff.router)
api_router.include_router(notifications.router)
api_router.include_router(security.router)
api_router.include_router(sales.router)
api_router.include_router(onboarding.router)
api_router.include_router(finance.router)
api_router.include_router(crm.router)
api_router.include_router(inventory.router)
api_router.include_router(purchasing.router)
api_router.include_router(projects.router)
api_router.include_router(messaging.router)
api_router.include_router(email.router)
api_router.include_router(automation.router)


