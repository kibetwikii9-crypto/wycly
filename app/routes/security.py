"""Security API routes."""
import logging
import secrets
import hashlib
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models import TwoFactorAuth, IPAllowlist, Session as SessionModel, APIKey, AuditLog, User as UserModel
from app.routes.auth import get_current_user, get_user_business_id

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/security", tags=["security"])


# ========== PYDANTIC MODELS ==========

class TwoFactorAuthSetup(BaseModel):
    secret: str
    backup_codes: List[str]


class IPAllowlistCreate(BaseModel):
    ip_address: str
    description: Optional[str] = None


class APIKeyCreate(BaseModel):
    name: str
    permissions: Optional[List[str]] = []
    expires_at: Optional[str] = None


# ========== 2FA ENDPOINTS ==========

@router.get("/2fa/status", response_model=dict)
async def get_2fa_status(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get 2FA status for current user."""
    two_fa = db.query(TwoFactorAuth).filter(TwoFactorAuth.user_id == current_user.id).first()
    
    return {
        "is_enabled": two_fa.is_enabled if two_fa else False,
        "has_backup_codes": bool(two_fa and two_fa.backup_codes) if two_fa else False,
    }


@router.post("/2fa/setup", response_model=TwoFactorAuthSetup)
async def setup_2fa(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Setup 2FA for current user."""
    import pyotp
    
    # Generate secret
    secret = pyotp.random_base32()
    
    # Generate backup codes
    backup_codes = [secrets.token_hex(4) for _ in range(10)]
    
    two_fa = db.query(TwoFactorAuth).filter(TwoFactorAuth.user_id == current_user.id).first()
    if two_fa:
        two_fa.secret = secret
        import json
        two_fa.backup_codes = json.dumps(backup_codes)
    else:
        import json
        two_fa = TwoFactorAuth(
            user_id=current_user.id,
            secret=secret,
            backup_codes=json.dumps(backup_codes),
            is_enabled=False,
        )
        db.add(two_fa)
    
    db.commit()
    
    return {
        "secret": secret,
        "backup_codes": backup_codes,
    }


@router.post("/2fa/enable", status_code=status.HTTP_204_NO_CONTENT)
async def enable_2fa(
    code: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Enable 2FA after verification."""
    import pyotp
    
    two_fa = db.query(TwoFactorAuth).filter(TwoFactorAuth.user_id == current_user.id).first()
    if not two_fa:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA not set up. Please set up first."
        )
    
    totp = pyotp.TOTP(two_fa.secret)
    if not totp.verify(code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code"
        )
    
    two_fa.is_enabled = True
    db.commit()
    
    return None


# ========== SESSION ENDPOINTS ==========

@router.get("/sessions/", response_model=List[dict])
async def get_sessions(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get active sessions for current user."""
    sessions = db.query(SessionModel).filter(
        SessionModel.user_id == current_user.id,
        SessionModel.is_active == True
    ).all()
    
    return [{
        "id": s.id,
        "ip_address": s.ip_address,
        "user_agent": s.user_agent,
        "created_at": s.created_at.isoformat(),
        "last_activity": s.last_activity.isoformat(),
    } for s in sessions]


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_session(
    session_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Revoke a session."""
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    session.is_active = False
    db.commit()
    
    return None


# ========== API KEY ENDPOINTS ==========

@router.get("/api-keys/", response_model=List[dict])
async def get_api_keys(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get API keys for business."""
    business_id = get_user_business_id(current_user, db)
    
    if business_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key access requires a business account"
        )
    
    api_keys = db.query(APIKey).filter(APIKey.business_id == business_id).all()
    
    return [{
        "id": k.id,
        "name": k.name,
        "last_used_at": k.last_used_at.isoformat() if k.last_used_at else None,
        "expires_at": k.expires_at.isoformat() if k.expires_at else None,
        "is_active": k.is_active,
        "created_at": k.created_at.isoformat(),
    } for k in api_keys]


@router.post("/api-keys/", response_model=dict)
async def create_api_key(
    key_data: APIKeyCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new API key."""
    business_id = get_user_business_id(current_user, db)
    
    if business_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key creation requires a business account"
        )
    
    # Generate API key
    api_key = secrets.token_urlsafe(32)
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    
    import json
    api_key_obj = APIKey(
        business_id=business_id,
        user_id=current_user.id,
        name=key_data.name,
        key_hash=key_hash,
        permissions=json.dumps(key_data.permissions) if key_data.permissions else None,
    )
    
    db.add(api_key_obj)
    db.commit()
    db.refresh(api_key_obj)
    
    # Return the key only once (client should save it)
    return {
        "id": api_key_obj.id,
        "name": api_key_obj.name,
        "key": api_key,  # Only returned once
        "created_at": api_key_obj.created_at.isoformat(),
    }


@router.delete("/api-keys/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_api_key(
    key_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Revoke an API key."""
    business_id = get_user_business_id(current_user, db)
    
    api_key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.business_id == business_id
    ).first()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    api_key.is_active = False
    db.commit()
    
    return None


# ========== AUDIT LOG ENDPOINTS ==========

@router.get("/audit-logs/", response_model=List[dict])
async def get_audit_logs(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    action: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get audit logs."""
    business_id = get_user_business_id(current_user, db)
    
    if business_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Audit log access requires a business account"
        )
    
    query = db.query(AuditLog).filter(AuditLog.business_id == business_id)
    
    if action:
        query = query.filter(AuditLog.action == action)
    
    offset = (page - 1) * limit
    logs = query.order_by(AuditLog.created_at.desc()).offset(offset).limit(limit).all()
    
    return [{
        "id": log.id,
        "user_id": log.user_id,
        "action": log.action,
        "resource_type": log.resource_type,
        "resource_id": log.resource_id,
        "ip_address": log.ip_address,
        "created_at": log.created_at.isoformat(),
    } for log in logs]

