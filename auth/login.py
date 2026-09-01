# ============================================================
# EXAMINA AI
# LOGIN
# ============================================================

import streamlit as st

from auth.authentication import login_user
from database.supabase_client import get_supabase_client


# ============================================================
# SHOW LOGIN
# ============================================================

def show_login():

    st.title("Welcome back")

    st.write(
        "Sign in to access your Examina AI workspace."
    )

    st.write("")


    with st.form("login_form"):

        email = st.text_input(
            "Email address"
        )

        password = st.text_input(
            "Password",
            type="password",
        )

        submitted = st.form_submit_button(
            "Sign in",
            use_container_width=True,
        )


    if submitted:

        if not email.strip():

            st.error(
                "Please enter your email address."
            )

            return


        if not password:

            st.error(
                "Please enter your password."
            )

            return


        try:

            supabase = get_supabase_client()

            response = (
                supabase.auth.sign_in_with_password(
                    {
                        "email": email.strip(),
                        "password": password,
                    }
                )
            )

            if not response.user:

                st.error(
                    "Unable to sign in."
                )

                return


            login_user(
                {
                    "id": response.user.id,
                    "email": response.user.email,
                }
            )

            st.session_state["page"] = "dashboard"

            st.rerun()


        except Exception as error:

            st.error(
                f"Login failed: {error}"
            )


    st.write("")


    if st.button(
        "← Back to home",
        use_container_width=True,
    ):

        st.session_state["page"] = "home"

        st.rerun()
