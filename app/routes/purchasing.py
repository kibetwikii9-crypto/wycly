"""Purchasing API routes - Suppliers, Purchase Orders."""
import logging
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from pydantic import BaseModel

from app.database import get_db
from app.models import Supplier, PurchaseOrder, PurchaseOrderItem, Product, User as UserModel
from app.routes.auth import get_current_user, get_user_business_id

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/purchasing", tags=["purchasing"])


# ========== PYDANTIC MODELS ==========

class SupplierCreate(BaseModel):
    name: str
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    payment_terms: Optional[str] = None
    notes: Optional[str] = None


class SupplierResponse(BaseModel):
    id: int
    name: str
    contact_person: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    payment_terms: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class PurchaseOrderItemCreate(BaseModel):
    product_id: Optional[int] = None
    description: str
    quantity: float
    unit_price: float


class PurchaseOrderCreate(BaseModel):
    supplier_id: int
    expected_delivery_date: Optional[datetime] = None
    items: List[PurchaseOrderItemCreate]
    notes: Optional[str] = None


class PurchaseOrderResponse(BaseModel):
    id: int
    supplier_id: int
    po_number: str
    status: str
    order_date: datetime
    expected_delivery_date: Optional[datetime]
    received_date: Optional[datetime]
    subtotal: float
    tax_amount: float
    total_amount: float
    currency: str
    created_at: datetime

    class Config:
        from_attributes = True


# ========== SUPPLIER ENDPOINTS ==========

def generate_po_number(business_id: int, db: Session) -> str:
    """Generate unique PO number."""
    count = db.query(PurchaseOrder).filter(PurchaseOrder.business_id == business_id).count()
    return f"PO-{business_id:04d}-{count + 1:05d}"


@router.post("/suppliers/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
async def create_supplier(
    supplier_data: SupplierCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new supplier."""
    business_id = get_user_business_id(current_user)
    supplier = Supplier(
        business_id=business_id,
        name=supplier_data.name,
        contact_person=supplier_data.contact_person,
        email=supplier_data.email,
        phone=supplier_data.phone,
        address=supplier_data.address,
        payment_terms=supplier_data.payment_terms,
        notes=supplier_data.notes,
    )
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


@router.get("/suppliers/", response_model=List[SupplierResponse])
async def get_suppliers(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all suppliers."""
    business_id = get_user_business_id(current_user)
    suppliers = db.query(Supplier).filter(
        and_(Supplier.business_id == business_id, Supplier.is_active == True)
    ).all()
    return suppliers


# ========== PURCHASE ORDER ENDPOINTS ==========

@router.post("/purchase-orders/", response_model=PurchaseOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_purchase_order(
    po_data: PurchaseOrderCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a purchase order."""
    business_id = get_user_business_id(current_user)
    
    # Verify supplier belongs to business
    supplier = db.query(Supplier).filter(
        and_(Supplier.id == po_data.supplier_id, Supplier.business_id == business_id)
    ).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    # Calculate totals
    subtotal = sum(item.quantity * item.unit_price for item in po_data.items)
    tax_amount = subtotal * 0.16  # Default 16% tax
    total_amount = subtotal + tax_amount
    
    # Create PO
    po = PurchaseOrder(
        business_id=business_id,
        supplier_id=po_data.supplier_id,
        po_number=generate_po_number(business_id, db),
        order_date=datetime.utcnow(),
        expected_delivery_date=po_data.expected_delivery_date,
        subtotal=subtotal,
        tax_amount=tax_amount,
        total_amount=total_amount,
        currency="USD",
        notes=po_data.notes,
        status="pending",
        created_by_user_id=current_user.id,
    )
    db.add(po)
    db.flush()
    
    # Create PO items
    for item_data in po_data.items:
        item = PurchaseOrderItem(
            purchase_order_id=po.id,
            product_id=item_data.product_id,
            description=item_data.description,
            quantity=item_data.quantity,
            unit_price=item_data.unit_price,
            total=item_data.quantity * item_data.unit_price,
        )
        db.add(item)
    
    db.commit()
    db.refresh(po)
    return po


@router.get("/purchase-orders/", response_model=List[PurchaseOrderResponse])
async def get_purchase_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all purchase orders."""
    business_id = get_user_business_id(current_user)
    query = db.query(PurchaseOrder).filter(PurchaseOrder.business_id == business_id)
    
    if status_filter:
        query = query.filter(PurchaseOrder.status == status_filter)
    
    pos = query.order_by(PurchaseOrder.order_date.desc()).offset((page - 1) * limit).limit(limit).all()
    return pos


@router.patch("/purchase-orders/{po_id}/status")
async def update_po_status(
    po_id: int,
    new_status: str = Query(..., regex="^(pending|ordered|received|paid|cancelled)$"),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update purchase order status."""
    business_id = get_user_business_id(current_user)
    po = db.query(PurchaseOrder).filter(
        and_(PurchaseOrder.id == po_id, PurchaseOrder.business_id == business_id)
    ).first()
    
    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    
    po.status = new_status
    if new_status == "received":
        po.received_date = datetime.utcnow()
    
    db.commit()
    return {"message": "Purchase order status updated", "status": new_status}

