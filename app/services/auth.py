"""Authentication service for JWT tokens and password hashing.

This module provides:
- Password hashing and verification
- JWT token generation and validation
- User authentication
"""
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.models import User, Business

# JWT settings
SECRET_KEY = settings.secret_key  # Loaded from environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 days


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    try:
        # Bcrypt hashes start with $2b$ or $2a$
        # All bcrypt hashes use the same verification method
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get a user by email."""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, email: str, password: str, full_name: str = None, role: str = "agent", business_id: int = None) -> User:
    """
    Create a new user.
    
    For business_owner role, a Business will be auto-created if business_id is not provided.
    Admin users don't need a business_id.
    """
    hashed_password = get_password_hash(password)
    
    # If role is business_owner and no business_id provided, create a new Business
    if role == "business_owner" and business_id is None:
        business_name = full_name or email.split("@")[0]  # Use name or email prefix as business name
        business = Business(
            name=business_name,
            owner_id=None,  # Will be set after user is created
            settings=None,
        )
        db.add(business)
        db.flush()  # Flush to get business.id without committing
        business_id = business.id
    
    user = User(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        role=role,
        business_id=business_id if role != "admin" else None,  # Admin users don't have business_id
        is_active=True,
    )
    db.add(user)
    db.flush()  # Flush to get user.id
    
    # If we created a Business, update its owner_id
    if role == "business_owner" and business_id:
        business = db.query(Business).filter(Business.id == business_id).first()
        if business:
            business.owner_id = user.id
    
    db.commit()
    db.refresh(user)
    return user

