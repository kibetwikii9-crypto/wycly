"""Sales and Products API routes."""
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models import Product, DigitalAsset, Service, Bundle, Order, OrderItem, User as UserModel
from app.routes.auth import get_current_user, get_user_business_id

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/sales", tags=["sales"])


# ========== PYDANTIC MODELS ==========

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    currency: str = "USD"
    category: Optional[str] = None
    tags: Optional[List[str]] = []
    image_url: Optional[str] = None
    inventory_count: Optional[int] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    currency: str
    category: Optional[str]
    inventory_count: Optional[int]
    is_active: bool

    class Config:
        from_attributes = True


# ========== PRODUCT ENDPOINTS ==========

@router.get("/products/", response_model=List[ProductResponse])
async def get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get products."""
    business_id = get_user_business_id(current_user, db)
    
    if business_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Product access requires a business account"
        )
    
    query = db.query(Product).filter(Product.business_id == business_id)
    
    if category:
        query = query.filter(Product.category == category)
    
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    
    offset = (page - 1) * limit
    products = query.order_by(Product.created_at.desc()).offset(offset).limit(limit).all()
    
    return products


@router.post("/products/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a product."""
    business_id = get_user_business_id(current_user, db)
    
    if business_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Product creation requires a business account"
        )
    
    import json
    product = Product(
        business_id=business_id,
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        currency=product_data.currency,
        category=product_data.category,
        tags=json.dumps(product_data.tags) if product_data.tags else None,
        image_url=product_data.image_url,
        inventory_count=product_data.inventory_count,
    )
    
    db.add(product)
    db.commit()
    db.refresh(product)
    
    return product


@router.get("/orders/", response_model=List[dict])
async def get_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get orders."""
    business_id = get_user_business_id(current_user, db)
    
    if business_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Order access requires a business account"
        )
    
    query = db.query(Order).filter(Order.business_id == business_id)
    
    if status:
        query = query.filter(Order.status == status)
    
    offset = (page - 1) * limit
    orders = query.order_by(Order.created_at.desc()).offset(offset).limit(limit).all()
    
    return [{
        "id": o.id,
        "customer_name": o.customer_name,
        "customer_email": o.customer_email,
        "status": o.status,
        "total_amount": o.total_amount,
        "currency": o.currency,
        "payment_status": o.payment_status,
        "created_at": o.created_at.isoformat(),
    } for o in orders]

