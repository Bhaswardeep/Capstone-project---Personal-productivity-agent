"""Streamlit task manager page."""

from datetime import date
import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
CATEGORIES = ["Work", "Learning", "Health", "Personal", "Other"]
PRIORITIES = ["Low", "Medium", "High", "Critical"]
STATUSES = ["Pending", "In Progress", "Completed", "Cancelled"]


def require_login() -> None:
    """Stop the page when the user is not authenticated."""
    if not st.session_state.get("access_token"):
        st.warning("Please log in to manage tasks.")
        st.stop()


def auth_headers() -> dict[str, str]:
    """Return authorization headers for API calls."""
    return {"Authorization": f"Bearer {st.session_state['access_token']}"}


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
    except requests.RequestException:
        st.error("Could not connect to the backend.")
        return None


def friendly_api_error(response: requests.Response, fallback: str) -> str:
    """Return a friendly message for an API error response."""
    try:
        detail = response.json().get("detail")
    except ValueError:
        return fallback

    if isinstance(detail, str):
        return detail

    if isinstance(detail, list):
        messages = []
        for item in detail:
            field = item.get("loc", ["field"])[-1]
            message = item.get("msg", "is invalid")
            messages.append(f"{field}: {message}")
        return "Please check: " + "; ".join(messages)

    return fallback


def load_tasks() -> list[dict]:
    """Load tasks for the authenticated user."""
    response = api_request("GET", "/tasks")
    if response is None:
        return []
    if response.ok:
        return response.json()

    st.error(friendly_api_error(response, "Could not load tasks."))
    return []


def schedule_create_form_reset() -> None:
    """Schedule task creation widgets to clear on the next rerun."""
    st.session_state["reset_create_form"] = True
    st.session_state["task_create_in_progress"] = False


def index_or_default(options: list[str], value: str, default: int = 0) -> int:
    """Return the option index or a fallback index."""
    return options.index(value) if value in options else default


require_login()

st.title("Tasks")

if st.session_state.pop("task_created", False):
    st.success("Task created.")
if st.session_state.pop("task_updated", False):
    st.success("Task updated.")
if st.session_state.pop("task_completed", False):
    st.success("Task completed.")
if st.session_state.pop("task_deleted", False):
    st.success("Task deleted.")

tasks = load_tasks()

if tasks:
    st.dataframe(
        [
            {
                "ID": task["id"],
                "Title": task["title"],
                "Priority": task["priority"],
                "Status": task["status"],
                "Due Date": task.get("due_date") or "",
                "Category": task["category"],
                "Estimated Minutes": task.get("estimated_minutes") or "",
            }
            for task in tasks
        ],
        width="stretch",
        hide_index=True,
    )
else:
    st.info("No tasks yet.")

st.subheader("Create Task")

if st.session_state.pop("reset_create_form", False):
    st.session_state["task_form_version"] = st.session_state.get("task_form_version", 0) + 1
    st.session_state["create_has_due_date"] = False

form_version = st.session_state.setdefault("task_form_version", 0)
has_due_date = st.checkbox("Add due date", key="create_has_due_date")
due_date_value = None
if has_due_date:
    due_date_value = st.date_input(
        "Due Date",
        value=date.today(),
        key=f"create_due_date_{form_version}",
    )

with st.form(f"create_task_form_{form_version}", clear_on_submit=False):
    title = st.text_input("Title", key=f"create_title_{form_version}")
    description = st.text_area("Description", key=f"create_description_{form_version}")
    priority = st.selectbox(
        "Priority",
        PRIORITIES,
        index=1,
        key=f"create_priority_{form_version}",
    )
    category = st.selectbox(
        "Category",
        CATEGORIES,
        index=4,
        key=f"create_category_{form_version}",
    )
    estimated_minutes = st.number_input(
        "Estimated Minutes",
        min_value=0,
        step=15,
        key=f"create_minutes_{form_version}",
    )
    create_submitted = st.form_submit_button(
        "Create Task",
        disabled=st.session_state.get("task_create_in_progress", False),
    )

if create_submitted:
    if st.session_state.get("task_create_in_progress", False):
        st.stop()

    if not title.strip():
        st.error("Task title is required.")
    else:
        st.session_state["task_create_in_progress"] = True
        payload = {
            "title": title.strip(),
            "description": description.strip() or None,
            "priority": priority,
            "category": category,
            "estimated_minutes": estimated_minutes or None,
            "due_date": due_date_value.isoformat() if due_date_value else None,
        }
        response = api_request("POST", "/tasks", json=payload)
        if response and response.ok:
            schedule_create_form_reset()
            st.session_state["task_created"] = True
            st.rerun()

        st.session_state["task_create_in_progress"] = False
        if response is not None:
            st.error(friendly_api_error(response, "Could not create task."))

