"""Inventory API routes."""
import logging
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from pydantic import BaseModel

from app.database import get_db
from app.models import Product, ProductVariant, InventoryTransaction, User as UserModel
from app.routes.auth import get_current_user, get_user_business_id

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/inventory", tags=["inventory"])


# ========== PYDANTIC MODELS ==========

class ProductVariantCreate(BaseModel):
    product_id: int
    name: str
    sku: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: int = 0
    low_stock_threshold: Optional[int] = None


class ProductVariantResponse(BaseModel):
    id: int
    product_id: int
    name: str
    sku: Optional[str]
    price: Optional[float]
    stock_quantity: int
    low_stock_threshold: Optional[int]
    is_active: bool

    class Config:
        from_attributes = True


class InventoryTransactionCreate(BaseModel):
    product_id: int
    variant_id: Optional[int] = None
    type: str  # stock_in, stock_out, adjustment, return
    quantity: int
    reason: Optional[str] = None
    reference_id: Optional[int] = None
    reference_type: Optional[str] = None


class InventoryTransactionResponse(BaseModel):
    id: int
    product_id: int
    variant_id: Optional[int]
    type: str
    quantity: int
    previous_quantity: Optional[int]
    new_quantity: int
    reason: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ========== VARIANT ENDPOINTS ==========

@router.post("/variants/", response_model=ProductVariantResponse, status_code=status.HTTP_201_CREATED)
async def create_variant(
    variant_data: ProductVariantCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a product variant."""
    business_id = get_user_business_id(current_user)
    
    # Verify product belongs to business
    product = db.query(Product).filter(
        and_(Product.id == variant_data.product_id, Product.business_id == business_id)
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    variant = ProductVariant(
        product_id=variant_data.product_id,
        name=variant_data.name,
        sku=variant_data.sku,
        price=variant_data.price,
        stock_quantity=variant_data.stock_quantity,
        low_stock_threshold=variant_data.low_stock_threshold,
    )
    db.add(variant)
    db.commit()
    db.refresh(variant)
    return variant


@router.get("/variants/", response_model=List[ProductVariantResponse])
async def get_variants(
    product_id: Optional[int] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all product variants."""
    business_id = get_user_business_id(current_user)
    query = db.query(ProductVariant).join(Product).filter(Product.business_id == business_id)
    
    if product_id:
        query = query.filter(ProductVariant.product_id == product_id)
    
    variants = query.all()
    return variants


# ========== INVENTORY TRANSACTION ENDPOINTS ==========

@router.post("/transactions/", response_model=InventoryTransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: InventoryTransactionCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create an inventory transaction."""
    business_id = get_user_business_id(current_user)
    
    # Verify product belongs to business
    product = db.query(Product).filter(
        and_(Product.id == transaction_data.product_id, Product.business_id == business_id)
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get current quantity
    if transaction_data.variant_id:
        variant = db.query(ProductVariant).filter(
            ProductVariant.id == transaction_data.variant_id
        ).first()
        if not variant:
            raise HTTPException(status_code=404, detail="Variant not found")
        previous_quantity = variant.stock_quantity
    else:
        previous_quantity = product.inventory_count or 0
    
    # Calculate new quantity
    if transaction_data.type in ["stock_in", "return"]:
        new_quantity = previous_quantity + transaction_data.quantity
    elif transaction_data.type in ["stock_out", "adjustment"]:
        new_quantity = previous_quantity - transaction_data.quantity
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")
    
    # Update stock
    if transaction_data.variant_id:
        variant.stock_quantity = new_quantity
    else:
        product.inventory_count = new_quantity
    
    # Create transaction record
    transaction = InventoryTransaction(
        business_id=business_id,
        product_id=transaction_data.product_id,
        variant_id=transaction_data.variant_id,
        type=transaction_data.type,
        quantity=transaction_data.quantity,
        previous_quantity=previous_quantity,
        new_quantity=new_quantity,
        reason=transaction_data.reason,
        reference_id=transaction_data.reference_id,
        reference_type=transaction_data.reference_type,
        user_id=current_user.id,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


@router.get("/transactions/", response_model=List[InventoryTransactionResponse])
async def get_transactions(
    product_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get inventory transactions."""
    business_id = get_user_business_id(current_user)
    query = db.query(InventoryTransaction).filter(
        InventoryTransaction.business_id == business_id
    )
    
    if product_id:
        query = query.filter(InventoryTransaction.product_id == product_id)
    
    transactions = query.order_by(InventoryTransaction.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    return transactions


@router.get("/low-stock")
async def get_low_stock_products(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get products with low stock."""
    business_id = get_user_business_id(current_user)
    
    # Products with low stock
    products = db.query(Product).filter(
        and_(
            Product.business_id == business_id,
            Product.inventory_count.isnot(None),
            Product.inventory_count <= 10  # Default threshold
        )
    ).all()
    
    # Variants with low stock
    variants = db.query(ProductVariant).join(Product).filter(
        and_(
            Product.business_id == business_id,
            ProductVariant.low_stock_threshold.isnot(None),
            ProductVariant.stock_quantity <= ProductVariant.low_stock_threshold
        )
    ).all()
    
    return {
        "products": [{"id": p.id, "name": p.name, "stock": p.inventory_count} for p in products],
        "variants": [{"id": v.id, "name": v.name, "stock": v.stock_quantity} for v in variants],
    }


