"""Projects & Tasks API routes."""
import logging
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from pydantic import BaseModel

from app.database import get_db
from app.models import Project, Task, TaskAssignment, TaskComment, User as UserModel
from app.routes.auth import get_current_user, get_user_business_id

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/projects", tags=["projects"])


# ========== PYDANTIC MODELS ==========

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "planning"
    priority: str = "medium"
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    assigned_to_user_id: Optional[int] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: str
    priority: str
    start_date: Optional[datetime]
    due_date: Optional[datetime]
    completed_date: Optional[datetime]
    progress: int
    assigned_to_user_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    project_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    status: str = "todo"
    priority: str = "medium"
    due_date: Optional[datetime] = None
    assigned_user_ids: Optional[List[int]] = []


class TaskResponse(BaseModel):
    id: int
    project_id: Optional[int]
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[datetime]
    completed_date: Optional[datetime]
    created_by_user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TaskCommentCreate(BaseModel):
    task_id: int
    comment: str


# ========== PROJECT ENDPOINTS ==========

@router.post("/projects/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new project."""
    business_id = get_user_business_id(current_user)
    project = Project(
        business_id=business_id,
        name=project_data.name,
        description=project_data.description,
        status=project_data.status,
        priority=project_data.priority,
        start_date=project_data.start_date,
        due_date=project_data.due_date,
        assigned_to_user_id=project_data.assigned_to_user_id,
        created_by_user_id=current_user.id,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/projects/", response_model=List[ProjectResponse])
async def get_projects(
    status_filter: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all projects."""
    business_id = get_user_business_id(current_user)
    query = db.query(Project).filter(Project.business_id == business_id)
    
    if status_filter:
        query = query.filter(Project.status == status_filter)
    
    projects = query.order_by(Project.created_at.desc()).all()
    return projects


@router.patch("/projects/{project_id}/status")
async def update_project_status(
    project_id: int,
    new_status: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update project status."""
    business_id = get_user_business_id(current_user)
    project = db.query(Project).filter(
        and_(Project.id == project_id, Project.business_id == business_id)
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project.status = new_status
    if new_status == "completed":
        project.completed_date = datetime.utcnow()
        project.progress = 100
    
    db.commit()
    return {"message": "Project status updated", "status": new_status}


# ========== TASK ENDPOINTS ==========

@router.post("/tasks/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new task."""
    business_id = get_user_business_id(current_user)
    
    # Verify project belongs to business if provided
    if task_data.project_id:
        project = db.query(Project).filter(
            and_(Project.id == task_data.project_id, Project.business_id == business_id)
        ).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
    
    task = Task(
        business_id=business_id,
        project_id=task_data.project_id,
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        due_date=task_data.due_date,
        created_by_user_id=current_user.id,
    )
    db.add(task)
    db.flush()
    
    # Assign users
    for user_id in task_data.assigned_user_ids or []:
        assignment = TaskAssignment(
            task_id=task.id,
            user_id=user_id,
            assigned_by_user_id=current_user.id,
        )
        db.add(assignment)
    
    db.commit()
    db.refresh(task)
    return task


@router.get("/tasks/", response_model=List[TaskResponse])
async def get_tasks(
    project_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all tasks."""
    business_id = get_user_business_id(current_user)
    query = db.query(Task).filter(Task.business_id == business_id)
    
    if project_id:
        query = query.filter(Task.project_id == project_id)
    if status_filter:
        query = query.filter(Task.status == status_filter)
    
    tasks = query.order_by(Task.created_at.desc()).all()
    return tasks


@router.patch("/tasks/{task_id}/status")
async def update_task_status(
    task_id: int,
    new_status: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update task status."""
    business_id = get_user_business_id(current_user)
    task = db.query(Task).filter(
        and_(Task.id == task_id, Task.business_id == business_id)
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = new_status
    if new_status == "done":
        task.completed_date = datetime.utcnow()
    
    db.commit()
    return {"message": "Task status updated", "status": new_status}


@router.post("/tasks/{task_id}/comments")
async def add_task_comment(
    task_id: int,
    comment_data: TaskCommentCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add a comment to a task."""
    business_id = get_user_business_id(current_user)
    task = db.query(Task).filter(
        and_(Task.id == task_id, Task.business_id == business_id)
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    comment = TaskComment(
        task_id=task_id,
        user_id=current_user.id,
        comment=comment_data.comment,
    )
    db.add(comment)
    db.commit()
    return {"message": "Comment added", "comment_id": comment.id}


