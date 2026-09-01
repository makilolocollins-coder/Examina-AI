# ============================================================
# EXAMINA AI
# SCHOOL REGISTRATION PAGE
# ============================================================

import streamlit as st

from database.database import (
    get_states,
    get_lgas,
    create_school,
)


# ============================================================
# PAGE CSS
# ============================================================

def registration_styles():

    st.markdown(
        """
        <style>

        .register-shell {
            max-width: 900px;
            margin: 0 auto;
        }

        .register-eyebrow {
            color: #4f46e5;
            font-size: 0.75rem;
            font-weight: 800;
            letter-spacing: 0.10em;
            text-transform: uppercase;
            margin-bottom: 0.7rem;
        }

        .register-title {
            font-size: clamp(
                2.6rem,
                6vw,
                4.6rem
            );

            line-height: 0.98;

            letter-spacing: -0.065em;

            font-weight: 800;

            color: #0f172a;

            margin: 0;
        }

        .register-description {
            max-width: 650px;

            color: #64748b;

            font-size: 1rem;

            line-height: 1.7;

            margin-top: 1.3rem;

            margin-bottom: 2.5rem;
        }

        .register-card {
            background: white;

            border: 1px solid #e2e8f0;

            border-radius: 24px;

            padding: 2rem;

            box-shadow:
                0 15px 40px rgba(
                    15,
                    23,
                    42,
                    0.06
                );
        }

        .card-title {
            font-size: 1.2rem;
            font-weight: 750;
            color: #0f172a;
            margin-bottom: 0.25rem;
        }

        .card-description {
            color: #64748b;
            font-size: 0.88rem;
            margin-bottom: 1.5rem;
        }

        .required-note {
            color: #94a3b8;
            font-size: 0.78rem;
            margin-bottom: 1rem;
        }

        .stButton > button {

            min-height: 48px;

            border-radius: 12px;

            font-weight: 700;

            transition:
                transform 0.15s ease,
                box-shadow 0.15s ease;

        }

        .stButton > button:hover {

            transform: translateY(-1px);

            box-shadow:
                0 8px 20px rgba(
                    15,
                    23,
                    42,
                    0.10
                );

        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# REGISTRATION PAGE
# ============================================================

def show_register():

    registration_styles()

    # ========================================================
    # BRAND
    # ========================================================

    st.markdown(
        """
        <div class="exa-brand">

            <div class="exa-mark">
                🎓
            </div>

            <div class="exa-name">
                Examina
                <span class="exa-ai">AI</span>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # HERO
    # ========================================================

    st.markdown(
        """
        <div class="register-shell">

            <div class="register-eyebrow">
                School registration
            </div>

            <h1 class="register-title">
                Bring your school<br>
                into Examina.
            </h1>

            <p class="register-description">
                Create your school's secure workspace
                for managing students, teachers,
                academic records, examinations
                and results.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # LOAD STATES
    # ========================================================

    try:

        states = get_states()

    except Exception as error:

        st.error(
            "We couldn't load the Nigerian states."
        )

        with st.expander(
            "Technical details"
        ):

            st.code(str(error))

        st.stop()

    if not states:

        st.warning(
            "No Nigerian states are available."
        )

        st.stop()

    # ========================================================
    # REGISTRATION CARD
    # ========================================================

    st.markdown(
        """
        <div class="register-card">

            <div class="card-title">
                School information
            </div>

            <div class="card-description">
                Enter the official information
                for your school.
            </div>

            <div class="required-note">
                Fields marked with * are required.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # SCHOOL DETAILS
    # ========================================================

    school_name = st.text_input(
        "School name *",
        placeholder="e.g. Bright Future College",
    )

    registration_number = st.text_input(
        "School registration number *",
        placeholder="e.g. MOE/2026/001234",
    )

    address = st.text_area(
        "School address",
        placeholder="Enter the school's full address",
        height=100,
    )

    phone = st.text_input(
        "School phone number",
        placeholder="e.g. 08012345678",
    )

    email = st.text_input(
        "School email",
        placeholder="school@example.com",
    )

    st.divider()

    # ========================================================
    # LOCATION
    # ========================================================

    st.subheader("School location")

    state_names = [
        state["name"]
        for state in states
    ]

    selected_state_name = st.selectbox(
        "State *",
        state_names,
    )

    selected_state = next(
        (
            state
            for state in states
            if state["name"]
            == selected_state_name
        ),
        None,
    )

    if selected_state is None:

        st.error(
            "The selected state could not be found."
        )

        st.stop()

    state_id = selected_state["id"]

    # ========================================================
    # LOAD LGAs
    # ========================================================

    try:

        lgas = get_lgas(
            state_id
        )

    except Exception as error:

        st.error(
            "We couldn't load the Local Government Areas."
        )

        with st.expander(
            "Technical details"
        ):

            st.code(str(error))

        st.stop()

    if not lgas:

        st.warning(
            "No Local Government Areas were found "
            "for the selected state."
        )

        st.stop()

    lga_names = [
        lga["name"]
        for lga in lgas
    ]

    selected_lga_name = st.selectbox(
        "Local Government Area *",
        lga_names,
    )

    selected_lga = next(
        (
            lga
            for lga in lgas
            if lga["name"]
            == selected_lga_name
        ),
        None,
    )

    if selected_lga is None:

        st.error(
            "The selected Local Government Area "
            "could not be found."
        )

        st.stop()

    lga_id = selected_lga["id"]

    # ========================================================
    # SUBMIT
    # ========================================================

    st.write("")

    if st.button(
        "Create school workspace",
        use_container_width=True,
        type="primary",
    ):

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not school_name.strip():

            st.error(
                "Please enter the school name."
            )

            return

        if not registration_number.strip():

            st.error(
                "Please enter the school registration number."
            )

            return

        # ----------------------------------------------------
        # CREATE SCHOOL
        # ----------------------------------------------------

        try:

            result = create_school(

                name=school_name.strip(),

                registration_number=(
                    registration_number.strip()
                ),

                local_government=(
                    selected_lga["name"]
                ),

                state=(
                    selected_state["name"]
                ),

                address=address.strip(),

                phone=phone.strip(),

                email=email.strip(),

                lga_id=lga_id,
            )

        except Exception as error:

            st.error(
                "School registration failed."
            )

            with st.expander(
                "Technical details"
            ):

                st.code(str(error))

            return

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        if result:

            school = result[0]

            st.success(
                "School registered successfully."
            )

            st.session_state[
                "school_id"
            ] = school["id"]

            st.session_state[
                "school"
            ] = school

            st.session_state[
                "registration_complete"
            ] = True

            st.balloons()

        else:

            st.error(
                "The school could not be registered."
            )
