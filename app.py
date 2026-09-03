# ============================================================
# EXAMINA AI
# MAIN APPLICATION ROUTER
# ============================================================

import streamlit as st

from pages.register import show_register
from pages.admin.login import show_admin_login
from pages.admin.dashboard import show_admin_dashboard
from pages.admin.verification import show_verification
from pages.school_login import show_school_portal

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Examina AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# SESSION STATE
# ============================================================

if "portal" not in st.session_state:
    st.session_state.portal = "home"

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if "admin_user" not in st.session_state:
    st.session_state.admin_user = None

if "school_authenticated" not in st.session_state:
    st.session_state.school_authenticated = False

if "school_user" not in st.session_state:
    st.session_state.school_user = None


# ============================================================
# BRANDING / BASIC STYLING
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# ADMIN PORTAL
# ============================================================

def admin_portal():

    # --------------------------------------------------------
    # ADMIN LOGIN
    # --------------------------------------------------------

    if not st.session_state.admin_authenticated:

        show_admin_login()

        return

    # --------------------------------------------------------
    # ADMIN SIDEBAR
    # --------------------------------------------------------

    st.sidebar.title("Examina AI")
    st.sidebar.caption("Admin Portal")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "School Verification",
        ],
    )

    st.sidebar.divider()

    if page == "Dashboard":

        show_admin_dashboard()

    elif page == "School Verification":

        show_verification()


# ============================================================
# SCHOOL PORTAL
# ============================================================

def school_portal():

    # --------------------------------------------------------
    # ALREADY AUTHENTICATED
    # --------------------------------------------------------

    if st.session_state.get(
        "school_authenticated",
        False,
    ):

        from pages.school_dashboard import (
            show_school_dashboard
        )

        show_school_dashboard()

        return

    # --------------------------------------------------------
    # SCHOOL LOGIN
    # --------------------------------------------------------

    from pages.school_login import (
        show_school_portal
    )

    show_school_portal()


# ============================================================
# SCHOOL REGISTRATION
# ============================================================

def registration_portal():

    show_register()


# ============================================================
# MAIN ROUTER
# ============================================================

def main():

    portal = st.session_state.portal

    # ========================================================
    # HOME
    # ========================================================

    if portal == "home":

        st.title("Examina AI")

        st.subheader(
            "School Examination & Management Platform"
        )

        st.write(
            "Choose your portal."
        )

        st.divider()

        col1, col2 = st.columns(2)

        # ----------------------------------------------------
        # SCHOOL
        # ----------------------------------------------------

        with col1:

            st.subheader(
                "🏫 School Portal"
            )

            st.write(
                "Access your school's examination "
                "and management system."
            )

            if st.button(
                "Enter School Portal",
                use_container_width=True,
            ):

                st.session_state.portal = "school"

                st.rerun()

        # ----------------------------------------------------
        # ADMIN
        # ----------------------------------------------------

        with col2:

            st.subheader(
                "🔐 Admin Portal"
            )

            st.write(
                "For authorized Examina AI administrators."
            )

            if st.button(
                "Enter Admin Portal",
                use_container_width=True,
            ):

                st.session_state.portal = "admin"

                st.rerun()

    # ========================================================
    # ADMIN
    # ========================================================

    elif portal == "admin":

        admin_portal()

    # ========================================================
    # SCHOOL
    # ========================================================

    elif portal == "school":

        school_portal()

    # ========================================================
    # REGISTRATION
    # ========================================================

    elif portal == "register":

        registration_portal()


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    main()
