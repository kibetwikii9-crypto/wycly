"""Handoff and Agent Workspace API routes."""
import logging
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from pydantic import BaseModel

from app.database import get_db
from app.models import Handoff, SLA, Escalation, Conversation, User as UserModel
from app.routes.auth import get_current_user, get_user_business_id

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/handoff", tags=["handoff"])


# ========== PYDANTIC MODELS ==========

class HandoffCreate(BaseModel):
    conversation_id: int
    reason: Optional[str] = None
    priority: str = "medium"


class HandoffUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to_user_id: Optional[int] = None


class HandoffResponse(BaseModel):
    id: int
    business_id: int
    conversation_id: int
    assigned_to_user_id: Optional[int]
    status: str
    priority: str
    reason: Optional[str]
    assigned_at: Optional[str]
    resolved_at: Optional[str]
    created_at: str

    class Config:
        from_attributes = True


# ========== HANDOFF ENDPOINTS ==========

@router.get("/", response_model=List[HandoffResponse])
async def get_handoffs(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assigned_to_me: bool = Query(False),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get list of handoffs."""
    business_id = get_user_business_id(current_user, db)
    
    if business_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Handoff access requires a business account"
        )
    
    query = db.query(Handoff).filter(Handoff.business_id == business_id)
    
    if status:
        query = query.filter(Handoff.status == status)
    
    if priority:
        query = query.filter(Handoff.priority == priority)
    
    if assigned_to_me:
        query = query.filter(Handoff.assigned_to_user_id == current_user.id)
    
    offset = (page - 1) * limit
    handoffs = query.order_by(Handoff.created_at.desc()).offset(offset).limit(limit).all()
    
    return handoffs


@router.post("/", response_model=HandoffResponse, status_code=status.HTTP_201_CREATED)
async def create_handoff(
    handoff_data: HandoffCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new handoff."""
    business_id = get_user_business_id(current_user, db)
    
    if business_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Handoff creation requires a business account"
        )
    
    # Verify conversation exists and belongs to business
    conversation = db.query(Conversation).filter(
        Conversation.id == handoff_data.conversation_id,
        Conversation.business_id == business_id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Create handoff
    handoff = Handoff(
        business_id=business_id,
        conversation_id=handoff_data.conversation_id,
        status="pending",
        priority=handoff_data.priority,
        reason=handoff_data.reason,
    )
    
    db.add(handoff)
    db.commit()
    db.refresh(handoff)
    
    return handoff


@router.put("/{handoff_id}", response_model=HandoffResponse)
async def update_handoff(
    handoff_id: int,
    handoff_data: HandoffUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update handoff."""
    business_id = get_user_business_id(current_user, db)
    
    handoff = db.query(Handoff).filter(
        Handoff.id == handoff_id,
        Handoff.business_id == business_id
    ).first()
    
    if not handoff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Handoff not found"
        )
    
    if handoff_data.status:
        handoff.status = handoff_data.status
        if handoff_data.status == "resolved":
            handoff.resolved_at = datetime.utcnow()
    
    if handoff_data.priority:
        handoff.priority = handoff_data.priority
    
    if handoff_data.assigned_to_user_id is not None:
        handoff.assigned_to_user_id = handoff_data.assigned_to_user_id
        if handoff_data.assigned_to_user_id:
            handoff.assigned_at = datetime.utcnow()
    
    db.commit()
    db.refresh(handoff)
    
    return handoff


@router.get("/sla/", response_model=List[dict])
async def get_sla_metrics(
    days: int = Query(30, ge=1, le=365),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get SLA metrics."""
    business_id = get_user_business_id(current_user, db)
    
    if business_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="SLA access requires a business account"
        )
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    slas = db.query(SLA).filter(
        SLA.business_id == business_id,
        SLA.created_at >= start_date
    ).all()
    
    total = len(slas)
    response_breached = sum(1 for s in slas if s.response_time_breached)
    resolution_breached = sum(1 for s in slas if s.resolution_time_breached)
    
    avg_response_time = sum(s.actual_response_time or 0 for s in slas) / total if total > 0 else 0
    avg_resolution_time = sum(s.actual_resolution_time or 0 for s in slas) / total if total > 0 else 0
    
    return {
        "total_handoffs": total,
        "response_breach_rate": (response_breached / total * 100) if total > 0 else 0,
        "resolution_breach_rate": (resolution_breached / total * 100) if total > 0 else 0,
        "avg_response_time_minutes": round(avg_response_time, 2),
        "avg_resolution_time_minutes": round(avg_resolution_time, 2),
    }

