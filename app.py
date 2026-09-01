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

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if "admin_user" not in st.session_state:
    st.session_state.admin_user = None

if "school_authenticated" not in st.session_state:
    st.session_state.school_authenticated = False

if "school_user" not in st.session_state:
    st.session_state.school_user = None



# ============================================================
# BRANDING
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

    st.title("School Portal")

    st.info(
        "School login will be connected next."
    )

    st.divider()

    st.subheader(
        "New School?"
    )

    if st.button(
        "Register School",
        type="primary",
        use_container_width=True,
    ):

        st.session_state.portal = "register"

        st.rerun()


# ============================================================
# SCHOOL REGISTRATION
# ============================================================

def registration_portal():

    show_register()


# ============================================================
# MAIN ROUTER
# ============================================================

def main():

    # --------------------------------------------------------
    # DEFAULT PORTAL
    # --------------------------------------------------------

    if "portal" not in st.session_state:

        st.session_state.portal = "home"

    portal = st.session_state.portal

    # --------------------------------------------------------
    # HOME
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # ADMIN
    # --------------------------------------------------------

    elif portal == "admin":

        admin_portal()

    # --------------------------------------------------------
    # SCHOOL
    # --------------------------------------------------------

    elif page == "school":

    show_school_portal()

    # --------------------------------------------------------
    # REGISTRATION
    # --------------------------------------------------------

    elif portal == "register":

        registration_portal()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()
