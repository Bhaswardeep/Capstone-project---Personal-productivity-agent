"""Reusable LangGraph nodes for productivity AI workflows."""

from __future__ import annotations

from collections import Counter
from datetime import date

from backend.langgraph.state import ClassificationState, ProductivityGraphState, TaskState

PRIORITY_WEIGHT = {
    "Critical": 0,
    "High": 1,
    "Medium": 2,
    "Low": 3,
    None: 4,
}


def classify_tasks(state: ProductivityGraphState) -> ProductivityGraphState:
    """Classify tasks with deterministic rules suitable for mock AI mode."""
    tasks = _all_tasks(state)
    classifications: list[ClassificationState] = []

    for task in tasks:
        category = task.get("category") or _infer_category(task.get("title", ""))
        priority = task.get("priority") or "Medium"
        urgency = _infer_urgency(task)
        classifications.append(
            {
                "title": task.get("title", "Untitled task"),
                "category": category,
                "priority": priority,
                "urgency": urgency,
            }
        )

    return {"classifications": classifications}


def analyze_overdue_tasks(state: ProductivityGraphState) -> ProductivityGraphState:
    """Detect overdue incomplete tasks."""
    today = date.today()
    overdue_tasks: list[TaskState] = []

    for task in _all_tasks(state):
        due_date = _parse_date(task.get("due_date"))
        status = task.get("status") or "Pending"
        if due_date and due_date < today and status != "Completed":
            overdue_tasks.append(task)

    return {"overdue_tasks": overdue_tasks}


def generate_summary(state: ProductivityGraphState) -> ProductivityGraphState:
    """Generate morning, evening, or weekly summary fields."""
    workflow = state.get("workflow")

    if workflow == "morning":
        return _generate_morning_plan(state)

    if workflow == "weekly":
        return _generate_weekly_review(state)

    return _generate_evening_summary(state)


def plan_tomorrow(state: ProductivityGraphState) -> ProductivityGraphState:
    """Generate tomorrow recommendations from pending and overdue work."""
    pending_tasks = state.get("pending_tasks", [])
    overdue_tasks = state.get("overdue_tasks", [])
    candidate_tasks = _sort_tasks(overdue_tasks + pending_tasks)

    recommendations = [
        f"Start with {task.get('title', 'the highest priority task')}."
        for task in candidate_tasks[:3]
    ]
    if not recommendations:
        recommendations = ["Use tomorrow to protect focus time and plan the next meaningful task."]

    if state.get("workflow") == "morning":
        return {}

    return {
        "tomorrow_recommendations": recommendations,
        "encouragement": "Close the day cleanly and begin tomorrow with the smallest clear next step.",
    }


def _generate_morning_plan(state: ProductivityGraphState) -> ProductivityGraphState:
    tasks = _sort_tasks(state.get("today_tasks", []))
    task_titles = [task.get("title", "Untitled task") for task in tasks]
    total_minutes = sum(task.get("estimated_minutes") or 0 for task in tasks)

    if total_minutes:
        estimated_focus = f"Plan for about {total_minutes} minutes of focused work."
    else:
        estimated_focus = "Plan for two focused work blocks and adjust after the first task."

    return {
        "prioritized_plan": task_titles[:5],
        "suggested_order": task_titles,
        "estimated_focus": estimated_focus,
        "motivational_advice": _morning_advice(tasks, state.get("morning_notes")),
    }


def _generate_evening_summary(state: ProductivityGraphState) -> ProductivityGraphState:
    completed = state.get("completed_tasks", [])
    pending = state.get("pending_tasks", [])
    notes = state.get("evening_notes")

    summary = (
        f"You completed {len(completed)} task(s) and have {len(pending)} task(s) still pending."
    )
    if notes:
        summary = f"{summary} Your reflection notes mention: {notes}"

    achievements = [task.get("title", "Completed task") for task in completed[:5]]
    if not achievements:
        achievements = ["You completed the reflection loop and kept your task list honest."]

    return {
        "daily_summary": summary,
        "achievements": achievements,
    }


