"""AI API routes."""

from __future__ import annotations

from datetime import date as Date
from datetime import datetime as DateTime

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from backend.auth.security import get_current_user
from backend.models.models import User
from backend.schemas.schemas import Category, Priority, TaskStatus
from backend.services.ai import (
    generate_evening_summary,
    generate_morning_plan,
    generate_weekly_review,
)

router = APIRouter(prefix="/ai", tags=["AI"])


class AITask(BaseModel):
    """Task payload accepted by AI endpoints."""

    id: int | None = None
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    category: Category | None = None
    priority: Priority | None = None
    status: TaskStatus | None = None
    due_date: Date | None = None
    estimated_minutes: int | None = Field(default=None, ge=0)
    completed_at: DateTime | None = None


class AIDailyLog(BaseModel):
    """Daily log payload accepted by weekly review."""

    date: Date
    morning_notes: str | None = None
    evening_notes: str | None = None
    wins: str | None = None
    challenges: str | None = None


class MorningPlanRequest(BaseModel):
    """Request body for morning planning."""

    today_tasks: list[AITask]
    morning_notes: str | None = None


class EveningSummaryRequest(BaseModel):
    """Request body for evening reflection."""

    completed_tasks: list[AITask]
    pending_tasks: list[AITask]
    evening_notes: str | None = None
    wins: str | None = None
    challenges: str | None = None


class WeeklyReviewRequest(BaseModel):
    """Request body for weekly review."""

    completed_tasks: list[AITask]
    missed_tasks: list[AITask]
    categories: dict[str, int] = Field(default_factory=dict)
    daily_logs: list[AIDailyLog] = Field(default_factory=list)


@router.post("/morning-plan")
def create_morning_plan(
    request: MorningPlanRequest,
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return a prioritized AI morning plan."""
    return generate_morning_plan(
        today_tasks=[task.model_dump() for task in request.today_tasks],
        morning_notes=request.morning_notes,
        user_id=current_user.id,
    )


@router.post("/evening-summary")
def create_evening_summary(
    request: EveningSummaryRequest,
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return an AI evening summary and tomorrow recommendations."""
    return generate_evening_summary(
        completed_tasks=[task.model_dump() for task in request.completed_tasks],
        pending_tasks=[task.model_dump() for task in request.pending_tasks],
        evening_notes=request.evening_notes,
        wins=request.wins,
        challenges=request.challenges,
        user_id=current_user.id,
    )


@router.post("/weekly-review")
def create_weekly_review(
    request: WeeklyReviewRequest,
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return an AI weekly productivity review."""
    return generate_weekly_review(
        completed_tasks=[task.model_dump() for task in request.completed_tasks],
        missed_tasks=[task.model_dump() for task in request.missed_tasks],
        categories=request.categories,
        daily_logs=[log.model_dump() for log in request.daily_logs],
        user_id=current_user.id,
    )
