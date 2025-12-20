"""Dashboard API routes for analytics and data retrieval."""
import logging
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Conversation, Lead, AnalyticsEvent, ChannelIntegration, User as UserModel
from app.routes.auth import get_current_user

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/overview")
async def get_overview(
    days: int = Query(7, ge=1, le=365),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get dashboard overview statistics."""
    start_date = datetime.utcnow() - timedelta(days=days)

    # Total conversations
    total_conversations = db.query(func.count(Conversation.id)).filter(
        Conversation.created_at >= start_date
    ).scalar() or 0

    # Active chats (conversations in last 24 hours)
    active_chats = db.query(func.count(Conversation.id)).filter(
        Conversation.created_at >= datetime.utcnow() - timedelta(hours=24)
    ).scalar() or 0

    # Leads captured
    total_leads = db.query(func.count(Lead.id)).filter(
        Lead.created_at >= start_date
    ).scalar() or 0

    # Most common intents
    intent_counts = (
        db.query(Conversation.intent, func.count(Conversation.id).label("count"))
        .filter(Conversation.created_at >= start_date)
        .group_by(Conversation.intent)
        .order_by(func.count(Conversation.id).desc())
        .limit(5)
        .all()
    )
    most_common_intents = [{"intent": intent, "count": count} for intent, count in intent_counts]

    # Channel distribution
    channel_counts = (
        db.query(Conversation.channel, func.count(Conversation.id).label("count"))
        .filter(Conversation.created_at >= start_date)
        .group_by(Conversation.channel)
        .all()
    )
    channel_distribution = [{"channel": channel, "count": count} for channel, count in channel_counts]

    return {
        "total_conversations": total_conversations,
        "active_chats": active_chats,
        "leads_captured": total_leads,
        "most_common_intents": most_common_intents,
        "channel_distribution": channel_distribution,
        "period_days": days,
    }


@router.get("/conversations")
async def get_conversations(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    channel: Optional[str] = None,
    intent: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get paginated conversations list."""
    query = db.query(Conversation)

    # Apply filters
    if channel:
        query = query.filter(Conversation.channel == channel)
    if intent:
        query = query.filter(Conversation.intent == intent)

    # Get total count
    total = query.count()

    # Apply pagination
    offset = (page - 1) * limit
    conversations = query.order_by(Conversation.created_at.desc()).offset(offset).limit(limit).all()

    return {
        "conversations": [
            {
                "id": conv.id,
                "user_id": conv.user_id,
                "channel": conv.channel,
                "user_message": conv.user_message,
                "bot_reply": conv.bot_reply,
                "intent": conv.intent,
                "created_at": conv.created_at.isoformat(),
            }
            for conv in conversations
        ],
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
    }


@router.get("/analytics/intents")
async def get_intent_analytics(
    days: int = Query(30, ge=1, le=365),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get intent analytics over time."""
    start_date = datetime.utcnow() - timedelta(days=days)

    # Intent frequency
    intent_data = (
        db.query(Conversation.intent, func.count(Conversation.id).label("count"))
        .filter(Conversation.created_at >= start_date)
        .group_by(Conversation.intent)
        .order_by(func.count(Conversation.id).desc())
        .all()
    )

    return {
        "intents": [{"intent": intent, "count": count} for intent, count in intent_data],
        "period_days": days,
    }


@router.get("/analytics/channels")
async def get_channel_analytics(
    days: int = Query(30, ge=1, le=365),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get channel performance analytics."""
    start_date = datetime.utcnow() - timedelta(days=days)

    channel_data = (
        db.query(
            Conversation.channel,
            func.count(Conversation.id).label("total"),
            func.count(func.distinct(Conversation.user_id)).label("unique_users"),
        )
        .filter(Conversation.created_at >= start_date)
        .group_by(Conversation.channel)
        .all()
    )

    return {
        "channels": [
            {"channel": channel, "total_conversations": total, "unique_users": unique_users}
            for channel, total, unique_users in channel_data
        ],
        "period_days": days,
    }


@router.get("/analytics/timeline")
async def get_timeline_analytics(
    days: int = Query(7, ge=1, le=90),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get conversation timeline data."""
    start_date = datetime.utcnow() - timedelta(days=days)

    # Group by day
    timeline_data = (
        db.query(
            func.date(Conversation.created_at).label("date"),
            func.count(Conversation.id).label("count"),
        )
        .filter(Conversation.created_at >= start_date)
        .group_by(func.date(Conversation.created_at))
        .order_by(func.date(Conversation.created_at))
        .all()
    )

    return {
        "timeline": [{"date": str(date), "count": count} for date, count in timeline_data],
        "period_days": days,
    }


@router.get("/leads")
async def get_leads(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get paginated leads list."""
    query = db.query(Lead)

    if status:
        query = query.filter(Lead.status == status)

    total = query.count()
    offset = (page - 1) * limit
    leads = query.order_by(Lead.created_at.desc()).offset(offset).limit(limit).all()

    return {
        "leads": [
            {
                "id": lead.id,
                "user_id": lead.user_id,
                "channel": lead.channel,
                "name": lead.name,
                "email": lead.email,
                "phone": lead.phone,
                "status": lead.status,
                "source_intent": lead.source_intent,
                "created_at": lead.created_at.isoformat(),
            }
            for lead in leads
        ],
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
    }

