"""Streamlit evening check-in page."""

import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


def require_login() -> None:
    """Stop the page when the user is not authenticated."""
    if not st.session_state.get("access_token"):
        st.warning("Please log in to use evening check-in.")
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


def load_today_log() -> dict | None:
    """Load today's daily log."""
    response = api_request("GET", "/checkin/morning")
    if response is None:
        return None

    if response.ok:
        return response.json()

    st.error(response.json().get("detail", "Could not load today's check-in."))
    return None


def load_tasks() -> list[dict]:
    """Load tasks for evening AI summary."""
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


def generate_evening_ai(
    tasks: list[dict],
    notes: str | None,
    wins: str | None,
    challenges: str | None,
) -> dict | None:
    """Call the evening AI summary endpoint."""
    completed_tasks = [task for task in tasks if task.get("status") == "Completed"]
    pending_tasks = [task for task in tasks if task.get("status") != "Completed"]

    if not completed_tasks and not pending_tasks:
        st.info("Create at least one task before generating an evening AI summary.")
        return None

    response = api_request(
        "POST",
        "/ai/evening-summary",
        json={
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "evening_notes": notes,
            "wins": wins,
            "challenges": challenges,
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

    st.error(friendly_api_error(response, "Could not generate evening summary."))
    return None


def render_evening_ai(ai_result: dict) -> None:
    """Display evening AI output."""
    st.subheader("AI Evening Summary")
    st.write(ai_result.get("daily_summary", "No summary returned."))

    with st.expander("Achievements", expanded=True):
        for item in ai_result.get("achievements", []):
            st.write(f"- {item}")

    with st.expander("Tomorrow Recommendations", expanded=True):
        for item in ai_result.get("tomorrow_recommendations", []):
            st.write(f"- {item}")

    st.write(ai_result.get("encouragement", ""))

    provider = ai_result.get("provider")
    if provider:
        st.write(f"AI Provider: {provider.upper()}")


require_login()

st.title("Evening Check-In")

today_log = load_today_log()
existing_evening_notes = today_log.get("evening_notes") if today_log else ""
existing_wins = today_log.get("wins") if today_log else ""
existing_challenges = today_log.get("challenges") if today_log else ""

with st.form("evening_checkin_form"):
    evening_notes = st.text_area(
        "Evening Notes",
        value=existing_evening_notes or "",
        height=140,
    )
    wins = st.text_area("Wins", value=existing_wins or "", height=120)
    challenges = st.text_area(
        "Challenges",
        value=existing_challenges or "",
        height=120,
    )
    submitted = st.form_submit_button("Save Evening Check-In")

if submitted:
    response = api_request(
        "POST",
        "/checkin/evening",
        json={
            "evening_notes": evening_notes or None,
            "wins": wins or None,
            "challenges": challenges or None,
        },
    )
    if response and response.ok:
        st.success("Evening check-in saved.")
        tasks = load_tasks()
        st.session_state["evening_ai_result"] = generate_evening_ai(
            tasks,
            evening_notes or None,
            wins or None,
            challenges or None,
        )
    elif response is not None:
        st.error(friendly_api_error(response, "Could not save check-in."))

if st.session_state.get("evening_ai_result"):
    render_evening_ai(st.session_state["evening_ai_result"])
