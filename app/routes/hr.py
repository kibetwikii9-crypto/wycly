"""HR & Employee Management API routes."""
import logging
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, or_
from pydantic import BaseModel, EmailStr

from app.database import get_db
from app.models import (
    Employee, Department, Attendance, LeaveRequest, PerformanceReview, EmployeeDocument,
    User as UserModel
)
from app.routes.auth import get_current_user, get_user_business_id

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/hr", tags=["hr"])


# ========== PYDANTIC MODELS ==========

class DepartmentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    manager_id: Optional[int] = None
    parent_department_id: Optional[int] = None


class DepartmentResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    manager_id: Optional[int]
    parent_department_id: Optional[int]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class EmployeeCreate(BaseModel):
    user_id: int
    employee_number: Optional[str] = None
    department_id: Optional[int] = None
    position: Optional[str] = None
    hire_date: Optional[datetime] = None
    employment_type: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    salary: Optional[float] = None
    currency: str = "USD"


class EmployeeResponse(BaseModel):
    id: int
    user_id: int
    employee_number: Optional[str]
    department_id: Optional[int]
    position: Optional[str]
    hire_date: Optional[datetime]
    employment_type: Optional[str]
    phone: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AttendanceCreate(BaseModel):
    employee_id: int
    date: datetime
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    status: str = "present"
    notes: Optional[str] = None


class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    date: datetime
    check_in: Optional[datetime]
    check_out: Optional[datetime]
    total_hours: Optional[float]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class LeaveRequestCreate(BaseModel):
    employee_id: int
    leave_type: str
    start_date: datetime
    end_date: datetime
    reason: Optional[str] = None


class LeaveRequestResponse(BaseModel):
    id: int
    employee_id: int
    leave_type: str
    start_date: datetime
    end_date: datetime
    days_requested: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class PerformanceReviewCreate(BaseModel):
    employee_id: int
    review_period_start: datetime
    review_period_end: datetime
    overall_rating: Optional[int] = None
    goals_achieved: Optional[str] = None
    strengths: Optional[str] = None
    areas_for_improvement: Optional[str] = None
    comments: Optional[str] = None


class PerformanceReviewResponse(BaseModel):
    id: int
    employee_id: int
    review_period_start: datetime
    review_period_end: datetime
    overall_rating: Optional[int]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class EmployeeDocumentCreate(BaseModel):
    employee_id: int
    document_type: str
    title: str
    file_url: str
    file_name: str
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    expiry_date: Optional[datetime] = None
    notes: Optional[str] = None


class EmployeeDocumentResponse(BaseModel):
    id: int
    employee_id: int
    document_type: str
    title: str
    file_url: str
    file_name: str
    expiry_date: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


# ========== DEPARTMENT ENDPOINTS ==========

