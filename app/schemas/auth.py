"""Authentication schemas for request/response validation."""
from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """JWT token response schema."""
    access_token: str
    token_type: str = "bearer"
    user: dict


class TokenData(BaseModel):
    """JWT token payload schema."""
    email: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None


class UserLogin(BaseModel):
    """User login request schema."""
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    """User creation request schema."""
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: str = "agent"


class UserResponse(BaseModel):
    """User response schema."""
    id: int
    email: str
    full_name: Optional[str]
    role: str
    is_active: bool

    class Config:
        from_attributes = True
