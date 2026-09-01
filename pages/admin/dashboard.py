# ============================================================
# EXAMINA AI
# ADMIN DASHBOARD
# ============================================================

import streamlit as st

from database.auth import logout_user


def show_admin_dashboard():

    admin = st.session_state.get(
        "admin_user"
    )

    if not admin:

        st.error(
            "Unauthorized access."
        )

        return

    st.title("Admin Dashboard")

    st.write(
        f"Welcome, {admin['full_name']}"
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Portal",
            "ADMIN"
        )

    with col2:
        st.metric(
            "Role",
            admin["role"]
        )

    with col3:
        st.metric(
            "Status",
            "Active"
        )

    st.divider()

    if st.button(
        "Logout",
        use_container_width=True
    ):

        logout_user()

        st.session_state.admin_authenticated = False
        st.session_state.admin_user = None

        st.rerun()
