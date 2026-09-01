# ============================================================
# EXAMINA AI
# SCHOOL DASHBOARD
# ============================================================

import streamlit as st

from database.auth import logout_user


# ============================================================
# SCHOOL ACCESS
# ============================================================

def check_school_access():

    school_user = st.session_state.get(
        "school_user"
    )

    if not school_user:

        st.error(
            "Unauthorized school access."
        )

        st.stop()

    if not school_user.get(
        "is_active",
        False
    ):

        st.error(
            "School account is inactive."
        )

        st.stop()

    school = school_user.get(
        "school"
    )

    if not school:

        st.error(
            "School information could not be loaded."
        )

        st.stop()

    if school.get(
        "verification_status"
    ) != "approved":

        st.error(
            "This school has not been approved."
        )

        st.stop()

    if not school.get(
        "is_active",
        False
    ):

        st.error(
            "This school account is inactive."
        )

        st.stop()

    return school_user, school


# ============================================================
# DASHBOARD
# ============================================================

def show_school_dashboard():

    school_user, school = check_school_access()

    # --------------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------------

    with st.sidebar:

        st.title("Examina AI")

        st.caption(
            school.get(
                "name",
                "School Portal"
            )
        )

        st.divider()

        st.write(
            f"**User:** {school_user.get('full_name', 'School Admin')}"
        )

        st.write(
            f"**Role:** {school_user.get('role', 'school_admin').replace('_', ' ').title()}"
        )

        st.divider()

        if st.button(
            "Logout",
            use_container_width=True
        ):

            try:

                logout_user()

            except Exception:
                pass

            st.session_state.school_authenticated = False

            st.session_state.school_user = None

            st.rerun()

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.title(
        school.get(
            "name",
            "School Dashboard"
        )
    )

    st.success(
        "School account verified and active."
    )

    st.caption(
        "Welcome to your Examina AI school portal."
    )

    st.divider()

    # --------------------------------------------------------
    # SCHOOL INFORMATION
    # --------------------------------------------------------

    st.subheader(
        "School Information"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            "**Registration Number:**",
            school.get(
                "registration_number",
                "N/A"
            )
        )

        st.write(
            "**State:**",
            school.get(
                "state",
                "N/A"
            )
        )

        st.write(
            "**Local Government:**",
            school.get(
                "local_government",
                "N/A"
            )
        )

    with col2:

        st.write(
            "**Email:**",
            school.get(
                "email",
                "N/A"
            )
        )

        st.write(
            "**Phone:**",
            school.get(
                "phone",
                "N/A"
            )
        )

        st.write(
            "**Status:** APPROVED"
        )

    st.divider()

    # --------------------------------------------------------
    # EXAMINA AI FEATURES
    # --------------------------------------------------------

    st.subheader(
        "Examina AI"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.button(
            "Students",
            use_container_width=True
        )

        st.button(
            "Teachers",
            use_container_width=True
        )

    with col2:

        st.button(
            "Subjects",
            use_container_width=True
        )

        st.button(
            "Examinations",
            use_container_width=True
        )

    with col3:

        st.button(
            "Results",
            use_container_width=True
        )

        st.button(
            "AI Marking",
            use_container_width=True
        )

    st.info(
        "School management and examination features "
        "will be connected to this dashboard."
    )
