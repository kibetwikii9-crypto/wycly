"""Finance API routes - Invoices, Expenses, Payments, Taxes."""
import logging
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from pydantic import BaseModel

from app.database import get_db
from app.models import (
    Invoice, InvoiceItem, Expense, ExpenseCategory, Payment, PaymentMethod,
    TaxRate, TaxTransaction, Contact, Order, User as UserModel
)
from app.routes.auth import get_current_user, get_user_business_id

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/finance", tags=["finance"])


# ========== PYDANTIC MODELS ==========

class InvoiceItemCreate(BaseModel):
    product_id: Optional[int] = None
    service_id: Optional[int] = None
    description: str
    quantity: float = 1.0
    unit_price: float
    tax_rate: float = 0.0


class InvoiceCreate(BaseModel):
    contact_id: Optional[int] = None
    order_id: Optional[int] = None
    issue_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    items: List[InvoiceItemCreate]
    discount_amount: float = 0.0
    notes: Optional[str] = None


class InvoiceResponse(BaseModel):
    id: int
    invoice_number: str
    contact_id: Optional[int]
    order_id: Optional[int]
    status: str
    issue_date: datetime
    due_date: Optional[datetime]
    paid_date: Optional[datetime]
    subtotal: float
    tax_amount: float
    discount_amount: float
    total_amount: float
    currency: str
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ExpenseCategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = None


class ExpenseCategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    color: Optional[str]

    class Config:
        from_attributes = True


class ExpenseCreate(BaseModel):
    category_id: Optional[int] = None
    description: str
    amount: float
    currency: str = "USD"
    expense_date: Optional[datetime] = None
    receipt_url: Optional[str] = None
    payment_method: Optional[str] = None
    vendor: Optional[str] = None
    notes: Optional[str] = None


class ExpenseResponse(BaseModel):
    id: int
    category_id: Optional[int]
    user_id: Optional[int]
    description: str
    amount: float
    currency: str
    expense_date: datetime
    receipt_url: Optional[str]
    payment_method: Optional[str]
    vendor: Optional[str]
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class PaymentMethodCreate(BaseModel):
    name: str
    type: str
    credentials: Optional[str] = None


class PaymentMethodResponse(BaseModel):
    id: int
    name: str
    type: str
    is_active: bool

    class Config:
        from_attributes = True


class PaymentCreate(BaseModel):
    invoice_id: Optional[int] = None
    order_id: Optional[int] = None
    payment_method_id: Optional[int] = None
    amount: float
    currency: str = "USD"
    payment_date: Optional[datetime] = None
    reference_number: Optional[str] = None
    notes: Optional[str] = None


class PaymentResponse(BaseModel):
    id: int
    invoice_id: Optional[int]
    order_id: Optional[int]
    payment_method_id: Optional[int]
    amount: float
    currency: str
    payment_date: datetime
    reference_number: Optional[str]
    status: str
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class TaxRateCreate(BaseModel):
    name: str
    rate: float
    is_default: bool = False


class TaxRateResponse(BaseModel):
    id: int
    name: str
    rate: float
    is_default: bool
    is_active: bool

    class Config:
        from_attributes = True


# ========== INVOICE ENDPOINTS ==========

def generate_invoice_number(business_id: int, db: Session) -> str:
    """Generate unique invoice number."""
    count = db.query(Invoice).filter(Invoice.business_id == business_id).count()
    return f"INV-{business_id:04d}-{count + 1:05d}"