if tasks:
    st.subheader("Task Details")
    task_options = {f"{task['id']} - {task['title']}": task for task in tasks}
    selected_label = st.selectbox("Choose Task", list(task_options.keys()))
    selected_task = task_options[selected_label]
    is_completed = selected_task["status"] == "Completed"

    if is_completed:
        st.info("This task is completed and is read-only.")
        st.write(f"Title: {selected_task['title']}")
        st.write(f"Description: {selected_task.get('description') or 'None'}")
        st.write(f"Priority: {selected_task['priority']}")
        st.write(f"Status: {selected_task['status']}")
        st.write(f"Category: {selected_task['category']}")
        st.write(f"Due Date: {selected_task.get('due_date') or 'None'}")
        st.write(f"Estimated Minutes: {selected_task.get('estimated_minutes') or 'None'}")
    else:
        with st.form(f"edit_task_form_{selected_task['id']}"):
            edit_title = st.text_input("Title", value=selected_task["title"])
            edit_description = st.text_area(
                "Description",
                value=selected_task.get("description") or "",
            )
            edit_priority = st.selectbox(
                "Priority",
                PRIORITIES,
                index=index_or_default(PRIORITIES, selected_task["priority"], 1),
            )
            edit_status = st.selectbox(
                "Status",
                STATUSES,
                index=index_or_default(STATUSES, selected_task["status"]),
            )
            edit_category = st.selectbox(
                "Category",
                CATEGORIES,
                index=index_or_default(CATEGORIES, selected_task["category"], 4),
            )
            edit_minutes = st.number_input(
                "Estimated Minutes",
                min_value=0,
                step=15,
                value=selected_task.get("estimated_minutes") or 0,
            )
            edit_has_due_date = st.checkbox(
                "Use due date",
                value=bool(selected_task.get("due_date")),
            )
            edit_due_date = (
                st.date_input(
                    "Due Date",
                    value=date.fromisoformat(selected_task["due_date"])
                    if selected_task.get("due_date")
                    else date.today(),
                )
                if edit_has_due_date
                else None
            )
            update_submitted = st.form_submit_button("Save Changes")

        if update_submitted:
            if not edit_title.strip():
                st.error("Task title is required.")
            else:
                payload = {
                    "title": edit_title.strip(),
                    "description": edit_description.strip() or None,
                    "priority": edit_priority,
                    "status": edit_status,
                    "category": edit_category,
                    "estimated_minutes": edit_minutes or None,
                    "due_date": edit_due_date.isoformat() if edit_due_date else None,
                }
                response = api_request("PUT", f"/tasks/{selected_task['id']}", json=payload)
                if response and response.ok:
                    st.session_state["task_updated"] = True
                    st.rerun()
                elif response is not None:
                    st.error(friendly_api_error(response, "Could not update task."))

    st.subheader("Task Actions")
    action_col_1, action_col_2 = st.columns(2)
    with action_col_1:
        if st.button("Mark Complete", disabled=is_completed):
            response = api_request("PATCH", f"/tasks/{selected_task['id']}/complete")
            if response and response.ok:
                st.session_state["task_completed"] = True
                st.rerun()
            elif response is not None:
                st.error(friendly_api_error(response, "Could not complete task."))
        if is_completed:
            st.caption("Already completed.")

    with action_col_2:
        pending_delete_id = st.session_state.get("pending_delete_task_id")
        if pending_delete_id == selected_task["id"]:
            st.warning("Delete this task? This cannot be undone.")
            if st.button("Confirm Delete"):
                response = api_request("DELETE", f"/tasks/{selected_task['id']}")
                if response and response.status_code == 204:
                    st.session_state.pop("pending_delete_task_id", None)
                    st.session_state["task_deleted"] = True
                    st.rerun()
                elif response is not None:
                    st.error(friendly_api_error(response, "Could not delete task."))

            if st.button("Cancel Delete"):
                st.session_state.pop("pending_delete_task_id", None)
                st.rerun()
        elif st.button("Delete Task"):
            st.session_state["pending_delete_task_id"] = selected_task["id"]
            st.rerun()