@router.post("/departments/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(
    dept_data: DepartmentCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a department."""
    business_id = get_user_business_id(current_user)
    department = Department(
        business_id=business_id,
        name=dept_data.name,
        description=dept_data.description,
        manager_id=dept_data.manager_id,
        parent_department_id=dept_data.parent_department_id,
    )
    db.add(department)
    db.commit()
    db.refresh(department)
    return department


@router.get("/departments/", response_model=List[DepartmentResponse])
async def get_departments(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all departments."""
    business_id = get_user_business_id(current_user)
    departments = db.query(Department).filter(
        and_(Department.business_id == business_id, Department.is_active == True)
    ).all()
    return departments


# ========== EMPLOYEE ENDPOINTS ==========

def generate_employee_number(business_id: int, db: Session) -> str:
    """Generate unique employee number."""
    count = db.query(Employee).filter(Employee.business_id == business_id).count()
    return f"EMP-{business_id:04d}-{count + 1:05d}"


@router.post("/employees/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(
    emp_data: EmployeeCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create an employee profile."""
    business_id = get_user_business_id(current_user)
    
    # Verify user belongs to business
    user = db.query(UserModel).filter(
        and_(UserModel.id == emp_data.user_id, UserModel.business_id == business_id)
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found or doesn't belong to business")
    
    # Check if employee profile already exists
    existing = db.query(Employee).filter(Employee.user_id == emp_data.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Employee profile already exists for this user")
    
    employee = Employee(
        business_id=business_id,
        user_id=emp_data.user_id,
        employee_number=emp_data.employee_number or generate_employee_number(business_id, db),
        department_id=emp_data.department_id,
        position=emp_data.position,
        hire_date=emp_data.hire_date or datetime.utcnow(),
        employment_type=emp_data.employment_type,
        phone=emp_data.phone,
        address=emp_data.address,
        city=emp_data.city,
        country=emp_data.country,
        date_of_birth=emp_data.date_of_birth,
        emergency_contact_name=emp_data.emergency_contact_name,
        emergency_contact_phone=emp_data.emergency_contact_phone,
        salary=emp_data.salary,
        currency=emp_data.currency,
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


@router.get("/employees/", response_model=List[EmployeeResponse])
async def get_employees(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    department_id: Optional[int] = None,
    search: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all employees."""
    business_id = get_user_business_id(current_user)
    query = db.query(Employee).filter(Employee.business_id == business_id)
    
    if department_id:
        query = query.filter(Employee.department_id == department_id)
    if search:
        query = query.join(UserModel).filter(
            or_(
                Employee.employee_number.ilike(f"%{search}%"),
                Employee.position.ilike(f"%{search}%"),
                UserModel.full_name.ilike(f"%{search}%"),
                UserModel.email.ilike(f"%{search}%"),
            )
        )
    
    employees = query.order_by(Employee.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    return employees


@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
    employee_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific employee."""
    business_id = get_user_business_id(current_user)
    employee = db.query(Employee).filter(
        and_(Employee.id == employee_id, Employee.business_id == business_id)
    ).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return employee


# ========== ATTENDANCE ENDPOINTS ==========

@router.post("/attendance/", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
async def create_attendance(
    att_data: AttendanceCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create attendance record."""
    business_id = get_user_business_id(current_user)
    
    # Verify employee belongs to business
    employee = db.query(Employee).filter(
        and_(Employee.id == att_data.employee_id, Employee.business_id == business_id)
    ).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Calculate total hours if check_in and check_out provided
    total_hours = None
    if att_data.check_in and att_data.check_out:
        delta = att_data.check_out - att_data.check_in
        total_hours = delta.total_seconds() / 3600.0
    
    attendance = Attendance(
        business_id=business_id,
        employee_id=att_data.employee_id,
        date=att_data.date,
        check_in=att_data.check_in,
        check_out=att_data.check_out,
        total_hours=total_hours,
        status=att_data.status,
        notes=att_data.notes,
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance


@router.get("/attendance/", response_model=List[AttendanceResponse])
async def get_attendance(
    employee_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get attendance records."""
    business_id = get_user_business_id(current_user)
    query = db.query(Attendance).filter(Attendance.business_id == business_id)
    
    if employee_id:
        query = query.filter(Attendance.employee_id == employee_id)
    if start_date:
        query = query.filter(Attendance.date >= start_date)
    if end_date:
        query = query.filter(Attendance.date <= end_date)
    
    attendance = query.order_by(Attendance.date.desc()).offset((page - 1) * limit).limit(limit).all()
    return attendance


# ========== LEAVE REQUEST ENDPOINTS ==========

@router.post("/leave-requests/", response_model=LeaveRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_leave_request(
    leave_data: LeaveRequestCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a leave request."""
    business_id = get_user_business_id(current_user)
    
    # Verify employee belongs to business
    employee = db.query(Employee).filter(
        and_(Employee.id == leave_data.employee_id, Employee.business_id == business_id)
    ).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Calculate days requested
    delta = leave_data.end_date - leave_data.start_date
    days_requested = delta.days + 1
    
    leave_request = LeaveRequest(
        business_id=business_id,
        employee_id=leave_data.employee_id,
        leave_type=leave_data.leave_type,
        start_date=leave_data.start_date,
        end_date=leave_data.end_date,
        days_requested=days_requested,
        reason=leave_data.reason,
        status="pending",
    )
    db.add(leave_request)
    db.commit()
    db.refresh(leave_request)
    return leave_request


@router.get("/leave-requests/", response_model=List[LeaveRequestResponse])
async def get_leave_requests(
    employee_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get leave requests."""
    business_id = get_user_business_id(current_user)
    query = db.query(LeaveRequest).filter(LeaveRequest.business_id == business_id)
    
    if employee_id:
        query = query.filter(LeaveRequest.employee_id == employee_id)
    if status_filter:
        query = query.filter(LeaveRequest.status == status_filter)
    
    leave_requests = query.order_by(LeaveRequest.created_at.desc()).all()
    return leave_requests


@router.patch("/leave-requests/{leave_id}/approve")
async def approve_leave_request(
    leave_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Approve a leave request."""
    business_id = get_user_business_id(current_user)
    leave_request = db.query(LeaveRequest).filter(
        and_(LeaveRequest.id == leave_id, LeaveRequest.business_id == business_id)
    ).first()
    
    if not leave_request:
        raise HTTPException(status_code=404, detail="Leave request not found")
    
    leave_request.status = "approved"
    leave_request.approved_by_user_id = current_user.id
    leave_request.approved_at = datetime.utcnow()
    db.commit()
    return {"message": "Leave request approved", "status": "approved"}


# ========== PERFORMANCE REVIEW ENDPOINTS ==========

@router.post("/performance-reviews/", response_model=PerformanceReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_performance_review(
    review_data: PerformanceReviewCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a performance review."""
    business_id = get_user_business_id(current_user)
    
    # Verify employee belongs to business
    employee = db.query(Employee).filter(
        and_(Employee.id == review_data.employee_id, Employee.business_id == business_id)
    ).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    review = PerformanceReview(
        business_id=business_id,
        employee_id=review_data.employee_id,
        review_period_start=review_data.review_period_start,
        review_period_end=review_data.review_period_end,
        reviewed_by_user_id=current_user.id,
        overall_rating=review_data.overall_rating,
        goals_achieved=review_data.goals_achieved,
        strengths=review_data.strengths,
        areas_for_improvement=review_data.areas_for_improvement,
        comments=review_data.comments,
        status="draft",
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.get("/performance-reviews/", response_model=List[PerformanceReviewResponse])
async def get_performance_reviews(
    employee_id: Optional[int] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get performance reviews."""
    business_id = get_user_business_id(current_user)
    query = db.query(PerformanceReview).filter(PerformanceReview.business_id == business_id)
    
    if employee_id:
        query = query.filter(PerformanceReview.employee_id == employee_id)
    
    reviews = query.order_by(PerformanceReview.review_period_end.desc()).all()
    return reviews


# ========== EMPLOYEE DOCUMENT ENDPOINTS ==========

@router.post("/documents/", response_model=EmployeeDocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_employee_document(
    doc_data: EmployeeDocumentCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create an employee document."""
    business_id = get_user_business_id(current_user)
    
    # Verify employee belongs to business
    employee = db.query(Employee).filter(
        and_(Employee.id == doc_data.employee_id, Employee.business_id == business_id)
    ).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    document = EmployeeDocument(
        business_id=business_id,
        employee_id=doc_data.employee_id,
        document_type=doc_data.document_type,
        title=doc_data.title,
        file_url=doc_data.file_url,
        file_name=doc_data.file_name,
        file_size=doc_data.file_size,
        file_type=doc_data.file_type,
        expiry_date=doc_data.expiry_date,
        notes=doc_data.notes,
        uploaded_by_user_id=current_user.id,
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


@router.get("/documents/", response_model=List[EmployeeDocumentResponse])
async def get_employee_documents(
    employee_id: Optional[int] = None,
    document_type: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get employee documents."""
    business_id = get_user_business_id(current_user)
    query = db.query(EmployeeDocument).filter(EmployeeDocument.business_id == business_id)
    
    if employee_id:
        query = query.filter(EmployeeDocument.employee_id == employee_id)
    if document_type:
        query = query.filter(EmployeeDocument.document_type == document_type)
    
    documents = query.order_by(EmployeeDocument.created_at.desc()).all()
    return documents


