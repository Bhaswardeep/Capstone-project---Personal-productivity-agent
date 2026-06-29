"""Streamlit registration page."""

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


def registration_error_message(response: requests.Response) -> str:
    """Translate backend registration errors into friendly messages."""
    try:
        detail = response.json().get("detail")
    except ValueError:
        return "Registration failed. Please try again."

    if isinstance(detail, str):
        normalized = detail.lower()
        if "username" in normalized and ("registered" in normalized or "exists" in normalized):
            return "Username already exists."
        if "email" in normalized and ("registered" in normalized or "exists" in normalized):
            return "Email already exists."
        return detail

    if isinstance(detail, list):
        for item in detail:
            location = item.get("loc", [])
            message = item.get("msg", "").lower()
            if "email" in location or "email" in message:
                return "Please enter a valid email address."
            if "password" in location:
                return "Please enter a password."
            if "username" in location:
                return "Please enter a username."

    return "Registration failed. Please check your information."


st.title("Register")

with st.form("register_form"):
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    submitted = st.form_submit_button("Create Account")

if submitted:
    username = username.strip()
    email = email.strip()

    if not username or not email or not password:
        st.error("Please complete all required fields.")
    elif not is_valid_email(email):
        st.error("Please enter a valid email address.")
    elif password != confirm_password:
        st.error("Passwords do not match.")
    else:
        try:
            response = requests.post(
                f"{API_URL}/auth/register",
                json={
                    "username": username,
                    "email": email,
                    "password": password,
                },
                timeout=10,
            )
        except requests.RequestException:
            st.error("Could not connect to the backend.")
        else:
            if response.ok:
                st.session_state["register_success"] = "Account created. Please log in."
                st.session_state["redirect_to"] = "Login"
                st.rerun()
            else:
                st.error(registration_error_message(response))
