"""Health check and root endpoints."""
from fastapi import APIRouter, status

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Telegram Bot API",
        "version": "0.1.0",
        "endpoints": {
            "health": "GET /health",
            "webhook": "POST /telegram/webhook",
            "docs": "GET /docs",
        },
    }


@router.get("/health", status_code=status.HTTP_200_OK)
async def health():
    """Health check endpoint."""
    return {"status": "ok"}




