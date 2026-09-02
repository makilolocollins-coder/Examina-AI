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

    st.caption(
        "Enter your approved school registration number "
        "to access your school portal."
    )

    with st.form("school_registration_login"):

        registration_number = st.text_input(
            "School Registration Number"
        )

        submitted = st.form_submit_button(
            "Access School Portal",
            type="primary",
            use_container_width=True,
        )

    if not submitted:
        return

    registration_number = registration_number.strip()

    if not registration_number:

        st.error(
            "Enter your school registration number."
        )

        return

    # --------------------------------------------------------
    # VERIFY SCHOOL
    # --------------------------------------------------------

    try:

        school = get_school_by_registration_number(
            registration_number
        )

    except Exception as error:

        st.error(
            f"Could not verify school: {error}"
        )

        return

    # --------------------------------------------------------
    # SCHOOL NOT APPROVED
    # --------------------------------------------------------

    if not school:

        st.error(
            "This school registration number is not "
            "associated with an approved and active school."
        )

        return

    # --------------------------------------------------------
    # CREATE SCHOOL SESSION
    # --------------------------------------------------------

    st.session_state.school_authenticated = True

    st.session_state.school_user = {
        "id": None,
        "school_id": school["school_id"],
        "full_name": school["school_name"],
        "role": "school_admin",
        "is_active": True,
        "school": {
            "id": school["school_id"],
            "name": school["school_name"],
            "registration_number":
                school["registration_number"],
            "state": school["state"],
            "local_government":
                school["local_government"],
            "address": school["address"],
            "phone": school["phone"],
            "email": school["email"],
            "motto": school["motto"],
            "logo_url": school["logo_url"],
            "verification_status":
                school["verification_status"],
            "is_active": school["is_active"],
        },
    }

    st.success(
        f"Welcome, {school['school_name']}!"
    )

    st.rerun()


# ============================================================
# SCHOOL PORTAL
# ============================================================

def show_school_portal():

    # ========================================================
    # ALREADY ACCESSED
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
    # SCHOOL LOGIN
    # ========================================================

    show_school_login()
