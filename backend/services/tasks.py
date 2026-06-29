"""Task and daily log service functions."""

from datetime import date, datetime, timezone

from sqlalchemy.orm import Session

from backend.models.models import DailyLog, Task


def create_task(db: Session, user_id: int, task_data: dict) -> Task:
    """Create a task owned by the authenticated user."""
    task = Task(user_id=user_id, **task_data)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_user_tasks(db: Session, user_id: int) -> list[Task]:
    """Return all tasks owned by a user."""
    return (
        db.query(Task)
        .filter(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
        .all()
    )


def get_user_task(db: Session, user_id: int, task_id: int) -> Task | None:
    """Return one task if it belongs to the user."""
    return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()


def update_task(db: Session, task: Task, task_data: dict) -> Task:
    """Update an existing task."""
    for field, value in task_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    """Delete an existing task."""
    db.delete(task)
    db.commit()


def complete_task(db: Session, task: Task) -> Task:
    """Mark a task as completed."""
    task.status = "Completed"
    task.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(task)
    return task


def get_today_log(db: Session, user_id: int) -> DailyLog | None:
    """Return today's daily log for a user."""
    return (
        db.query(DailyLog)
        .filter(DailyLog.user_id == user_id, DailyLog.date == date.today())
        .first()
    )


def upsert_today_log(db: Session, user_id: int, log_data: dict) -> DailyLog:
    """Create or update today's daily log for a user."""
    log = get_today_log(db, user_id)
    if log is None:
        log = DailyLog(user_id=user_id, date=date.today())
        db.add(log)

    for field, value in log_data.items():
        setattr(log, field, value)

    db.commit()
    db.refresh(log)
    return log
