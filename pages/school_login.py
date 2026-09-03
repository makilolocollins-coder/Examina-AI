# ============================================================
# EXAMINA AI
# SCHOOL PORTAL
# ============================================================

import streamlit as st

from database.auth import (
    get_school_by_registration_number,
)


# ============================================================
# SCHOOL LOGIN
# ============================================================

def show_school_login():

    st.title("🏫 School Portal")

    st.write(
        "Enter your approved school registration number "
        "to access your school portal."
    )

    st.divider()

    with st.form(
        "school_registration_login"
    ):

        registration_number = st.text_input(
            "School Registration Number",
            placeholder="Enter registration number",
        )

        submitted = st.form_submit_button(
            "Access School Portal",
            type="primary",
            use_container_width=True,
        )

    if not submitted:
        return

    registration_number = (
        registration_number.strip()
    )

    if not registration_number:

        st.error(
            "Please enter your school registration number."
        )

        return

    # ========================================================
    # CHECK APPROVED SCHOOL
    # ========================================================

    try:

        school = (
            get_school_by_registration_number(
                registration_number
            )
        )

    except Exception as error:

        st.error(
            "Unable to verify the school."
        )

        st.caption(
            f"Technical error: {error}"
        )

        return

    # ========================================================
    # SCHOOL NOT APPROVED / NOT ACTIVE
    # ========================================================

    if not school:

        st.error(
            "This registration number does not belong "
            "to an approved and active school."
        )

        return

    # ========================================================
    # CREATE SCHOOL SESSION
    # ========================================================

    st.session_state.school_authenticated = True

    st.session_state.school_user = {
        "id": None,
        "school_id": school["id"],
        "full_name": school["name"],
        "role": "school_admin",
        "is_active": school["is_active"],
        "school": school,
    }

    st.session_state.portal = "school"

    st.success(
        f"Welcome, {school['name']}!"
    )

    st.rerun()


# ============================================================
# SCHOOL PORTAL
# ============================================================

def show_school_portal():

    # ========================================================
    # ALREADY LOGGED IN
    # ========================================================

    if st.session_state.get(
        "school_authenticated",
        False,
    ):

        from pages.school_dashboard import (
            show_school_dashboard
        )

        show_school_dashboard()

        return

    # ========================================================
    # EXISTING SCHOOL LOGIN
    # ========================================================

    show_school_login()

    # ========================================================
    # NEW SCHOOL REGISTRATION
    # ========================================================

    st.divider()

    st.subheader("New School?")

    st.write(
        "Register your school for verification and approval "
        "before accessing the school portal."
    )

    if st.button(
        "Register School",
        use_container_width=True,
    ):

        st.session_state.portal = "register"

        st.rerun()
