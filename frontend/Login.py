"""Streamlit login page."""

import os
import re

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


def is_valid_email(email: str) -> bool:
    """Return whether an email address has a friendly valid shape."""
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return False

    top_level_domain = email.rsplit(".", maxsplit=1)[-1]
    return len(top_level_domain) >= 2


def login_error_message(response: requests.Response) -> str:
    """Translate backend login errors into friendly messages."""
    try:
        detail = response.json().get("detail")
    except ValueError:
        return "Login failed. Please try again."

    if isinstance(detail, str):
        if "invalid" in detail.lower():
            return "Invalid email or password."
        return detail

    return "Login failed. Please check your email and password."


def auth_headers() -> dict[str, str]:
    """Return authorization headers for authenticated API calls."""
    return {"Authorization": f"Bearer {st.session_state['access_token']}"}


def logout() -> None:
    """Clear the active login session."""
    st.session_state.pop("access_token", None)
    st.session_state.pop("current_user", None)
    st.session_state["redirect_to"] = "Login"
    st.success("You have been logged out.")


def load_current_user() -> None:
    """Load the authenticated user's profile."""
    try:
        response = requests.get(
            f"{API_URL}/auth/me",
            headers=auth_headers(),
            timeout=10,
        )
    except requests.RequestException:
        st.error("Could not connect to the backend.")
        return

    if response.ok:
        st.session_state["current_user"] = response.json()
    else:
        logout()
        st.error("Your session expired. Please log in again.")


st.title("Login")

if st.session_state.get("register_success"):
    st.success(st.session_state.pop("register_success"))

if st.session_state.get("access_token"):
    if not st.session_state.get("current_user"):
        load_current_user()

    user = st.session_state.get("current_user", {})
    st.success(f"Logged in as {user.get('email', 'current user')}.")
    if st.button("Logout"):
        logout()
        st.rerun()
    st.stop()

with st.form("login_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

if submitted:
    email = email.strip()

    if not email or not password:
        st.error("Please enter your email and password.")
    elif not is_valid_email(email):
        st.error("Please enter a valid email address.")
    else:
        try:
            response = requests.post(
                f"{API_URL}/auth/login",
                data={"username": email, "password": password},
                timeout=10,
            )
        except requests.RequestException:
            st.error("Could not connect to the backend.")
        else:
            if response.ok:
                token_data = response.json()
                st.session_state["access_token"] = token_data["access_token"]
                load_current_user()
                st.session_state["redirect_to"] = "Dashboard"
                st.success("Login successful.")
                st.rerun()
            else:
                st.error(login_error_message(response))
