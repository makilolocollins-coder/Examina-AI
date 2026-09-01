# ============================================================
# EXAMINA AI
# MAIN APPLICATION
# ============================================================

import streamlit as st

from database.database import test_database_connection

from auth.authentication import (
    initialize_auth,
    is_authenticated,
    logout_user,
)

from auth.login import show_login


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
# INITIALIZE AUTHENTICATION
# ============================================================

initialize_auth()


# ============================================================
# DATABASE CHECK
# ============================================================

def check_configuration():

    try:
        success, result = test_database_connection()

        return success, result

    except Exception as error:

        return False, str(error)


# ============================================================
# HOME
# ============================================================

def show_home():

    st.title("Examina AI 🎓")

    st.subheader(
        "Intelligent school management, academic records, "
        "examination results and secure digital learning."
    )

    st.write(
        "Examina AI brings school administration, "
        "student records, teachers, classes, subjects "
        "and examination management into one platform."
    )

    st.divider()

    # --------------------------------------------------------
    # ACTION BUTTONS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🏫 Register your school",
            use_container_width=True,
            type="primary",
        ):

            st.session_state["page"] = "register"

            st.rerun()

    with col2:

        if st.button(
            "🔐 Sign in",
            use_container_width=True,
        ):

            st.session_state["page"] = "login"

            st.rerun()

    st.divider()

    # --------------------------------------------------------
    # FEATURES
    # --------------------------------------------------------

    st.header("Everything your school needs")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.subheader("🏫 School Management")

        st.write(
            "Manage your school, teachers, students, "
            "classes and subjects."
        )

    with col2:

        st.subheader("📊 Academic Results")

        st.write(
            "Manage tests, examinations, grades, "
            "totals and student positions."
        )

    with col3:

        st.subheader("🤖 AI Examination")

        st.write(
            "Support handwritten examination scanning "
            "and intelligent marking."
        )

    st.divider()

    # --------------------------------------------------------
    # TRUST
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.success("✓ Secure authentication")

    with col2:

        st.success("✓ School-level data isolation")

    with col3:

        st.success("✓ Controlled result publishing")

    st.divider()

    st.caption(
        "Examina AI · Intelligent School Management"
    )


# ============================================================
# DASHBOARD
# ============================================================

def show_dashboard():

    user = st.session_state.get(
        "user",
        {},
    )

    if isinstance(user, dict):

        email = user.get(
            "email",
            "User",
        )

    else:

        email = "User"

    st.title("Dashboard 🎓")

    st.write(
        f"Welcome, {email}"
    )

    st.divider()

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Students",
            "0",
        )

    with col2:

        st.metric(
            "Teachers",
            "0",
        )

    with col3:

        st.metric(
            "Classes",
            "0",
        )

    with col4:

        st.metric(
            "Subjects",
            "0",
        )

    st.divider()

    st.info(
        "Your Examina AI workspace is ready."
    )

    # --------------------------------------------------------
    # LOGOUT
    # --------------------------------------------------------

    if st.button(
        "Logout",
        use_container_width=True,
    ):

        logout_user()

        st.session_state["page"] = "home"

        st.rerun()


# ============================================================
# SCHOOL REGISTRATION
# ============================================================

def show_register():

    st.title("Register your school 🏫")

    st.write(
        "Create your school's secure Examina AI workspace."
    )

    st.divider()

    st.info(
        "The school registration form will be connected "
        "to your Supabase school tables."
    )

    if st.button(
        "← Back to home",
        use_container_width=True,
    ):

        st.session_state["page"] = "home"

        st.rerun()


# ============================================================
# ROUTER
# ============================================================

def main():

    # --------------------------------------------------------
    # DATABASE CONNECTION
    # --------------------------------------------------------

    success, result = check_configuration()

    if not success:

        st.error(
            "Unable to connect to the Examina database."
        )

        with st.expander(
            "Technical details"
        ):

            st.code(
                str(result)
            )

        st.stop()

    # --------------------------------------------------------
    # CURRENT PAGE
    # --------------------------------------------------------

    page = st.session_state.get(
        "page",
        "home",
    )

    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    if page == "login":

        show_login()

        return

    # --------------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------------

    if page == "dashboard":

        if not is_authenticated():

            st.session_state["page"] = "login"

            st.rerun()

            return

        show_dashboard()

        return

    # --------------------------------------------------------
    # REGISTRATION
    # --------------------------------------------------------

    if page == "register":

        show_register()

        return

    # --------------------------------------------------------
    # HOME
    # --------------------------------------------------------

    show_home()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()
