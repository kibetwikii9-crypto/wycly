"""CRM API routes - Contacts, Interactions, Pipeline."""
import logging
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from pydantic import BaseModel

from app.database import get_db
from app.models import Contact, Interaction, PipelineStage, PipelineOpportunity, User as UserModel
from app.routes.auth import get_current_user, get_user_business_id

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/crm", tags=["crm"])


# ========== PYDANTIC MODELS ==========

class ContactCreate(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    tags: Optional[List[str]] = []
    notes: Optional[str] = None
    source: Optional[str] = None
    status: str = "lead"


class ContactResponse(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    company: Optional[str]
    job_title: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class InteractionCreate(BaseModel):
    contact_id: int
    type: str
    subject: Optional[str] = None
    description: Optional[str] = None
    interaction_date: Optional[datetime] = None


class InteractionResponse(BaseModel):
    id: int
    contact_id: int
    user_id: Optional[int]
    type: str
    subject: Optional[str]
    description: Optional[str]
    interaction_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class PipelineStageCreate(BaseModel):
    name: str
    order: int = 0
    color: Optional[str] = None
    is_default: bool = False


class PipelineStageResponse(BaseModel):
    id: int
    name: str
    order: int
    color: Optional[str]
    is_default: bool

    class Config:
        from_attributes = True


class PipelineOpportunityCreate(BaseModel):
    contact_id: int
    stage_id: int
    title: str
    value: Optional[float] = None
    currency: str = "USD"
    probability: int = 0
    expected_close_date: Optional[datetime] = None
    assigned_to_user_id: Optional[int] = None
    notes: Optional[str] = None


class PipelineOpportunityResponse(BaseModel):
    id: int
    contact_id: int
    stage_id: int
    title: str
    value: Optional[float]
    currency: str
    probability: int
    expected_close_date: Optional[datetime]
    assigned_to_user_id: Optional[int]
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ========== CONTACT ENDPOINTS ==========

@router.post("/contacts/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact_data: ContactCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new contact."""
    business_id = get_user_business_id(current_user)
    contact = Contact(
        business_id=business_id,
        first_name=contact_data.first_name,
        last_name=contact_data.last_name,
        email=contact_data.email,
        phone=contact_data.phone,
        company=contact_data.company,
        job_title=contact_data.job_title,
        address=contact_data.address,
        city=contact_data.city,
        country=contact_data.country,
        tags=str(contact_data.tags) if contact_data.tags else None,
        notes=contact_data.notes,
        source=contact_data.source,
        status=contact_data.status,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


@router.get("/contacts/", response_model=List[ContactResponse])
async def get_contacts(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = None,
    search: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all contacts."""
    business_id = get_user_business_id(current_user)
    query = db.query(Contact).filter(Contact.business_id == business_id)
    
    if status_filter:
        query = query.filter(Contact.status == status_filter)
    if search:
        query = query.filter(
            (Contact.first_name.ilike(f"%{search}%")) |
            (Contact.last_name.ilike(f"%{search}%")) |
            (Contact.email.ilike(f"%{search}%")) |
            (Contact.company.ilike(f"%{search}%"))
        )
    
    contacts = query.order_by(Contact.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    return contacts


@router.get("/contacts/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific contact."""
    business_id = get_user_business_id(current_user)
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.business_id == business_id)
    ).first()
    
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return contact


# ========== INTERACTION ENDPOINTS ==========

@router.post("/interactions/", response_model=InteractionResponse, status_code=status.HTTP_201_CREATED)
async def create_interaction(
    interaction_data: InteractionCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new interaction."""
    business_id = get_user_business_id(current_user)
    
    # Verify contact belongs to business
    contact = db.query(Contact).filter(
        and_(Contact.id == interaction_data.contact_id, Contact.business_id == business_id)
    ).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    interaction = Interaction(
        business_id=business_id,
        contact_id=interaction_data.contact_id,
        user_id=current_user.id,
        type=interaction_data.type,
        subject=interaction_data.subject,
        description=interaction_data.description,
        interaction_date=interaction_data.interaction_date or datetime.utcnow(),
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


@router.get("/contacts/{contact_id}/interactions", response_model=List[InteractionResponse])
async def get_contact_interactions(
    contact_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all interactions for a contact."""
    business_id = get_user_business_id(current_user)
    interactions = db.query(Interaction).filter(
        and_(
            Interaction.contact_id == contact_id,
            Interaction.business_id == business_id
        )
    ).order_by(Interaction.interaction_date.desc()).all()
    return interactions


# ========== PIPELINE ENDPOINTS ==========

@router.post("/pipeline/stages/", response_model=PipelineStageResponse, status_code=status.HTTP_201_CREATED)
async def create_pipeline_stage(
    stage_data: PipelineStageCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a pipeline stage."""
    business_id = get_user_business_id(current_user)
    
    # If this is default, unset other defaults
    if stage_data.is_default:
        db.query(PipelineStage).filter(
            and_(PipelineStage.business_id == business_id, PipelineStage.is_default == True)
        ).update({"is_default": False})
    
    stage = PipelineStage(
        business_id=business_id,
        name=stage_data.name,
        order=stage_data.order,
        color=stage_data.color,
        is_default=stage_data.is_default,
    )
    db.add(stage)
    db.commit()
    db.refresh(stage)
    return stage


@router.get("/pipeline/stages/", response_model=List[PipelineStageResponse])
async def get_pipeline_stages(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all pipeline stages."""
    business_id = get_user_business_id(current_user)
    stages = db.query(PipelineStage).filter(
        PipelineStage.business_id == business_id
    ).order_by(PipelineStage.order).all()
    return stages


@router.post("/pipeline/opportunities/", response_model=PipelineOpportunityResponse, status_code=status.HTTP_201_CREATED)
async def create_opportunity(
    opportunity_data: PipelineOpportunityCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a pipeline opportunity."""
    business_id = get_user_business_id(current_user)
    
    # Verify contact and stage belong to business
    contact = db.query(Contact).filter(
        and_(Contact.id == opportunity_data.contact_id, Contact.business_id == business_id)
    ).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    stage = db.query(PipelineStage).filter(
        and_(PipelineStage.id == opportunity_data.stage_id, PipelineStage.business_id == business_id)
    ).first()
    if not stage:
        raise HTTPException(status_code=404, detail="Pipeline stage not found")
    
    opportunity = PipelineOpportunity(
        business_id=business_id,
        contact_id=opportunity_data.contact_id,
        stage_id=opportunity_data.stage_id,
        title=opportunity_data.title,
        value=opportunity_data.value,
        currency=opportunity_data.currency,
        probability=opportunity_data.probability,
        expected_close_date=opportunity_data.expected_close_date,
        assigned_to_user_id=opportunity_data.assigned_to_user_id,
        notes=opportunity_data.notes,
    )
    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)
    return opportunity


@router.get("/pipeline/opportunities/", response_model=List[PipelineOpportunityResponse])
async def get_opportunities(
    stage_id: Optional[int] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all pipeline opportunities."""
    business_id = get_user_business_id(current_user)
    query = db.query(PipelineOpportunity).filter(
        PipelineOpportunity.business_id == business_id
    )
    
    if stage_id:
        query = query.filter(PipelineOpportunity.stage_id == stage_id)
    
    opportunities = query.order_by(PipelineOpportunity.created_at.desc()).all()
    return opportunities


@router.patch("/pipeline/opportunities/{opportunity_id}/stage")
async def update_opportunity_stage(
    opportunity_id: int,
    new_stage_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update opportunity stage."""
    business_id = get_user_business_id(current_user)
    opportunity = db.query(PipelineOpportunity).filter(
        and_(
            PipelineOpportunity.id == opportunity_id,
            PipelineOpportunity.business_id == business_id
        )
    ).first()
    
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    
    # Verify new stage belongs to business
    stage = db.query(PipelineStage).filter(
        and_(PipelineStage.id == new_stage_id, PipelineStage.business_id == business_id)
    ).first()
    if not stage:
        raise HTTPException(status_code=404, detail="Pipeline stage not found")
    
    opportunity.stage_id = new_stage_id
    db.commit()
    return {"message": "Opportunity stage updated", "stage_id": new_stage_id}


