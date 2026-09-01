# ============================================================
# EXAMINA AI
# SCHOOL REGISTRATION PAGE
# ============================================================

import re
import streamlit as st

from database.database import (
    get_states,
    get_lgas,
    school_exists,
    create_school,
)


# ============================================================
# EMAIL VALIDATION
# ============================================================

def valid_email(email):

    if not email:
        return True

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return bool(
        re.match(pattern, email)
    )


# ============================================================
# REGISTRATION PAGE
# ============================================================

def show_register():

    # ========================================================
    # BRAND
    # ========================================================

    brand_col1, brand_col2 = st.columns(
        [0.06, 0.94],
        vertical_alignment="center",
    )

    with brand_col1:
        st.markdown("## 🎓")

    with brand_col2:
        st.markdown("## Examina AI")

    st.write("")

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.caption("SCHOOL REGISTRATION")

    st.title(
        "Bring your school\ninto Examina."
    )

    st.write(
        """
        Create your school's secure workspace for managing
        students, teachers, academic records, examinations
        and results.
        """
    )

    st.write("")
    st.divider()

    # ========================================================
    # LOAD STATES
    # ========================================================

    try:

        states = get_states()

    except Exception:

        st.error(
            "We could not load the states. "
            "Please try again."
        )

        return

    if not states:

        st.warning(
            "No states are currently available."
        )

        return

    # ========================================================
    # STATE OPTIONS
    # ========================================================

    state_options = {
        state["name"]: state
        for state in states
    }

    # ========================================================
    # REGISTRATION FORM
    # ========================================================

    st.subheader("School information")

    with st.form(
        "school_registration_form",
        clear_on_submit=False,
    ):

        # ----------------------------------------------------
        # SCHOOL NAME
        # ----------------------------------------------------

        school_name = st.text_input(
            "School name *",
            placeholder="Example: Bright Future College",
        )

        # ----------------------------------------------------
        # REGISTRATION NUMBER
        # ----------------------------------------------------

        registration_number = st.text_input(
            "Registration number *",
            placeholder="Enter your school registration number",
        )

        # ----------------------------------------------------
        # LOCATION
        # ----------------------------------------------------

        state_name = st.selectbox(
            "State *",
            options=list(state_options.keys()),
            index=None,
            placeholder="Select state",
        )

        lga_name = None
        selected_lga = None

        if state_name:

            selected_state = state_options[state_name]

            try:

                lgas = get_lgas(
                    selected_state["id"]
                )

            except Exception:

                st.error(
                    "We could not load the LGAs "
                    "for this state."
                )

                return

            if not lgas:

                st.warning(
                    "No local governments are available "
                    "for the selected state."
                )

            else:

                lga_options = {
                    lga["name"]: lga
                    for lga in lgas
                }

                lga_name = st.selectbox(
                    "Local Government *",
                    options=list(lga_options.keys()),
                    index=None,
                    placeholder="Select local government",
                )

                if lga_name:
                    selected_lga = lga_options[lga_name]

        # ----------------------------------------------------
        # ADDRESS
        # ----------------------------------------------------

        address = st.text_area(
            "School address",
            placeholder="Enter your school's full address",
            height=100,
        )

        # ----------------------------------------------------
        # CONTACT
        # ----------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            phone = st.text_input(
                "Phone number",
                placeholder="08012345678",
            )

        with col2:

            email = st.text_input(
                "School email",
                placeholder="school@example.com",
            )

        # ----------------------------------------------------
        # MOTTO
        # ----------------------------------------------------

        motto = st.text_input(
            "School motto",
            placeholder="Optional",
        )

        # ----------------------------------------------------
        # SUBMIT
        # ----------------------------------------------------

        submitted = st.form_submit_button(
            "Register school →",
            use_container_width=True,
            type="primary",
        )

    # ========================================================
    # FORM SUBMISSION
    # ========================================================

    if not submitted:
        return

    # ========================================================
    # VALIDATION
    # ========================================================

    errors = []

    if not school_name.strip():

        errors.append(
            "School name is required."
        )

    if not registration_number.strip():

        errors.append(
            "Registration number is required."
        )

    if not state_name:

        errors.append(
            "State is required."
        )

    if not selected_lga:

        errors.append(
            "Local Government is required."
        )

    if not valid_email(email.strip()):

        errors.append(
            "Please enter a valid school email."
        )

    if errors:

        for error in errors:
            st.error(error)

        return

    # ========================================================
    # CLEAN DATA
    # ========================================================

    clean_name = school_name.strip()

    clean_registration_number = (
        registration_number.strip()
    )

    clean_address = address.strip()

    clean_phone = phone.strip()

    clean_email = email.strip()

    clean_motto = motto.strip()

    # ========================================================
    # CHECK DUPLICATE REGISTRATION NUMBER
    # ========================================================

    try:

        if school_exists(
            clean_registration_number
        ):

            st.error(
                "A school with this registration number "
                "already exists."
            )

            return

    except Exception:

        st.error(
            "We could not verify the registration number. "
            "Please try again."
        )

        return

    # ========================================================
    # CREATE SCHOOL
    # ========================================================

    try:

        result = create_school(

            name=clean_name,

            registration_number=(
                clean_registration_number
            ),

            local_government=(
                selected_lga["name"]
            ),

            state=state_name,

            address=clean_address,

            phone=clean_phone,

            email=clean_email,

            motto=clean_motto,

            verification_status="pending",

            is_active=False,

            lga_id=selected_lga["id"],

            administrative_area_id=None,
        )

    except Exception:

        st.error(
            "We could not complete the school "
            "registration. Please try again."
        )

        return

    # ========================================================
    # CONFIRM DATABASE INSERT
    # ========================================================

    if not result:

        st.error(
            "The school could not be registered."
        )

        return

    # ========================================================
    # STORE REGISTRATION RESULT
    # ========================================================

    school = result[0]

    st.session_state["registration_data"] = school

    st.session_state["school_id"] = school["id"]

    # ========================================================
    # SUCCESS
    # ========================================================

    st.success(
        "School registration submitted successfully."
    )

    st.info(
        "Your school is currently awaiting verification. "
        "You will be able to continue once the school "
        "has been approved."
    )