def _generate_weekly_review(state: ProductivityGraphState) -> ProductivityGraphState:
    completed = state.get("completed_tasks", [])
    missed = state.get("missed_tasks", [])
    all_tasks = completed + missed + state.get("pending_tasks", [])
    total_tasks = len(completed) + len(missed)
    score = round((len(completed) / total_tasks) * 100) if total_tasks else 0
    category_counts = state.get("metadata", {}).get("category_counts", {})
    categories = Counter(category_counts)
    if not categories:
        categories = Counter(task.get("category") or "Other" for task in all_tasks)
    common_categories = [category for category, _count in categories.most_common(3)]

    strengths = ["Consistent task completion"] if completed else ["Awareness of weekly workload"]
    if common_categories:
        strengths.append(f"Clear activity around {', '.join(common_categories)}")

    weaknesses = []
    if missed:
        weaknesses.append("Some planned tasks slipped and need earlier follow-up.")
    if not completed:
        weaknesses.append("Completion data is limited for this week.")
    if not weaknesses:
        weaknesses.append("No major weakness detected from the available task data.")

    patterns = _weekly_patterns(state, categories)
    recommendations = [
        "Move unfinished high-priority work into the next morning plan.",
        "Keep daily notes short but specific so weekly reviews become more useful.",
        "Limit each day to a realistic number of high-focus tasks.",
    ]

    return {
        "productivity_score": score,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recurring_patterns": patterns,
        "recommendations": recommendations,
        "weekly_summary": (
            f"Weekly mock review: {len(completed)} completed task(s), "
            f"{len(missed)} missed task(s), productivity score {score}%."
        ),
    }


def _all_tasks(state: ProductivityGraphState) -> list[TaskState]:
    return (
        state.get("today_tasks", [])
        + state.get("completed_tasks", [])
        + state.get("pending_tasks", [])
        + state.get("missed_tasks", [])
    )


def _sort_tasks(tasks: list[TaskState]) -> list[TaskState]:
    return sorted(
        tasks,
        key=lambda task: (
            PRIORITY_WEIGHT.get(task.get("priority"), 4),
            task.get("due_date") or "9999-12-31",
            task.get("title") or "",
        ),
    )


def _infer_category(title: str) -> str:
    title_lower = title.lower()
    if any(word in title_lower for word in ("study", "learn", "course", "read")):
        return "Learning"
    if any(word in title_lower for word in ("work", "project", "meeting", "client")):
        return "Work"
    if any(word in title_lower for word in ("gym", "walk", "health", "doctor")):
        return "Health"
    if any(word in title_lower for word in ("home", "family", "errand", "personal")):
        return "Personal"
    return "Other"


def _infer_urgency(task: TaskState) -> str:
    due_date = _parse_date(task.get("due_date"))
    priority = task.get("priority")

    if priority == "Critical":
        return "Critical"
    if due_date and due_date <= date.today():
        return "High"
    if priority == "High":
        return "High"
    if priority == "Low":
        return "Low"
    return "Medium"


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _morning_advice(tasks: list[TaskState], notes: str | None) -> str:
    if not tasks:
        return "Start by choosing one concrete task that would make today feel successful."
    first_task = tasks[0].get("title", "your top priority")
    if notes:
        return f"Use your notes as context, then protect the first block for {first_task}."
    return f"Begin with {first_task}, then reassess before adding more work."


def _weekly_patterns(state: ProductivityGraphState, categories: Counter[str]) -> list[str]:
    patterns: list[str] = []
    if categories:
        category, count = categories.most_common(1)[0]
        patterns.append(f"Most task activity was in {category} ({count} task(s)).")
    if state.get("daily_logs"):
        patterns.append("Daily logs are available for reflection context.")
    if state.get("missed_tasks"):
        patterns.append("Some tasks carried across the week without completion.")
    if not patterns:
        patterns.append("Not enough history yet to identify strong recurring patterns.")
    return patterns
