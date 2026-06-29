"""Streamlit dashboard page."""

import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


def require_login() -> None:
    """Stop the page when the user is not authenticated."""
    if not st.session_state.get("access_token"):
        st.warning("Please log in to view the dashboard.")
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


def load_dashboard() -> dict | None:
    """Load dashboard statistics from the backend."""
    try:
        response = requests.get(
            f"{API_URL}/dashboard",
            headers=auth_headers(),
            timeout=10,
        )
    except requests.Timeout:
        st.error("The backend took too long to respond.")
        return None
    except requests.RequestException:
        st.error("Could not connect to the backend.")
        return None

    if response.ok:
        try:
            return response.json()
        except ValueError:
            st.error("The dashboard response was not valid.")
            return None

    st.error(friendly_api_error(response, "Could not load dashboard statistics."))
    return None


def task_title(task: dict) -> str:
    """Return a readable task title."""
    return task.get("title") or "Untitled task"


require_login()

st.title("Dashboard")

dashboard = load_dashboard()
if dashboard is None:
    st.stop()

today_tasks = dashboard.get("today_tasks", [])
pending_today = dashboard.get("pending_today", 0)
completed_today = dashboard.get("completed_today", 0)
completion_percentage = dashboard.get("completion_percentage", 0)
estimated_minutes = dashboard.get("total_estimated_minutes_today")
if estimated_minutes is None:
    estimated_minutes = sum(task.get("estimated_minutes") or 0 for task in today_tasks)

metric_col_1, metric_col_2, metric_col_3, metric_col_4 = st.columns(4)
metric_col_1.metric("Tasks Due Today", len(today_tasks))
metric_col_2.metric("Pending", pending_today)
metric_col_3.metric("Completed Today", completed_today)
metric_col_4.metric("Completion", f"{completion_percentage}%")

st.metric(
    "Total Estimated Minutes Today",
    estimated_minutes,
)

if not today_tasks:
    st.info("No tasks are due today.")
else:
    st.subheader("Tasks Due Today")
    st.dataframe(
        [
            {
                "Title": task_title(task),
                "Priority": task.get("priority", ""),
                "Status": task.get("status", ""),
                "Estimated Minutes": task.get("estimated_minutes") or "",
            }
            for task in today_tasks
        ],
        width="stretch",
        hide_index=True,
    )

with st.expander("Overdue Tasks", expanded=False):
    overdue_tasks = dashboard.get("overdue_tasks", [])
    if overdue_tasks:
        for task in overdue_tasks:
            st.write(f"- {task_title(task)}")
    else:
        st.write("No overdue tasks.")

with st.expander("High Priority Tasks", expanded=False):
    high_priority_tasks = dashboard.get("high_priority_tasks", [])
    if high_priority_tasks:
        for task in high_priority_tasks:
            st.write(f"- {task_title(task)}")
    else:
        st.write("No high priority tasks.")
