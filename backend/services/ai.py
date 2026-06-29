"""AI service abstraction for productivity planning and reviews."""

from __future__ import annotations

import os
from datetime import date, datetime
from typing import Any

from dotenv import load_dotenv

from backend.langgraph.graph import get_productivity_graph
from backend.langgraph.state import DailyLogState, ProductivityGraphState, TaskState
from backend.models.models import DailyLog, Task

load_dotenv()


def generate_morning_plan(
    today_tasks: list[dict[str, Any] | Task],
    morning_notes: str | None = None,
    user_id: int | None = None,
) -> dict[str, Any]:
    """Generate a prioritized morning plan."""
    state: ProductivityGraphState = {
        "user_id": user_id or 0,
        "workflow": "morning",
        "today_tasks": [_serialize_task(task) for task in today_tasks],
        "morning_notes": morning_notes,
        "metadata": _provider_metadata(),
    }
    result = get_productivity_graph().invoke(state)

    return {
        "prioritized_plan": result.get("prioritized_plan", []),
        "suggested_order": result.get("suggested_order", []),
        "estimated_focus": result.get("estimated_focus", ""),
        "motivational_advice": result.get("motivational_advice", ""),
        "classifications": result.get("classifications", []),
        "provider": result.get("metadata", {}).get("provider", "mock"),
    }


def generate_evening_summary(
    completed_tasks: list[dict[str, Any] | Task],
    pending_tasks: list[dict[str, Any] | Task],
    evening_notes: str | None = None,
    user_id: int | None = None,
) -> dict[str, Any]:
    """Generate an evening reflection and tomorrow recommendations."""
    state: ProductivityGraphState = {
        "user_id": user_id or 0,
        "workflow": "evening",
        "completed_tasks": [_serialize_task(task) for task in completed_tasks],
        "pending_tasks": [_serialize_task(task) for task in pending_tasks],
        "evening_notes": evening_notes,
        "metadata": _provider_metadata(),
    }
    result = get_productivity_graph().invoke(state)

    return {
        "daily_summary": result.get("daily_summary", ""),
        "achievements": result.get("achievements", []),
        "tomorrow_recommendations": result.get("tomorrow_recommendations", []),
        "encouragement": result.get("encouragement", ""),
        "overdue_tasks": result.get("overdue_tasks", []),
        "provider": result.get("metadata", {}).get("provider", "mock"),
    }


def generate_weekly_review(
    completed_tasks: list[dict[str, Any] | Task],
    missed_tasks: list[dict[str, Any] | Task],
    categories: dict[str, int] | None = None,
    daily_logs: list[dict[str, Any] | DailyLog] | None = None,
    user_id: int | None = None,
) -> dict[str, Any]:
    """Generate a weekly productivity review."""
    state: ProductivityGraphState = {
        "user_id": user_id or 0,
        "workflow": "weekly",
        "completed_tasks": [_serialize_task(task) for task in completed_tasks],
        "missed_tasks": [_serialize_task(task) for task in missed_tasks],
        "daily_logs": [_serialize_daily_log(log) for log in daily_logs or []],
        "metadata": {
            **_provider_metadata(),
            "category_counts": categories or {},
        },
    }
    result = get_productivity_graph().invoke(state)

    return {
        "productivity_score": result.get("productivity_score", 0),
        "strengths": result.get("strengths", []),
        "weaknesses": result.get("weaknesses", []),
        "recurring_patterns": result.get("recurring_patterns", []),
        "recommendations": result.get("recommendations", []),
        "weekly_summary": result.get("weekly_summary", ""),
        "provider": result.get("metadata", {}).get("provider", "mock"),
    }


def _provider_metadata() -> dict[str, Any]:
    """Return provider configuration without exposing secrets."""
    provider = os.getenv("LLM_PROVIDER")
    openai_key = os.getenv("OPENAI_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    has_key = bool(openai_key or groq_key)

    return {
        "provider": provider if provider and has_key else "mock",
        "mock": not (provider and has_key),
    }


def _serialize_task(task: dict[str, Any] | Task) -> TaskState:
    """Convert ORM or request task data into graph state."""
    if isinstance(task, dict):
        return {
            "id": task.get("id"),
            "title": task.get("title", "Untitled task"),
            "description": task.get("description"),
            "category": task.get("category"),
            "priority": task.get("priority"),
            "status": task.get("status"),
            "due_date": _serialize_date(task.get("due_date")),
            "estimated_minutes": task.get("estimated_minutes"),
            "completed_at": _serialize_datetime(task.get("completed_at")),
        }

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "category": task.category,
        "priority": task.priority,
        "status": task.status,
        "due_date": _serialize_date(task.due_date),
        "estimated_minutes": task.estimated_minutes,
        "completed_at": _serialize_datetime(task.completed_at),
    }


def _serialize_daily_log(log: dict[str, Any] | DailyLog) -> DailyLogState:
    """Convert ORM or request daily log data into graph state."""
    if isinstance(log, dict):
        return {
            "date": _serialize_date(log.get("date")) or "",
            "morning_notes": log.get("morning_notes"),
            "evening_notes": log.get("evening_notes"),
            "wins": log.get("wins"),
            "challenges": log.get("challenges"),
        }

    return {
        "date": _serialize_date(log.date) or "",
        "morning_notes": log.morning_notes,
        "evening_notes": log.evening_notes,
        "wins": log.wins,
        "challenges": log.challenges,
    }


def _serialize_date(value: Any) -> str | None:
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str):
        return value
    return None


def _serialize_datetime(value: Any) -> str | None:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, str):
        return value
    return None