@router.post("/invoices/", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice(
    invoice_data: InvoiceCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new invoice."""
    business_id = get_user_business_id(current_user)
    
    # Calculate totals
    subtotal = sum(item.quantity * item.unit_price for item in invoice_data.items)
    tax_amount = sum(item.quantity * item.unit_price * (item.tax_rate / 100) for item in invoice_data.items)
    total_amount = subtotal + tax_amount - invoice_data.discount_amount
    
    # Create invoice
    invoice = Invoice(
        business_id=business_id,
        invoice_number=generate_invoice_number(business_id, db),
        contact_id=invoice_data.contact_id,
        order_id=invoice_data.order_id,
        issue_date=invoice_data.issue_date or datetime.utcnow(),
        due_date=invoice_data.due_date,
        subtotal=subtotal,
        tax_amount=tax_amount,
        discount_amount=invoice_data.discount_amount,
        total_amount=total_amount,
        currency="USD",
        notes=invoice_data.notes,
        status="draft",
    )
    db.add(invoice)
    db.flush()
    
    # Create invoice items
    for item_data in invoice_data.items:
        item = InvoiceItem(
            invoice_id=invoice.id,
            product_id=item_data.product_id,
            service_id=item_data.service_id,
            description=item_data.description,
            quantity=item_data.quantity,
            unit_price=item_data.unit_price,
            tax_rate=item_data.tax_rate,
            total=item_data.quantity * item_data.unit_price * (1 + item_data.tax_rate / 100),
        )
        db.add(item)
    
    db.commit()
    db.refresh(invoice)
    return invoice


@router.get("/invoices/", response_model=List[InvoiceResponse])
async def get_invoices(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all invoices."""
    business_id = get_user_business_id(current_user)
    query = db.query(Invoice).filter(Invoice.business_id == business_id)
    
    if status_filter:
        query = query.filter(Invoice.status == status_filter)
    
    invoices = query.order_by(Invoice.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    return invoices


@router.get("/invoices/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific invoice."""
    business_id = get_user_business_id(current_user)
    invoice = db.query(Invoice).filter(
        and_(Invoice.id == invoice_id, Invoice.business_id == business_id)
    ).first()
    
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    return invoice


@router.patch("/invoices/{invoice_id}/status")
async def update_invoice_status(
    invoice_id: int,
    new_status: str = Query(..., regex="^(draft|sent|paid|overdue|cancelled)$"),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update invoice status."""
    business_id = get_user_business_id(current_user)
    invoice = db.query(Invoice).filter(
        and_(Invoice.id == invoice_id, Invoice.business_id == business_id)
    ).first()
    
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    invoice.status = new_status
    if new_status == "paid":
        invoice.paid_date = datetime.utcnow()
    
    db.commit()
    return {"message": "Invoice status updated", "status": new_status}


# ========== EXPENSE ENDPOINTS ==========

@router.post("/expense-categories/", response_model=ExpenseCategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_expense_category(
    category_data: ExpenseCategoryCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create an expense category."""
    business_id = get_user_business_id(current_user)
    category = ExpenseCategory(
        business_id=business_id,
        name=category_data.name,
        description=category_data.description,
        color=category_data.color,
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.get("/expense-categories/", response_model=List[ExpenseCategoryResponse])
async def get_expense_categories(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all expense categories."""
    business_id = get_user_business_id(current_user)
    categories = db.query(ExpenseCategory).filter(
        ExpenseCategory.business_id == business_id
    ).all()
    return categories


@router.post("/expenses/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(
    expense_data: ExpenseCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new expense."""
    business_id = get_user_business_id(current_user)
    expense = Expense(
        business_id=business_id,
        category_id=expense_data.category_id,
        user_id=current_user.id,
        description=expense_data.description,
        amount=expense_data.amount,
        currency=expense_data.currency,
        expense_date=expense_data.expense_date or datetime.utcnow(),
        receipt_url=expense_data.receipt_url,
        payment_method=expense_data.payment_method,
        vendor=expense_data.vendor,
        notes=expense_data.notes,
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.get("/expenses/", response_model=List[ExpenseResponse])
async def get_expenses(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all expenses."""
    business_id = get_user_business_id(current_user)
    query = db.query(Expense).filter(Expense.business_id == business_id)
    
    if category_id:
        query = query.filter(Expense.category_id == category_id)
    if start_date:
        query = query.filter(Expense.expense_date >= start_date)
    if end_date:
        query = query.filter(Expense.expense_date <= end_date)
    
    expenses = query.order_by(Expense.expense_date.desc()).offset((page - 1) * limit).limit(limit).all()
    return expenses


# ========== PAYMENT ENDPOINTS ==========

@router.post("/payment-methods/", response_model=PaymentMethodResponse, status_code=status.HTTP_201_CREATED)
async def create_payment_method(
    method_data: PaymentMethodCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a payment method."""
    business_id = get_user_business_id(current_user)
    method = PaymentMethod(
        business_id=business_id,
        name=method_data.name,
        type=method_data.type,
        credentials=method_data.credentials,
    )
    db.add(method)
    db.commit()
    db.refresh(method)
    return method


@router.get("/payment-methods/", response_model=List[PaymentMethodResponse])
async def get_payment_methods(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all payment methods."""
    business_id = get_user_business_id(current_user)
    methods = db.query(PaymentMethod).filter(
        and_(PaymentMethod.business_id == business_id, PaymentMethod.is_active == True)
    ).all()
    return methods


@router.post("/payments/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment_data: PaymentCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a payment record."""
    business_id = get_user_business_id(current_user)
    payment = Payment(
        business_id=business_id,
        invoice_id=payment_data.invoice_id,
        order_id=payment_data.order_id,
        payment_method_id=payment_data.payment_method_id,
        amount=payment_data.amount,
        currency=payment_data.currency,
        payment_date=payment_data.payment_date or datetime.utcnow(),
        reference_number=payment_data.reference_number,
        notes=payment_data.notes,
        status="completed",
    )
    db.add(payment)
    
    # Update invoice status if linked
    if payment_data.invoice_id:
        invoice = db.query(Invoice).filter(Invoice.id == payment_data.invoice_id).first()
        if invoice:
            invoice.status = "paid"
            invoice.paid_date = payment.payment_date
    
    db.commit()
    db.refresh(payment)
    return payment


@router.get("/payments/", response_model=List[PaymentResponse])
async def get_payments(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    invoice_id: Optional[int] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all payments."""
    business_id = get_user_business_id(current_user)
    query = db.query(Payment).filter(Payment.business_id == business_id)
    
    if invoice_id:
        query = query.filter(Payment.invoice_id == invoice_id)
    
    payments = query.order_by(Payment.payment_date.desc()).offset((page - 1) * limit).limit(limit).all()
    return payments


# ========== TAX ENDPOINTS ==========

@router.post("/tax-rates/", response_model=TaxRateResponse, status_code=status.HTTP_201_CREATED)
async def create_tax_rate(
    tax_data: TaxRateCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a tax rate."""
    business_id = get_user_business_id(current_user)
    
    # If this is default, unset other defaults
    if tax_data.is_default:
        db.query(TaxRate).filter(
            and_(TaxRate.business_id == business_id, TaxRate.is_default == True)
        ).update({"is_default": False})
    
    tax_rate = TaxRate(
        business_id=business_id,
        name=tax_data.name,
        rate=tax_data.rate,
        is_default=tax_data.is_default,
    )
    db.add(tax_rate)
    db.commit()
    db.refresh(tax_rate)
    return tax_rate


@router.get("/tax-rates/", response_model=List[TaxRateResponse])
async def get_tax_rates(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all tax rates."""
    business_id = get_user_business_id(current_user)
    rates = db.query(TaxRate).filter(
        and_(TaxRate.business_id == business_id, TaxRate.is_active == True)
    ).all()
    return rates


# ========== FINANCIAL SUMMARY ENDPOINTS ==========

@router.get("/summary")
async def get_financial_summary(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get financial summary (revenue, expenses, profit)."""
    business_id = get_user_business_id(current_user)
    
    # Default to last 30 days
    if not end_date:
        end_date = datetime.utcnow()
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    # Total revenue (from paid invoices)
    revenue = db.query(func.sum(Invoice.total_amount)).filter(
        and_(
            Invoice.business_id == business_id,
            Invoice.status == "paid",
            Invoice.paid_date >= start_date,
            Invoice.paid_date <= end_date,
        )
    ).scalar() or 0.0
    
    # Total expenses
    expenses = db.query(func.sum(Expense.amount)).filter(
        and_(
            Expense.business_id == business_id,
            Expense.expense_date >= start_date,
            Expense.expense_date <= end_date,
        )
    ).scalar() or 0.0
    
    # Pending invoices
    pending_invoices = db.query(func.sum(Invoice.total_amount)).filter(
        and_(
            Invoice.business_id == business_id,
            Invoice.status.in_(["draft", "sent"]),
        )
    ).scalar() or 0.0
    
    return {
        "revenue": revenue,
        "expenses": expenses,
        "profit": revenue - expenses,
        "pending_invoices": pending_invoices,
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
    }

