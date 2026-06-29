"""Streamlit morning check-in page."""

import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


def require_login() -> None:
    """Stop the page when the user is not authenticated."""
    if not st.session_state.get("access_token"):
        st.warning("Please log in to use morning check-in.")
        st.stop()


def auth_headers() -> dict[str, str]:
    """Return authorization headers for API calls."""
    return {"Authorization": f"Bearer {st.session_state['access_token']}"}


def load_today_log() -> dict | None:
    """Load today's daily log."""
    try:
        response = requests.get(
            f"{API_URL}/checkin/morning",
            headers=auth_headers(),
            timeout=10,
        )
    except requests.RequestException:
        st.error("Could not connect to the backend.")
        return None

    if response.ok:
        return response.json()

    st.error(response.json().get("detail", "Could not load today's check-in."))
    return None


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
    try:
        response = requests.post(
            f"{API_URL}/checkin/morning",
            headers=auth_headers(),
            json={"morning_notes": morning_notes or None},
            timeout=10,
        )
    except requests.RequestException:
        st.error("Could not connect to the backend.")
    else:
        if response.ok:
            st.success("Morning check-in saved.")
            st.rerun()
        else:
            st.error(response.json().get("detail", "Could not save check-in."))
