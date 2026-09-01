# ============================================================
# EXAMINA AI
# LOGIN PAGE
# ============================================================

import streamlit as st

from auth.authentication import login_user


def show_login():

    st.markdown(
        """
        <div style="
            max-width:620px;
            margin:3rem auto 1rem auto;
            text-align:center;
        ">
            <div style="
                font-size:3rem;
                margin-bottom:0.5rem;
            ">
                🎓
            </div>

            <h1 style="
                margin:0;
                font-weight:800;
                letter-spacing:-0.04em;
            ">
                Welcome back
            </h1>

            <p style="
                color:#64748b;
                margin-top:0.7rem;
            ">
                Sign in securely to your Examina AI workspace.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("examina_login"):

        email = st.text_input(
            "Email address",
            placeholder="you@example.com",
            autocomplete="email",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            autocomplete="current-password",
        )

        submitted = st.form_submit_button(
            "Sign in",
            use_container_width=True,
        )

        if submitted:

            success, error = login_user(
                email=email,
                password=password,
            )

            if success:
                st.success("Signed in successfully.")
                st.rerun()

            else:
                st.error(error)
