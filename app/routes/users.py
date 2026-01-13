"""Users and Roles API routes."""
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.database import get_db
from app.models import User as UserModel, Role, Permission, RolePermission, UserRole, Business
from app.routes.auth import get_current_user, get_user_business_id

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/users", tags=["users"])


# ========== PYDANTIC MODELS ==========

class UserCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: Optional[str] = "agent"
    business_id: Optional[int] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    role: str
    business_id: Optional[int]
    is_active: bool
    created_at: str

    class Config:
        from_attributes = True


class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    permission_ids: Optional[List[int]] = []


class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_system: bool
    permissions: List[dict]

    class Config:
        from_attributes = True


class PermissionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category: Optional[str]

    class Config:
        from_attributes = True


# ========== USER ENDPOINTS ==========

@router.get("/", response_model=List[UserResponse])
async def get_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    role: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get list of users in the business."""
    business_id = get_user_business_id(current_user, db)
    
    if business_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User management requires a business account"
        )
    
    # Check permissions (only admin and business_owner can view users)
    if current_user.role not in ["admin", "business_owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    query = db.query(UserModel).filter(UserModel.business_id == business_id)
    
    if search:
        query = query.filter(
            (UserModel.email.ilike(f"%{search}%")) |
            (UserModel.full_name.ilike(f"%{search}%"))
        )
    
    if role:
        query = query.filter(UserModel.role == role)
    
    offset = (page - 1) * limit
    users = query.order_by(UserModel.created_at.desc()).offset(offset).limit(limit).all()
    
    return users


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new user."""
    business_id = get_user_business_id(current_user, db)
    
    if business_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User creation requires a business account"
        )
    
    # Check permissions
    if current_user.role not in ["admin", "business_owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    # Check if user already exists
    existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    from app.services.auth import create_user as create_user_service
    user = create_user_service(
        db,
        email=user_data.email,
        password="temp_password_123",  # Should send invitation email with password reset
        full_name=user_data.full_name,
        role=user_data.role or "agent",
        business_id=business_id,
    )
    
    return user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get user by ID."""
    business_id = get_user_business_id(current_user, db)
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check permissions
    if business_id and user.business_id != business_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    if current_user.role not in ["admin", "business_owner"] and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update user."""
    business_id = get_user_business_id(current_user, db)
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check permissions
    if business_id and user.business_id != business_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    if current_user.role not in ["admin", "business_owner"] and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    # Update fields
    if user_data.full_name is not None:
        user.full_name = user_data.full_name
    if user_data.role is not None and current_user.role in ["admin", "business_owner"]:
        user.role = user_data.role
    if user_data.is_active is not None and current_user.role in ["admin", "business_owner"]:
        user.is_active = user_data.is_active
    
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete user."""
    business_id = get_user_business_id(current_user, db)
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check permissions
    if business_id and user.business_id != business_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    if current_user.role not in ["admin", "business_owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    db.delete(user)
    db.commit()
    return None


# ========== ROLE ENDPOINTS ==========

@router.get("/roles/", response_model=List[RoleResponse])
async def get_roles(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all roles."""
    business_id = get_user_business_id(current_user, db)
    
    query = db.query(Role).filter(
        (Role.business_id == business_id) | (Role.is_system == True)
    )
    roles = query.all()
    
    result = []
    for role in roles:
        permissions = db.query(Permission).join(RolePermission).filter(
            RolePermission.role_id == role.id
        ).all()
        result.append({
            "id": role.id,
            "name": role.name,
            "description": role.description,
            "is_system": role.is_system,
            "permissions": [{"id": p.id, "name": p.name} for p in permissions]
        })
    
    return result


@router.get("/permissions/", response_model=List[PermissionResponse])
async def get_permissions(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all permissions."""
    permissions = db.query(Permission).all()
    return permissions

