# ============================================================
# EXAMINA AI
# ADMIN LOGIN
# ============================================================

import streamlit as st

from database.auth import (
    login_user,
    get_admin_profile,
)


def show_admin_login():

    st.title("Examina AI")
    st.subheader("Admin Portal")

    st.caption(
        "Authorized administrators only."
    )

    email = st.text_input(
        "Admin Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(
        "Login to Admin Portal",
        type="primary",
        use_container_width=True,
    ):

        if not email or not password:

            st.error(
                "Enter your email and password."
            )

            return

        try:

            response = login_user(
                email,
                password
            )

            user = response.user

            profile = get_admin_profile(
                user.id
            )

            if not profile:

                st.error(
                    "This account is not authorized "
                    "to access the Admin Portal."
                )

                from database.auth import logout_user

                logout_user()

                return

            st.session_state.admin_authenticated = True
            st.session_state.admin_user = profile

            st.success(
                "Login successful."
            )

            st.rerun()

        except Exception as error:

            st.error(
                f"Login failed: {error}"
            )
