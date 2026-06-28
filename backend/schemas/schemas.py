"""Pydantic schemas for database entities."""

from __future__ import annotations

from datetime import date as Date
from datetime import datetime as DateTime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Category = Literal["Work", "Learning", "Health", "Personal", "Other"]
Priority = Literal["Low", "Medium", "High", "Critical"]
TaskStatus = Literal["Pending", "In Progress", "Completed", "Cancelled"]


class UserBase(BaseModel):
    """Shared user fields."""

    username: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=255, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class UserCreate(UserBase):
    """Fields required to create a stored user record."""

    password: str = Field(min_length=1, max_length=255)


class UserLogin(BaseModel):
    """Credentials required to authenticate a user."""

    email: str = Field(min_length=3, max_length=255, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    password: str = Field(min_length=1, max_length=255)


class UserUpdate(BaseModel):
    """Fields allowed when updating a user record."""

    username: str | None = Field(default=None, min_length=1, max_length=100)
    email: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    )
    password: str | None = Field(default=None, min_length=1, max_length=255)
    last_login: DateTime | None = None


class UserResponse(UserBase):
    """User data returned by the backend."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: DateTime
    last_login: DateTime | None = None


class TokenResponse(BaseModel):
    """JWT access token response."""

    access_token: str
    token_type: str = "bearer"


class TaskBase(BaseModel):
    """Shared task fields."""

    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    category: Category = "Other"
    priority: Priority = "Medium"
    status: TaskStatus = "Pending"
    due_date: Date | None = None
    estimated_minutes: int | None = Field(default=None, ge=0)
    completed_at: DateTime | None = None


class TaskCreate(TaskBase):
    """Fields required to create a task."""

    user_id: int


class TaskUpdate(BaseModel):
    """Fields allowed when updating a task."""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    category: Category | None = None
    priority: Priority | None = None
    status: TaskStatus | None = None
    due_date: Date | None = None
    estimated_minutes: int | None = Field(default=None, ge=0)
    completed_at: DateTime | None = None


class TaskResponse(TaskBase):
    """Task data returned by the backend."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: DateTime
    updated_at: DateTime


class DailyLogBase(BaseModel):
    """Shared daily log fields."""

    date: Date
    morning_notes: str | None = None
    evening_notes: str | None = None
    wins: str | None = None
    challenges: str | None = None


class DailyLogCreate(DailyLogBase):
    """Fields required to create a daily log."""

    user_id: int


class DailyLogUpdate(BaseModel):
    """Fields allowed when updating a daily log."""

    date: Date | None = None
    morning_notes: str | None = None
    evening_notes: str | None = None
    wins: str | None = None
    challenges: str | None = None


class DailyLogResponse(DailyLogBase):
    """Daily log data returned by the backend."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int


class EODSummaryBase(BaseModel):
    """Shared end-of-day summary fields."""

    date: Date
    summary: str = Field(min_length=1)
    tomorrow_plan: str | None = None


class EODSummaryCreate(EODSummaryBase):
    """Fields required to create an end-of-day summary."""

    user_id: int


class EODSummaryUpdate(BaseModel):
    """Fields allowed when updating an end-of-day summary."""

    date: Date | None = None
    summary: str | None = Field(default=None, min_length=1)
    tomorrow_plan: str | None = None


class EODSummaryResponse(EODSummaryBase):
    """End-of-day summary data returned by the backend."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: DateTime


class WeeklyReviewBase(BaseModel):
    """Shared weekly review fields."""

    week_start: Date
    week_end: Date
    review: str = Field(min_length=1)
    productivity_score: int | None = Field(default=None, ge=0, le=100)
    patterns: str | None = None
    recommendations: str | None = None


class WeeklyReviewCreate(WeeklyReviewBase):
    """Fields required to create a weekly review."""

    user_id: int


class WeeklyReviewUpdate(BaseModel):
    """Fields allowed when updating a weekly review."""

    week_start: Date | None = None
    week_end: Date | None = None
    review: str | None = Field(default=None, min_length=1)
    productivity_score: int | None = Field(default=None, ge=0, le=100)
    patterns: str | None = None
    recommendations: str | None = None


class WeeklyReviewResponse(WeeklyReviewBase):
    """Weekly review data returned by the backend."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: DateTime
