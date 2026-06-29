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
    try:
        response = requests.post(
            f"{API_URL}/checkin/evening",
            headers=auth_headers(),
            json={
                "evening_notes": evening_notes or None,
                "wins": wins or None,
                "challenges": challenges or None,
            },
            timeout=10,
        )
    except requests.RequestException:
        st.error("Could not connect to the backend.")
    else:
        if response.ok:
            st.success("Evening check-in saved.")
            st.rerun()
        else:
            st.error(response.json().get("detail", "Could not save check-in."))
