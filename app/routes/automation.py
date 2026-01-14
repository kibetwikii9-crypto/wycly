"""Automation API routes - Recurring Tasks, Scheduled Jobs."""
import logging
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from pydantic import BaseModel

from app.database import get_db
from app.models import RecurringTask, ScheduledJob, User as UserModel
from app.routes.auth import get_current_user, get_user_business_id

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/automation", tags=["automation"])


# ========== PYDANTIC MODELS ==========

class RecurringTaskCreate(BaseModel):
    name: str
    description: Optional[str] = None
    frequency: str  # daily, weekly, monthly, yearly, custom
    frequency_value: Optional[int] = None
    next_run_date: datetime


class RecurringTaskResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    frequency: str
    frequency_value: Optional[int]
    next_run_date: datetime
    last_run_date: Optional[datetime]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ScheduledJobCreate(BaseModel):
    job_type: str
    job_name: str
    schedule: str  # cron expression or frequency
    config: Optional[str] = None


class ScheduledJobResponse(BaseModel):
    id: int
    job_type: str
    job_name: str
    schedule: str
    last_run: Optional[datetime]
    next_run: Optional[datetime]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ========== RECURRING TASK ENDPOINTS ==========

@router.post("/recurring-tasks/", response_model=RecurringTaskResponse, status_code=status.HTTP_201_CREATED)
async def create_recurring_task(
    task_data: RecurringTaskCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a recurring task."""
    business_id = get_user_business_id(current_user)
    task = RecurringTask(
        business_id=business_id,
        name=task_data.name,
        description=task_data.description,
        frequency=task_data.frequency,
        frequency_value=task_data.frequency_value,
        next_run_date=task_data.next_run_date,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/recurring-tasks/", response_model=List[RecurringTaskResponse])
async def get_recurring_tasks(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all recurring tasks."""
    business_id = get_user_business_id(current_user)
    tasks = db.query(RecurringTask).filter(
        and_(RecurringTask.business_id == business_id, RecurringTask.is_active == True)
    ).order_by(RecurringTask.next_run_date).all()
    return tasks


@router.patch("/recurring-tasks/{task_id}/run")
async def mark_task_run(
    task_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark a recurring task as run and calculate next run date."""
    business_id = get_user_business_id(current_user)
    task = db.query(RecurringTask).filter(
        and_(RecurringTask.id == task_id, RecurringTask.business_id == business_id)
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Recurring task not found")
    
    task.last_run_date = datetime.utcnow()
    
    # Calculate next run date
    if task.frequency == "daily":
        task.next_run_date = datetime.utcnow() + timedelta(days=1)
    elif task.frequency == "weekly":
        task.next_run_date = datetime.utcnow() + timedelta(weeks=1)
    elif task.frequency == "monthly":
        task.next_run_date = datetime.utcnow() + timedelta(days=30)
    elif task.frequency == "yearly":
        task.next_run_date = datetime.utcnow() + timedelta(days=365)
    elif task.frequency == "custom" and task.frequency_value:
        task.next_run_date = datetime.utcnow() + timedelta(days=task.frequency_value)
    
    db.commit()
    return {"message": "Task marked as run", "next_run_date": task.next_run_date}


# ========== SCHEDULED JOB ENDPOINTS ==========

@router.post("/scheduled-jobs/", response_model=ScheduledJobResponse, status_code=status.HTTP_201_CREATED)
async def create_scheduled_job(
    job_data: ScheduledJobCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a scheduled job."""
    business_id = get_user_business_id(current_user)
    
    # Calculate next run (simplified - in production, use cron parser)
    next_run = datetime.utcnow() + timedelta(days=1)
    
    job = ScheduledJob(
        business_id=business_id,
        job_type=job_data.job_type,
        job_name=job_data.job_name,
        schedule=job_data.schedule,
        config=job_data.config,
        next_run=next_run,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("/scheduled-jobs/", response_model=List[ScheduledJobResponse])
async def get_scheduled_jobs(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all scheduled jobs."""
    business_id = get_user_business_id(current_user)
    jobs = db.query(ScheduledJob).filter(
        and_(ScheduledJob.business_id == business_id, ScheduledJob.is_active == True)
    ).order_by(ScheduledJob.next_run).all()
    return jobs


@router.patch("/scheduled-jobs/{job_id}/run")
async def mark_job_run(
    job_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark a scheduled job as run."""
    business_id = get_user_business_id(current_user)
    job = db.query(ScheduledJob).filter(
        and_(ScheduledJob.id == job_id, ScheduledJob.business_id == business_id)
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Scheduled job not found")
    
    job.last_run = datetime.utcnow()
    # Calculate next run (simplified)
    job.next_run = datetime.utcnow() + timedelta(days=1)
    
    db.commit()
    return {"message": "Job marked as run", "next_run": job.next_run}

