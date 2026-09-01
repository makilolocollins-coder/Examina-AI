# ============================================================
# EXAMINA AI
# SCHOOL REGISTRATION PAGE
# ============================================================

import streamlit as st


# ============================================================
# PAGE
# ============================================================

def show_register():
    """
    Display the school registration page.

    This page only handles the user interface.
    Database operations will be added separately.
    """

    # ========================================================
    # BRAND
    # ========================================================

    brand_col1, brand_col2 = st.columns(
        [0.06, 0.94],
        vertical_alignment="center",
    )

    with brand_col1:
        st.markdown(
            "## 🎓"
        )

    with brand_col2:
        st.markdown(
            "## Examina AI"
        )

    st.write("")

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.caption(
        "SCHOOL REGISTRATION"
    )

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
    # REGISTRATION FORM
    # ========================================================

    st.subheader(
        "School information"
    )

    with st.form(
        "school_registration_form",
        clear_on_submit=False,
    ):

        school_name = st.text_input(
            "School name *",
            placeholder="Example: Bright Future College",
        )

        registration_number = st.text_input(
            "Registration number *",
            placeholder="Enter your school registration number",
        )

        address = st.text_area(
            "School address",
            placeholder="Enter your school's full address",
            height=100,
        )

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

        submitted = st.form_submit_button(
            "Continue →",
            use_container_width=True,
            type="primary",
        )

    # ========================================================
    # FORM VALIDATION
    # ========================================================

    if submitted:

        errors = []

        if not school_name.strip():
            errors.append(
                "School name is required."
            )

        if not registration_number.strip():
            errors.append(
                "Registration number is required."
            )

        if errors:

            for error in errors:
                st.error(error)

            return

        # ====================================================
        # TEMPORARY SUCCESS
        # ====================================================

        # Database registration will be connected in a
        # separate service layer.

        st.success(
            "School information saved successfully. "
            "You can now continue with the next step."
        )

        # Store temporary registration data safely
        # in the Streamlit session.

        st.session_state["registration_data"] = {
            "name": school_name.strip(),
            "registration_number": (
                registration_number.strip()
            ),
            "address": address.strip(),
            "phone": phone.strip(),
            "email": email.strip(),
        }
