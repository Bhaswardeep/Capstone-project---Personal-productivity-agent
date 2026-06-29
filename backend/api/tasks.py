"""Task and daily check-in API routes."""

from datetime import date as Date
from datetime import datetime as DateTime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.auth.security import get_current_user
from backend.database.database import get_db
from backend.models.models import DailyLog, Task, User
from backend.schemas.schemas import Category, DailyLogResponse, Priority, TaskResponse, TaskStatus
from backend.services.tasks import (
    complete_task,
    create_task,
    delete_task,
    get_today_log,
    get_user_task,
    get_user_tasks,
    update_task,
    upsert_today_log,
)

router = APIRouter(tags=["Tasks"])


class TaskCreateRequest(BaseModel):
    """Task fields accepted from the frontend."""

    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    category: Category = "Other"
    priority: Priority = "Medium"
    status: TaskStatus = "Pending"
    due_date: Date | None = None
    estimated_minutes: int | None = Field(default=None, ge=0)


class TaskUpdateRequest(BaseModel):
    """Optional task fields accepted during updates."""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    category: Category | None = None
    priority: Priority | None = None
    status: TaskStatus | None = None
    due_date: Date | None = None
    estimated_minutes: int | None = Field(default=None, ge=0)
    completed_at: DateTime | None = None


class MorningCheckInRequest(BaseModel):
    """Morning check-in data."""

    morning_notes: str | None = None


class EveningCheckInRequest(BaseModel):
    """Evening check-in data."""

    evening_notes: str | None = None
    wins: str | None = None
    challenges: str | None = None


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_user_task(
    task_data: TaskCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Task:
    """Create a task for the authenticated user."""
    return create_task(
        db=db,
        user_id=current_user.id,
        task_data=task_data.model_dump(),
    )


@router.get("/tasks", response_model=list[TaskResponse])
def read_user_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Task]:
    """Return tasks owned by the authenticated user."""
    return get_user_tasks(db=db, user_id=current_user.id)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def read_user_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Task:
    """Return a single task owned by the authenticated user."""
    task = get_user_task(db=db, user_id=current_user.id, task_id=task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_user_task(
    task_id: int,
    task_data: TaskUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Task:
    """Update a task owned by the authenticated user."""
    task = get_user_task(db=db, user_id=current_user.id, task_id=task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    update_data = task_data.model_dump(exclude_unset=True)
    return update_task(db=db, task=task, task_data=update_data)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a task owned by the authenticated user."""
    task = get_user_task(db=db, user_id=current_user.id, task_id=task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    delete_task(db=db, task=task)


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_user_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Task:
    """Mark a task owned by the authenticated user as completed."""
    task = get_user_task(db=db, user_id=current_user.id, task_id=task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    return complete_task(db=db, task=task)


@router.get("/checkin/morning", response_model=DailyLogResponse | None)
def read_morning_checkin(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DailyLog | None:
    """Return today's daily log for the authenticated user."""
    return get_today_log(db=db, user_id=current_user.id)


@router.post("/checkin/morning", response_model=DailyLogResponse, status_code=status.HTTP_201_CREATED)
def save_morning_checkin(
    checkin_data: MorningCheckInRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DailyLog:
    """Create or update today's morning check-in."""
    return upsert_today_log(
        db=db,
        user_id=current_user.id,
        log_data=checkin_data.model_dump(),
    )


@router.put("/checkin/morning", response_model=DailyLogResponse)
def update_morning_checkin(
    checkin_data: MorningCheckInRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DailyLog:
    """Update today's morning check-in."""
    return upsert_today_log(
        db=db,
        user_id=current_user.id,
        log_data=checkin_data.model_dump(),
    )


@router.post("/checkin/evening", response_model=DailyLogResponse)
def save_evening_checkin(
    checkin_data: EveningCheckInRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DailyLog:
    """Create or update today's evening check-in."""
    return upsert_today_log(
        db=db,
        user_id=current_user.id,
        log_data=checkin_data.model_dump(),
    )
