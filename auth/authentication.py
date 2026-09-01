# ============================================================
# EXAMINA AI
# AUTHENTICATION SERVICE
# ============================================================

import streamlit as st

from services.supabase_client import get_supabase_client


def get_client():
    return get_supabase_client()


def login_user(email: str, password: str):
    """
    Authenticate a user through Supabase Auth.

    Passwords are never stored or logged by Examina.
    """

    email = email.strip().lower()

    if not email or not password:
        return False, "Email and password are required."

    try:
        supabase = get_client()

        response = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password,
            }
        )

        if not response.session or not response.user:
            return False, "Unable to authenticate."

        # Store only the authentication session required
        # for the current Streamlit session.
        st.session_state["auth_session"] = response.session
        st.session_state["auth_user"] = response.user

        return True, None

    except Exception:
        # Never expose Supabase/PostgreSQL/internal errors.
        return False, "Invalid email or password."


def logout_user():
    """
    End the current authenticated session.
    """

    try:
        supabase = get_client()
        supabase.auth.sign_out()
    except Exception:
        pass

    for key in (
        "auth_session",
        "auth_user",
        "user_profile",
        "supabase_ready",
    ):
        st.session_state.pop(key, None)


def is_authenticated() -> bool:
    """
    Determine whether the current Streamlit session
    contains an authenticated Supabase session.
    """

    return bool(
        st.session_state.get("auth_session")
        and st.session_state.get("auth_user")
    )
