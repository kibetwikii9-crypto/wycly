"""Onboarding API routes."""
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from app.database import get_db
from app.models import OnboardingStep, OnboardingProgress, User as UserModel
from app.routes.auth import get_current_user, get_user_business_id

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/onboarding", tags=["onboarding"])


# ========== PYDANTIC MODELS ==========

class OnboardingProgressResponse(BaseModel):
    step_key: str
    title: str
    description: str
    order: int
    is_required: bool
    is_completed: bool
    completed_at: Optional[str] = None


# ========== ONBOARDING ENDPOINTS ==========

@router.get("/progress/", response_model=List[OnboardingProgressResponse])
async def get_progress(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get onboarding progress for current user."""
    business_id = get_user_business_id(current_user, db)
    
    if business_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Onboarding access requires a business account"
        )
    
    # Get all steps
    steps = db.query(OnboardingStep).order_by(OnboardingStep.order).all()
    
    # Get progress
    progress_dict = {
        p.step_key: p for p in db.query(OnboardingProgress).filter(
            OnboardingProgress.user_id == current_user.id,
            OnboardingProgress.business_id == business_id
        ).all()
    }
    
    result = []
    for step in steps:
        progress = progress_dict.get(step.step_key)
        result.append({
            "step_key": step.step_key,
            "title": step.title,
            "description": step.description,
            "order": step.order,
            "is_required": step.is_required,
            "is_completed": progress.is_completed if progress else False,
            "completed_at": progress.completed_at.isoformat() if progress and progress.completed_at else None,
        })
    
    return result


@router.post("/complete-step/{step_key}", status_code=status.HTTP_204_NO_CONTENT)
async def complete_step(
    step_key: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark an onboarding step as completed."""
    business_id = get_user_business_id(current_user, db)
    
    if business_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Onboarding access requires a business account"
        )
    
    # Verify step exists
    step = db.query(OnboardingStep).filter(OnboardingStep.step_key == step_key).first()
    if not step:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Step not found"
        )
    
    # Get or create progress
    progress = db.query(OnboardingProgress).filter(
        OnboardingProgress.user_id == current_user.id,
        OnboardingProgress.business_id == business_id,
        OnboardingProgress.step_key == step_key
    ).first()
    
    if progress:
        progress.is_completed = True
        progress.completed_at = datetime.utcnow()
    else:
        progress = OnboardingProgress(
            user_id=current_user.id,
            business_id=business_id,
            step_key=step_key,
            is_completed=True,
            completed_at=datetime.utcnow(),
        )
        db.add(progress)
    
    db.commit()
    
    return None

