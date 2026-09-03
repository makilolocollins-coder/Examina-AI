# ============================================================
# EXAMINA AI
# SCHOOL PORTAL
# ============================================================

import streamlit as st

from database.auth import (
    get_school_by_registration_number,
    get_school_status,
    create_school_session,
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

    # ========================================================
    # EXISTING SCHOOL
    # ========================================================

    st.subheader("Existing School")

    with st.form(
        "school_registration_login"
    ):

        registration_number = st.text_input(
            "School Registration Number",
            placeholder="Enter your registration number",
        )

        submitted = st.form_submit_button(
            "Access School Portal",
            type="primary",
            use_container_width=True,
        )

    if submitted:

        registration_number = (
            registration_number
            .strip()
        )

        # ----------------------------------------------------
        # EMPTY REGISTRATION NUMBER
        # ----------------------------------------------------

        if not registration_number:

            st.error(
                "Please enter your school registration number."
            )

            return

        # ----------------------------------------------------
        # CHECK SCHOOL
        # ----------------------------------------------------

        try:

            school = (
                get_school_by_registration_number(
                    registration_number
                )
            )

        except Exception as error:

            st.error(
                "Unable to verify the school at this time."
            )

            st.caption(
                f"Technical error: {error}"
            )

            return

        # ====================================================
        # APPROVED SCHOOL
        # ====================================================

        if school:

            # ------------------------------------------------
            # CREATE SCHOOL SESSION
            # ------------------------------------------------

            st.session_state.school_authenticated = True

            st.session_state.school_user = (
                create_school_session(
                    school
                )
            )

            st.session_state.portal = "school"

            st.success(
                f"Welcome, {school['school_name']}!"
            )

            st.rerun()

        # ====================================================
        # SCHOOL WAS NOT APPROVED
        # ====================================================

        try:

            status = get_school_status(
                registration_number
            )

        except Exception as error:

            st.error(
                "Unable to check school status."
            )

            st.caption(
                f"Technical error: {error}"
            )

            return

        # ----------------------------------------------------
        # REGISTRATION NUMBER DOES NOT EXIST
        # ----------------------------------------------------

        if not status:

            st.error(
                "School registration number not found."
            )

            st.info(
                "If your school has not registered with "
                "Examina AI, use the registration option below."
            )

            return

        # ----------------------------------------------------
        # PENDING
        # ----------------------------------------------------

        if status["verification_status"] == "pending":

            st.warning(
                "Your school registration is still "
                "awaiting admin approval."
            )

            st.info(
                "You will be able to access the school "
                "portal after your registration has been approved."
            )

            return

        # ----------------------------------------------------
        # REJECTED
        # ----------------------------------------------------

        if status["verification_status"] == "rejected":

            st.error(
                "Your school registration has been rejected."
            )

            st.info(
                "Please contact Examina AI administration "
                "for further information."
            )

            return

        # ----------------------------------------------------
        # SUSPENDED
        # ----------------------------------------------------

        if status["verification_status"] == "suspended":

            st.error(
                "This school account has been suspended."
            )

            st.info(
                "Please contact Examina AI administration."
            )

            return

        # ----------------------------------------------------
        # NOT ACTIVE
        # ----------------------------------------------------

        if not status["is_active"]:

            st.error(
                "This school is currently inactive."
            )

            return

        # ----------------------------------------------------
        # FALLBACK
        # ----------------------------------------------------

        st.error(
            "This school is not currently authorized "
            "to access the Examina AI school portal."
        )


# ============================================================
# SCHOOL REGISTRATION
# ============================================================

def show_school_registration_option():

    st.divider()

    st.subheader("New School?")

    st.write(
        "Register your school for verification and approval "
        "by Examina AI administration."
    )

    if st.button(
        "Register School",
        use_container_width=True,
    ):

        st.session_state.portal = "register"

        st.rerun()


# ============================================================
# SCHOOL PORTAL
# ============================================================

def show_school_portal():

    # ========================================================
    # ALREADY AUTHENTICATED
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

    # ========================================================
    # NEW SCHOOL REGISTRATION
    # ========================================================

    show_school_registration_option()
