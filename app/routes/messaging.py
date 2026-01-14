"""Internal Messaging API routes."""
import logging
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from pydantic import BaseModel

from app.database import get_db
from app.models import Channel, ChannelMember, InternalMessage, User as UserModel
from app.routes.auth import get_current_user, get_user_business_id

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/messaging", tags=["messaging"])


# ========== PYDANTIC MODELS ==========

class ChannelCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_private: bool = False
    member_ids: Optional[List[int]] = []


class ChannelResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_private: bool
    created_by_user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    channel_id: Optional[int] = None
    recipient_id: Optional[int] = None
    message: str


class MessageResponse(BaseModel):
    id: int
    channel_id: Optional[int]
    sender_id: int
    recipient_id: Optional[int]
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ========== CHANNEL ENDPOINTS ==========

@router.post("/channels/", response_model=ChannelResponse, status_code=status.HTTP_201_CREATED)
async def create_channel(
    channel_data: ChannelCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a messaging channel."""
    business_id = get_user_business_id(current_user)
    channel = Channel(
        business_id=business_id,
        name=channel_data.name,
        description=channel_data.description,
        is_private=channel_data.is_private,
        created_by_user_id=current_user.id,
    )
    db.add(channel)
    db.flush()
    
    # Add creator as member
    member = ChannelMember(channel_id=channel.id, user_id=current_user.id)
    db.add(member)
    
    # Add other members
    for user_id in channel_data.member_ids or []:
        member = ChannelMember(channel_id=channel.id, user_id=user_id)
        db.add(member)
    
    db.commit()
    db.refresh(channel)
    return channel


@router.get("/channels/", response_model=List[ChannelResponse])
async def get_channels(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all channels user is a member of."""
    business_id = get_user_business_id(current_user)
    
    # Get channels where user is a member or channel is public
    channels = db.query(Channel).join(ChannelMember).filter(
        and_(
            Channel.business_id == business_id,
            or_(
                ChannelMember.user_id == current_user.id,
                Channel.is_private == False
            )
        )
    ).distinct().all()
    
    return channels


# ========== MESSAGE ENDPOINTS ==========

@router.post("/messages/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    message_data: MessageCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Send a message."""
    business_id = get_user_business_id(current_user)
    
    # Verify channel or recipient
    if message_data.channel_id:
        channel = db.query(Channel).filter(
            and_(Channel.id == message_data.channel_id, Channel.business_id == business_id)
        ).first()
        if not channel:
            raise HTTPException(status_code=404, detail="Channel not found")
        
        # Check if user is member
        member = db.query(ChannelMember).filter(
            and_(
                ChannelMember.channel_id == message_data.channel_id,
                ChannelMember.user_id == current_user.id
            )
        ).first()
        if not member and channel.is_private:
            raise HTTPException(status_code=403, detail="Not a member of this channel")
    
    message = InternalMessage(
        business_id=business_id,
        channel_id=message_data.channel_id,
        sender_id=current_user.id,
        recipient_id=message_data.recipient_id,
        message=message_data.message,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


@router.get("/messages/", response_model=List[MessageResponse])
async def get_messages(
    channel_id: Optional[int] = None,
    recipient_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get messages."""
    business_id = get_user_business_id(current_user)
    query = db.query(InternalMessage).filter(InternalMessage.business_id == business_id)
    
    if channel_id:
        query = query.filter(InternalMessage.channel_id == channel_id)
    elif recipient_id:
        # Direct messages: sent to or from current user
        query = query.filter(
            or_(
                and_(
                    InternalMessage.recipient_id == current_user.id,
                    InternalMessage.sender_id == recipient_id
                ),
                and_(
                    InternalMessage.sender_id == current_user.id,
                    InternalMessage.recipient_id == recipient_id
                )
            )
        )
    else:
        # Get all messages for user (channels they're in + direct messages)
        query = query.filter(
            or_(
                InternalMessage.recipient_id == current_user.id,
                InternalMessage.sender_id == current_user.id
            )
        )
    
    messages = query.order_by(InternalMessage.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    return messages


@router.patch("/messages/{message_id}/read")
async def mark_message_read(
    message_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark a message as read."""
    message = db.query(InternalMessage).filter(
        and_(
            InternalMessage.id == message_id,
            InternalMessage.recipient_id == current_user.id
        )
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.is_read = True
    message.read_at = datetime.utcnow()
    db.commit()
    return {"message": "Message marked as read"}


@router.get("/unread-count")
async def get_unread_count(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get unread message count."""
    count = db.query(InternalMessage).filter(
        and_(
            InternalMessage.recipient_id == current_user.id,
            InternalMessage.is_read == False
        )
    ).count()
    
    return {"unread_count": count}


