"""Streamlit morning check-in page."""

import os

import requests
import streamlit as st

# API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
API_URL = os.getenv(
    "API_URL",
    "https://personal-productivity-agent-with-groq-ai.onrender.com",
)


def require_login() -> None:
    """Stop the page when the user is not authenticated."""
    if not st.session_state.get("access_token"):
        st.warning("Please log in to use morning check-in.")
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
    """Load tasks for AI planning."""
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


def generate_morning_ai(tasks: list[dict], notes: str | None) -> dict | None:
    """Call the morning AI planning endpoint."""
    if not tasks:
        st.info("Create at least one task before generating a morning AI plan.")
        return None

    response = api_request(
        "POST",
        "/ai/morning-plan",
        json={"today_tasks": tasks, "morning_notes": notes},
    )
    if response is None:
        return None
    if response.ok:
        try:
            return response.json()
        except ValueError:
            st.error("The AI response was not valid.")
            return None

    st.error(friendly_api_error(response, "Could not generate morning plan."))
    return None


def render_morning_ai(ai_result: dict) -> None:
    """Display morning AI output."""
    st.subheader("AI Morning Plan")
    st.write("Estimated focus:", ai_result.get("estimated_focus", "Not available"))

    with st.expander("Prioritized Plan", expanded=True):
        for item in ai_result.get("prioritized_plan", []):
            st.write(f"- {item}")

    with st.expander("Suggested Order", expanded=True):
        for index, item in enumerate(ai_result.get("suggested_order", []), start=1):
            st.write(f"{index}. {item}")

    with st.expander("Classified Priorities", expanded=False):
        classifications = ai_result.get("classifications", [])
        if classifications:
            st.dataframe(classifications, width="stretch", hide_index=True)
        else:
            st.write("No classifications returned.")

    motivational_advice = ai_result.get("motivational_advice")
    if motivational_advice:
        st.write("Motivational advice:", motivational_advice)

    provider = ai_result.get("provider")
    if provider:
        st.write(f"AI Provider: {provider.upper()}")


require_login()

st.title("Morning Check-In")

today_log = load_today_log()
existing_notes = today_log.get("morning_notes") if today_log else ""

with st.form("morning_checkin_form"):
    morning_notes = st.text_area(
        "Morning Plan",
        value=existing_notes or "",
        height=180,
    )
    submitted = st.form_submit_button("Save Morning Check-In")

if submitted:
    response = api_request(
        "POST",
        "/checkin/morning",
        json={"morning_notes": morning_notes or None},
    )
    if response and response.ok:
        st.success("Morning check-in saved.")
        tasks = load_tasks()
        st.session_state["morning_ai_result"] = generate_morning_ai(
            tasks,
            morning_notes or None,
        )
    elif response is not None:
        st.error(friendly_api_error(response, "Could not save check-in."))

if st.session_state.get("morning_ai_result"):
    render_morning_ai(st.session_state["morning_ai_result"])
