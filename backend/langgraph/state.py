"""Typed state shared by the productivity LangGraph workflow."""

from __future__ import annotations

from typing import Any, Literal, TypedDict


WorkflowType = Literal["morning", "evening", "weekly"]


class TaskState(TypedDict, total=False):
    """Task shape used inside AI workflows."""

    id: int | None
    title: str
    description: str | None
    category: str | None
    priority: str | None
    status: str | None
    due_date: str | None
    estimated_minutes: int | None
    completed_at: str | None


class DailyLogState(TypedDict, total=False):
    """Daily log shape used for weekly review context."""

    date: str
    morning_notes: str | None
    evening_notes: str | None
    wins: str | None
    challenges: str | None


class ClassificationState(TypedDict):
    """AI classification output for a single task."""

    title: str
    category: str
    priority: str
    urgency: str


class ProductivityGraphState(TypedDict, total=False):
    """Complete state for the productivity AI graph."""

    user_id: int
    workflow: WorkflowType
    today_tasks: list[TaskState]
    completed_tasks: list[TaskState]
    pending_tasks: list[TaskState]
    missed_tasks: list[TaskState]
    overdue_tasks: list[TaskState]
    daily_logs: list[DailyLogState]
    morning_notes: str | None
    evening_notes: str | None
    wins: str | None
    challenges: str | None
    classifications: list[ClassificationState]
    prioritized_plan: list[str]
    suggested_order: list[str]
    estimated_focus: str
    motivational_advice: str
    daily_summary: str
    achievements: list[str]
    tomorrow_recommendations: list[str]
    encouragement: str
    productivity_score: int
    strengths: list[str]
    weaknesses: list[str]
    recurring_patterns: list[str]
    recommendations: list[str]
    weekly_summary: str
    metadata: dict[str, Any]
