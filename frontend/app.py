"""Streamlit application entry point and navigation shell."""

from pathlib import Path
import runpy

import streamlit as st

APP_DIR = Path(__file__).parent

PUBLIC_PAGES = {
    "Login": "Login.py",
    "Register": "Register.py",
}

PROTECTED_PAGES = {
    "Tasks": "Tasks.py",
    "Morning Check-In": "Morning_Checkin.py",
    "Evening Check-In": "Evening_Checkin.py",
}


def logout() -> None:
    """Clear authentication state and return to the login page."""
    st.session_state.pop("access_token", None)
    st.session_state.pop("current_user", None)
    st.session_state["redirect_to"] = "Login"


def apply_pending_redirect() -> None:
    """Apply page redirects before sidebar widgets are created."""
    target_page = st.session_state.pop("redirect_to", None)
    if target_page is None:
        return

    st.session_state["nav_page"] = target_page

    if target_page in PUBLIC_PAGES:
        st.session_state["public_nav"] = target_page
        st.session_state.pop("protected_nav", None)

    if target_page in PROTECTED_PAGES:
        st.session_state["protected_nav"] = target_page
        st.session_state.pop("public_nav", None)


def render_page(page_file: str) -> None:
    """Run a page file inside the shared Streamlit app shell."""
    runpy.run_path(str(APP_DIR / page_file), run_name="__main__")


def select_public_page() -> str:
    """Render navigation for unauthenticated users."""
    st.session_state.setdefault("nav_page", "Login")
    if st.session_state["nav_page"] not in PUBLIC_PAGES:
        st.session_state["nav_page"] = "Login"
    if st.session_state.get("public_nav") not in PUBLIC_PAGES:
        st.session_state["public_nav"] = st.session_state["nav_page"]

    selected_page = st.sidebar.radio(
        "Navigation",
        list(PUBLIC_PAGES.keys()),
        index=list(PUBLIC_PAGES.keys()).index(st.session_state["public_nav"]),
        key="public_nav",
    )
    st.session_state["nav_page"] = selected_page
    return selected_page


def select_protected_page() -> str:
    """Render navigation for authenticated users."""
    if st.session_state.get("nav_page") not in PROTECTED_PAGES:
        st.session_state["nav_page"] = "Tasks"
    if st.session_state.get("protected_nav") not in PROTECTED_PAGES:
        st.session_state["protected_nav"] = st.session_state["nav_page"]

    selected_page = st.sidebar.radio(
        "Navigation",
        list(PROTECTED_PAGES.keys()),
        index=list(PROTECTED_PAGES.keys()).index(st.session_state["protected_nav"]),
        key="protected_nav",
    )
    st.session_state["nav_page"] = selected_page

    if st.sidebar.button("Logout", width="stretch", key="logout_button"):
        logout()
        st.rerun()

    return selected_page


st.set_page_config(page_title="Personal Productivity Agent")
apply_pending_redirect()
st.sidebar.title("Personal Productivity Agent")

if st.session_state.get("access_token"):
    page_name = select_protected_page()
    render_page(PROTECTED_PAGES[page_name])
else:
    page_name = select_public_page()
    render_page(PUBLIC_PAGES[page_name])
