"""Email Templates API routes."""
import logging
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from pydantic import BaseModel

from app.database import get_db
from app.models import EmailTemplate, User as UserModel
from app.routes.auth import get_current_user, get_user_business_id

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/email", tags=["email"])


# ========== PYDANTIC MODELS ==========

class EmailTemplateCreate(BaseModel):
    name: str
    subject: str
    body: str
    variables: Optional[List[str]] = []
    category: Optional[str] = None


class EmailTemplateResponse(BaseModel):
    id: int
    name: str
    subject: str
    body: str
    variables: Optional[str]
    category: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ========== TEMPLATE ENDPOINTS ==========

@router.post("/templates/", response_model=EmailTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    template_data: EmailTemplateCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create an email template."""
    business_id = get_user_business_id(current_user)
    template = EmailTemplate(
        business_id=business_id,
        name=template_data.name,
        subject=template_data.subject,
        body=template_data.body,
        variables=str(template_data.variables) if template_data.variables else None,
        category=template_data.category,
    )
    db.add(template)
    db.commit()
    db.refresh(template)
    return template


@router.get("/templates/", response_model=List[EmailTemplateResponse])
async def get_templates(
    category: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all email templates."""
    business_id = get_user_business_id(current_user)
    query = db.query(EmailTemplate).filter(
        and_(EmailTemplate.business_id == business_id, EmailTemplate.is_active == True)
    )
    
    if category:
        query = query.filter(EmailTemplate.category == category)
    
    templates = query.order_by(EmailTemplate.created_at.desc()).all()
    return templates


@router.get("/templates/{template_id}", response_model=EmailTemplateResponse)
async def get_template(
    template_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific email template."""
    business_id = get_user_business_id(current_user)
    template = db.query(EmailTemplate).filter(
        and_(EmailTemplate.id == template_id, EmailTemplate.business_id == business_id)
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return template


@router.patch("/templates/{template_id}")
async def update_template(
    template_id: int,
    template_data: EmailTemplateCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update an email template."""
    business_id = get_user_business_id(current_user)
    template = db.query(EmailTemplate).filter(
        and_(EmailTemplate.id == template_id, EmailTemplate.business_id == business_id)
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    template.name = template_data.name
    template.subject = template_data.subject
    template.body = template_data.body
    template.variables = str(template_data.variables) if template_data.variables else None
    template.category = template_data.category
    
    db.commit()
    return {"message": "Template updated"}

