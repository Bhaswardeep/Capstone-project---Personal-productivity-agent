"""Dashboard statistics service functions."""

from __future__ import annotations

from collections import Counter
from datetime import date, timedelta

from sqlalchemy.orm import Session

from backend.models.models import Task


def get_dashboard_statistics(db: Session, user_id: int) -> dict:
    """Return task statistics for the authenticated user's dashboard."""
    today = date.today()
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    todays_tasks = [task for task in tasks if _is_today_task(task, today)]
    completed_today = [
        task for task in tasks if task.completed_at and task.completed_at.date() == today
    ]
    pending_today = [task for task in todays_tasks if task.status != "Completed"]
    overdue_tasks = [
        task
        for task in tasks
        if task.due_date and task.due_date < today and task.status != "Completed"
    ]
    high_priority_tasks = [
        task
        for task in tasks
        if task.priority in {"High", "Critical"} and task.status != "Completed"
    ]
    upcoming_limit = today + timedelta(days=7)
    upcoming_tasks = [
        task
        for task in tasks
        if task.due_date
        and today < task.due_date <= upcoming_limit
        and task.status != "Completed"
    ]
    category_counts = Counter(task.category or "Other" for task in tasks)
    completion_percentage = (
        round((len(completed_today) / len(todays_tasks)) * 100) if todays_tasks else 0
    )

    return {
        "today_tasks": [_serialize_task(task) for task in todays_tasks],
        "completed_today": len(completed_today),
        "pending_today": len(pending_today),
        "completion_percentage": completion_percentage,
        "overdue_tasks": [_serialize_task(task) for task in overdue_tasks],
        "high_priority_tasks": [_serialize_task(task) for task in high_priority_tasks],
        "upcoming_tasks": [_serialize_task(task) for task in upcoming_tasks],
        "category_counts": dict(category_counts),
    }


def _is_today_task(task: Task, today: date) -> bool:
    if task.due_date == today:
        return True
    if task.completed_at and task.completed_at.date() == today:
        return True
    return task.created_at.date() == today


def _serialize_task(task: Task) -> dict:
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "category": task.category,
        "priority": task.priority,
        "status": task.status,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "estimated_minutes": task.estimated_minutes,
        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
    }
