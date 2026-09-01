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

    return bool(
        re.match(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            email,
        )
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
    # HEADER
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
            "Unable to load states. Please try again."
        )

        return

    if not states:

        st.warning(
            "No states are available."
        )

        return

    # ========================================================
    # STATE LOOKUP
    # ========================================================

    state_lookup = {
        state["name"]: state
        for state in states
    }

    # ========================================================
    # FORM
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
            placeholder="Enter your official school registration number",
        )

        # ----------------------------------------------------
        # STATE
        # ----------------------------------------------------

        state_name = st.selectbox(
            "State *",
            options=list(state_lookup.keys()),
            index=None,
            placeholder="Select state",
        )

        # ----------------------------------------------------
        # LGA
        # ----------------------------------------------------

        selected_lga = None

        if state_name:

            selected_state = state_lookup[state_name]

            try:

                lgas = get_lgas(
                    selected_state["id"]
                )

            except Exception:

                st.error(
                    "Unable to load local governments."
                )

                return

            if lgas:

                lga_lookup = {
                    lga["name"]: lga
                    for lga in lgas
                }

                lga_name = st.selectbox(
                    "Local Government *",
                    options=list(lga_lookup.keys()),
                    index=None,
                    placeholder="Select local government",
                )

                if lga_name:

                    selected_lga = lga_lookup[
                        lga_name
                    ]

            else:

                st.warning(
                    "No local governments found "
                    "for this state."
                )

        else:

            st.selectbox(
                "Local Government *",
                options=[],
                disabled=True,
                placeholder="Select a state first",
            )

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
    # STOP IF NOT SUBMITTED
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
    # CLEAN INPUT
    # ========================================================

    school_name = school_name.strip()

    registration_number = (
        registration_number.strip()
    )

    address = address.strip()

    phone = phone.strip()

    email = email.strip()

    motto = motto.strip()

    # ========================================================
    # CHECK DUPLICATE REGISTRATION NUMBER
    # ========================================================

    try:

        exists = school_exists(
            registration_number
        )

    except Exception:

        st.error(
            "Unable to verify the registration number."
        )

        return

    if exists:

        st.error(
            "A school with this registration number "
            "already exists."
        )

        return

    # ========================================================
    # REGISTER SCHOOL
    # ========================================================

    try:

        result = create_school(

            name=school_name,

            registration_number=(
                registration_number
            ),

            local_government=(
                selected_lga["name"]
            ),

            state=state_name,

            address=address,

            phone=phone,

            email=email,

            motto=motto,

            verification_status="pending",

            is_active=False,

            lga_id=selected_lga["id"],

            administrative_area_id=None,
        )

    except Exception:

        st.error(
            "School registration failed. "
            "Please try again."
        )

        return

    # ========================================================
    # CONFIRM
    # ========================================================

    if not result:

        st.error(
            "The school was not registered."
        )

        return

    # ========================================================
    # SAVE SESSION DATA
    # ========================================================

    school = result[0]

    st.session_state["school_id"] = school["id"]

    st.session_state["registration_data"] = school

    # ========================================================
    # SUCCESS
    # ========================================================

    st.success(
        "School registration submitted successfully."
    )

    st.info(
        "Your school is awaiting verification. "
        "You can continue once the school has been approved."
    )
