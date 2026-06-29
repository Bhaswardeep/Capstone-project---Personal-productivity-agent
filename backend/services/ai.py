"""AI service abstraction for productivity planning and reviews."""

from __future__ import annotations

import json
import logging
import os
from datetime import date, datetime
from typing import Any

from dotenv import load_dotenv

from backend.langgraph.graph import get_productivity_graph
from backend.langgraph.state import DailyLogState, ProductivityGraphState, TaskState
from backend.models.models import DailyLog, Task

load_dotenv()

logger = logging.getLogger(__name__)

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
GROQ_TIMEOUT_SECONDS = float(os.getenv("GROQ_TIMEOUT_SECONDS", "15"))


def generate_morning_plan(
    today_tasks: list[dict[str, Any] | Task],
    morning_notes: str | None = None,
    user_id: int | None = None,
) -> dict[str, Any]:
    """Generate a prioritized morning plan."""
    serialized_tasks = [_serialize_task(task) for task in today_tasks]
    groq_result = _generate_groq_morning_plan(serialized_tasks, morning_notes)
    if groq_result is not None:
        return groq_result

    state: ProductivityGraphState = {
        "user_id": user_id or 0,
        "workflow": "morning",
        "today_tasks": serialized_tasks,
        "morning_notes": morning_notes,
        "metadata": _provider_metadata("mock"),
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
    wins: str | None = None,
    challenges: str | None = None,
    user_id: int | None = None,
) -> dict[str, Any]:
    """Generate an evening reflection and tomorrow recommendations."""
    serialized_completed = [_serialize_task(task) for task in completed_tasks]
    serialized_pending = [_serialize_task(task) for task in pending_tasks]
    groq_result = _generate_groq_evening_summary(
        serialized_completed,
        serialized_pending,
        evening_notes,
        wins,
        challenges,
    )
    if groq_result is not None:
        return groq_result

    state: ProductivityGraphState = {
        "user_id": user_id or 0,
        "workflow": "evening",
        "completed_tasks": serialized_completed,
        "pending_tasks": serialized_pending,
        "evening_notes": evening_notes,
        "wins": wins,
        "challenges": challenges,
        "metadata": _provider_metadata("mock"),
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
    serialized_completed = [_serialize_task(task) for task in completed_tasks]
    serialized_missed = [_serialize_task(task) for task in missed_tasks]
    serialized_logs = [_serialize_daily_log(log) for log in daily_logs or []]
    groq_result = _generate_groq_weekly_review(
        serialized_completed,
        serialized_missed,
        categories or {},
        serialized_logs,
    )
    if groq_result is not None:
        return groq_result

    state: ProductivityGraphState = {
        "user_id": user_id or 0,
        "workflow": "weekly",
        "completed_tasks": serialized_completed,
        "missed_tasks": serialized_missed,
        "daily_logs": serialized_logs,
        "metadata": {
            **_provider_metadata("mock"),
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


def _provider_metadata(provider: str) -> dict[str, Any]:
    """Return provider configuration without exposing secrets."""
    return {
        "provider": provider,
        "mock": provider == "mock",
    }


def _generate_groq_morning_plan(
    today_tasks: list[TaskState],
    morning_notes: str | None,
) -> dict[str, Any] | None:
    prompt = _json_prompt(
        workflow="morning planning",
        schema={
            "prioritized_plan": ["task title"],
            "suggested_order": ["task title"],
            "estimated_focus": "short focus estimate",
            "motivational_advice": "one concise sentence",
            "classifications": [
                {
                    "title": "task title",
                    "category": "Work|Learning|Health|Personal|Other",
                    "priority": "Low|Medium|High|Critical",
                    "urgency": "Low|Medium|High|Critical",
                }
            ],
        },
        context={
            "today_tasks": today_tasks,
            "morning_notes": morning_notes,
        },
    )
    result = _invoke_groq_json(prompt)
    if result is None:
        return None

    return {
        "prioritized_plan": _string_list(result.get("prioritized_plan")),
        "suggested_order": _string_list(result.get("suggested_order")),
        "estimated_focus": str(result.get("estimated_focus") or ""),
        "motivational_advice": str(result.get("motivational_advice") or ""),
        "classifications": _classification_list(result.get("classifications")),
        "provider": "groq",
    }


def _generate_groq_evening_summary(
    completed_tasks: list[TaskState],
    pending_tasks: list[TaskState],
    evening_notes: str | None,
    wins: str | None,
    challenges: str | None,
) -> dict[str, Any] | None:
    prompt = _json_prompt(
        workflow="evening productivity summary",
        schema={
            "daily_summary": "short paragraph",
            "achievements": ["completed achievement"],
            "tomorrow_recommendations": ["specific recommendation"],
            "encouragement": "one concise sentence",
        },
        context={
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "evening_notes": evening_notes,
            "wins": wins,
            "challenges": challenges,
        },
    )
    result = _invoke_groq_json(prompt)
    if result is None:
        return None

    overdue_tasks = [
        task for task in pending_tasks if _is_overdue(task)
    ]
    return {
        "daily_summary": str(result.get("daily_summary") or ""),
        "achievements": _string_list(result.get("achievements")),
        "tomorrow_recommendations": _string_list(result.get("tomorrow_recommendations")),
        "encouragement": str(result.get("encouragement") or ""),
        "overdue_tasks": overdue_tasks,
        "provider": "groq",
    }


def _generate_groq_weekly_review(
    completed_tasks: list[TaskState],
    missed_tasks: list[TaskState],
    categories: dict[str, int],
    daily_logs: list[DailyLogState],
) -> dict[str, Any] | None:
    prompt = _json_prompt(
        workflow="weekly productivity review",
        schema={
            "productivity_score": "integer from 0 to 100",
            "strengths": ["strength"],
            "weaknesses": ["weakness"],
            "recurring_patterns": ["pattern"],
            "recommendations": ["recommendation"],
            "weekly_summary": "short paragraph",
        },
        context={
            "completed_tasks": completed_tasks,
            "missed_tasks": missed_tasks,
            "category_counts": categories,
            "daily_logs": daily_logs,
        },
    )
    result = _invoke_groq_json(prompt)
    if result is None:
        return None

    return {
        "productivity_score": _score(result.get("productivity_score")),
        "strengths": _string_list(result.get("strengths")),
        "weaknesses": _string_list(result.get("weaknesses")),
        "recurring_patterns": _string_list(result.get("recurring_patterns")),
        "recommendations": _string_list(result.get("recommendations")),
        "weekly_summary": str(result.get("weekly_summary") or ""),
        "provider": "groq",
    }


def _invoke_groq_json(prompt: str) -> dict[str, Any] | None:
    """Call Groq through LangChain and return parsed JSON, or None on fallback."""
    if not os.getenv("GROQ_API_KEY"):
        return None

    try:
        from langchain_groq import ChatGroq
    except ImportError:
        logger.warning("Groq provider unavailable because langchain-groq is not installed.")
        return None

    try:
        llm = ChatGroq(
            model=GROQ_MODEL,
            temperature=0.2,
            max_retries=0,
            request_timeout=GROQ_TIMEOUT_SECONDS,
        )
        response = llm.invoke(prompt)
        content = getattr(response, "content", "")
        parsed = _parse_json_object(str(content))
    except Exception as exc:  # pragma: no cover - network/provider dependent
        logger.warning("Groq request failed; using mock AI provider. Error: %s", exc.__class__.__name__)
        return None

    if parsed is None:
        logger.warning("Groq returned a non-JSON response; using mock AI provider.")
        return None

    return parsed


def _json_prompt(workflow: str, schema: dict[str, Any], context: dict[str, Any]) -> str:
    """Build a strict JSON prompt for hosted LLM calls."""
    return (
        "You are a concise productivity assistant. "
        "Return only valid JSON with no markdown, comments, or extra text. "
        "Preserve the requested key names and use short, useful strings.\n\n"
        f"Workflow: {workflow}\n"
        f"Required JSON shape: {json.dumps(schema, ensure_ascii=True)}\n"
        f"Context: {json.dumps(context, ensure_ascii=True, default=str)}"
    )


def _parse_json_object(content: str) -> dict[str, Any] | None:
    """Parse a JSON object from an LLM response."""
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        start = content.find("{")
        end = content.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return None
        try:
            parsed = json.loads(content[start : end + 1])
        except json.JSONDecodeError:
            return None

    return parsed if isinstance(parsed, dict) else None


def _string_list(value: Any) -> list[str]:
    """Normalize model output to a list of strings."""
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item is not None]


def _classification_list(value: Any) -> list[dict[str, str]]:
    """Normalize task classifications to the existing response shape."""
    if not isinstance(value, list):
        return []

    classifications: list[dict[str, str]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        classifications.append(
            {
                "title": str(item.get("title") or "Untitled task"),
                "category": str(item.get("category") or "Other"),
                "priority": str(item.get("priority") or "Medium"),
                "urgency": str(item.get("urgency") or "Medium"),
            }
        )
    return classifications


def _score(value: Any) -> int:
    """Normalize a model score to the expected 0-100 integer range."""
    try:
        score = int(value)
    except (TypeError, ValueError):
        return 0
    return max(0, min(100, score))


def _is_overdue(task: TaskState) -> bool:
    due_date = _serialize_date(task.get("due_date"))
    status = task.get("status") or "Pending"
    if status == "Completed" or not due_date:
        return False
    try:
        return date.fromisoformat(due_date) < date.today()
    except ValueError:
        return False


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
