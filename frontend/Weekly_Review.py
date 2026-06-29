"""Streamlit weekly review page."""

from collections import Counter
import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


def require_login() -> None:
    """Stop the page when the user is not authenticated."""
    if not st.session_state.get("access_token"):
        st.warning("Please log in to view your weekly review.")
        st.stop()


def auth_headers() -> dict[str, str]:
    """Return authorization headers for API calls."""
    return {"Authorization": f"Bearer {st.session_state['access_token']}"}


def friendly_api_error(response: requests.Response, fallback: str) -> str:
    """Return a friendly message for an API error response."""
    if response.status_code == 401:
        return "Your session expired. Please log in again."

    try:
        detail = response.json().get("detail")
    except ValueError:
        return fallback

    return detail if isinstance(detail, str) else fallback


def api_request(method: str, path: str, **kwargs) -> requests.Response | None:
    """Call the backend API and handle connection errors."""
    try:
        return requests.request(
            method,
            f"{API_URL}{path}",
            headers=auth_headers(),
            timeout=10,
            **kwargs,
        )
    except requests.Timeout:
        st.error("The backend took too long to respond.")
        return None
    except requests.RequestException:
        st.error("Could not connect to the backend.")
        return None


def load_tasks() -> list[dict]:
    """Load tasks for weekly review."""
    response = api_request("GET", "/tasks")
    if response is None:
        return []
    if response.ok:
        try:
            return response.json()
        except ValueError:
            st.error("The task response was not valid.")
            return []

    st.error(friendly_api_error(response, "Could not load tasks."))
    return []


def generate_weekly_ai(tasks: list[dict]) -> dict | None:
    """Call the weekly review AI endpoint."""
    if not tasks:
        st.info("Create tasks before generating a weekly review.")
        return None

    completed_tasks = [task for task in tasks if task.get("status") == "Completed"]
    missed_tasks = [task for task in tasks if task.get("status") != "Completed"]
    categories = Counter(task.get("category") or "Other" for task in tasks)
    response = api_request(
        "POST",
        "/ai/weekly-review",
        json={
            "completed_tasks": completed_tasks,
            "missed_tasks": missed_tasks,
            "categories": dict(categories),
            "daily_logs": [],
        },
    )
    if response is None:
        return None
    if response.ok:
        try:
            return response.json()
        except ValueError:
            st.error("The AI response was not valid.")
            return None

    st.error(friendly_api_error(response, "Could not generate weekly review."))
    return None


def render_list(title: str, items: list[str]) -> None:
    """Render a titled list in an expander."""
    with st.expander(title, expanded=True):
        if items:
            for item in items:
                st.write(f"- {item}")
        else:
            st.write("No items returned.")


def render_weekly_ai(ai_result: dict, tasks: list[dict]) -> None:
    """Display weekly AI output."""
    st.subheader("Weekly Summary")
    st.write(ai_result.get("weekly_summary", "No weekly summary returned."))

    score = ai_result.get("productivity_score")
    if score is not None:
        st.metric("Productivity Score", f"{score}%")

    render_list("Strengths", ai_result.get("strengths", []))
    render_list("Weaknesses", ai_result.get("weaknesses", []))
    render_list("Suggested Improvements", ai_result.get("recommendations", []))
    render_list("Productivity Insights", ai_result.get("recurring_patterns", []))

    with st.expander("Category Analysis", expanded=True):
        categories = Counter(task.get("category") or "Other" for task in tasks)
        if categories:
            st.dataframe(
                [
                    {"Category": category, "Tasks": count}
                    for category, count in categories.items()
                ],
                width="stretch",
                hide_index=True,
            )
        else:
            st.write("No category data available.")

    provider = ai_result.get("provider")
    if provider:
        st.write(f"AI Provider: {provider.upper()}")


require_login()

st.title("Weekly Review")

tasks = load_tasks()
if tasks:
    st.caption(f"{len(tasks)} task(s) loaded for review.")
else:
    st.info("No tasks are available for weekly review yet.")

if st.button("Generate Weekly Review", disabled=not tasks):
    st.session_state["weekly_ai_result"] = generate_weekly_ai(tasks)

if st.session_state.get("weekly_ai_result"):
    render_weekly_ai(st.session_state["weekly_ai_result"], tasks)
