# ============================================================
# EXAMINA AI
# SCHOOL REGISTRATION
# ============================================================

import streamlit as st

from database.database import (
    get_states,
    get_lgas,
    create_school,
)


# ============================================================
# PAGE STYLES
# ============================================================

def register_styles():

    st.markdown(
        """
        <style>

        /* ----------------------------------------------------
           BASE
        ---------------------------------------------------- */

        .stApp {
            background: #f8fafc;
        }

        .block-container {
            max-width: 1050px;
            padding-top: 2.5rem;
            padding-bottom: 4rem;
        }

        /* ----------------------------------------------------
           HIDE STREAMLIT CHROME
        ---------------------------------------------------- */

        #MainMenu {
            visibility: hidden;
        }

        header {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        /* ----------------------------------------------------
           BRAND
        ---------------------------------------------------- */

        .exa-brand {
            display: flex;
            align-items: center;
            gap: 11px;
            margin-bottom: 3.5rem;
        }

        .exa-mark {
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: #111827;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            box-shadow:
                0 4px 12px rgba(15, 23, 42, 0.12);
        }

        .exa-name {
            font-size: 1.15rem;
            font-weight: 750;
            letter-spacing: -0.035em;
            color: #111827;
        }

        .exa-ai {
            color: #4f46e5;
        }

        /* ----------------------------------------------------
           INTRO
        ---------------------------------------------------- */

        .register-intro {
            max-width: 720px;
            margin-bottom: 2.5rem;
        }

        .register-eyebrow {
            display: inline-block;
            margin-bottom: 0.9rem;
            color: #4f46e5;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .register-title {
            margin: 0;
            color: #0f172a;
            font-size: clamp(2.4rem, 5vw, 4rem);
            line-height: 1;
            font-weight: 800;
            letter-spacing: -0.065em;
        }

        .register-description {
            max-width: 650px;
            margin-top: 1.15rem;
            color: #64748b;
            font-size: 1rem;
            line-height: 1.7;
        }

        /* ----------------------------------------------------
           FORM CARD
        ---------------------------------------------------- */

        .form-card {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 20px;
            padding: 2rem;
            box-shadow:
                0 8px 30px rgba(15, 23, 42, 0.045);
        }

        .form-section-title {
            color: #0f172a;
            font-size: 1.05rem;
            font-weight: 750;
            letter-spacing: -0.02em;
            margin-bottom: 0.25rem;
        }

        .form-section-description {
            color: #64748b;
            font-size: 0.84rem;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }

        .section-divider {
            height: 1px;
            background: #eef2f7;
            margin: 2rem 0;
        }

        /* ----------------------------------------------------
           STREAMLIT INPUTS
        ---------------------------------------------------- */

        label {
            font-weight: 650 !important;
            color: #334155 !important;
        }

        .stTextInput input,
        .stTextArea textarea,
        .stSelectbox div[data-baseweb="select"] {
            border-radius: 10px !important;
        }

        .stTextInput input,
        .stTextArea textarea {
            border-color: #cbd5e1 !important;
            background: white !important;
        }

        .stTextInput input:focus,
        .stTextArea textarea:focus {
            border-color: #6366f1 !important;
            box-shadow:
                0 0 0 1px #6366f1 !important;
        }

        /* ----------------------------------------------------
           BUTTON
        ---------------------------------------------------- */

        .stButton > button {
            min-height: 48px;
            border-radius: 11px;
            font-weight: 700;
            transition:
                transform 120ms ease,
                box-shadow 120ms ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
        }

        /* ----------------------------------------------------
           SECURITY NOTE
        ---------------------------------------------------- */

        .security-note {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            padding: 13px 15px;
            margin-top: 1.25rem;
            border-radius: 11px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            color: #64748b;
            font-size: 0.78rem;
            line-height: 1.55;
        }

        .security-icon {
            color: #16a34a;
            font-weight: 800;
        }

        /* ----------------------------------------------------
           FOOTER
        ---------------------------------------------------- */

        .register-footer {
            text-align: center;
            margin-top: 2.5rem;
            color: #94a3b8;
            font-size: 0.75rem;
        }

        /* ----------------------------------------------------
           MOBILE
        ---------------------------------------------------- */

        @media (max-width: 700px) {

            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
                padding-top: 1.5rem;
            }

            .exa-brand {
                margin-bottom: 2.5rem;
            }

            .register-title {
                font-size: 2.6rem;
            }

            .form-card {
                padding: 1.25rem;
                border-radius: 16px;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# REGISTER PAGE
# ============================================================

def show_register():

    register_styles()

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
                Examina <span class="exa-ai">AI</span>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # INTRO
    # ========================================================

    st.markdown(
        """
        <div class="register-intro">

            <div class="register-eyebrow">
                School registration
            </div>

            <h1 class="register-title">
                Bring your school<br>
                into Examina.
            </h1>

            <p class="register-description">
                Create your school's secure workspace for
                managing students, teachers, academic records,
                examinations and results.
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

    except Exception:

        st.error(
            "We couldn't load the Nigerian states. "
            "Please try again."
        )

        return

    if not states:

        st.warning(
            "No states are currently available."
        )

        return

    # ========================================================
    # FORM CARD
    # ========================================================

    st.markdown(
        '<div class="form-card">',
        unsafe_allow_html=True,
    )

    # ========================================================
    # SCHOOL INFORMATION
    # ========================================================

    st.markdown(
        """
        <div class="form-section-title">
            School information
        </div>

        <div class="form-section-description">
            Enter the official information used to identify
            your school.
        </div>
        """,
        unsafe_allow_html=True,
    )

    school_name = st.text_input(
        "School name *",
        placeholder="e.g. Bright Future College",
    )

    registration_number = st.text_input(
        "School registration number *",
        placeholder="Official school registration number",
    )

    motto = st.text_input(
        "School motto",
        placeholder="e.g. Knowledge, Character and Excellence",
    )

    # ========================================================
    # LOCATION
    # ========================================================

    st.markdown(
        '<div class="section-divider"></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="form-section-title">
            School location
        </div>

        <div class="form-section-description">
            Select the state and Local Government Area where
            your school is located.
        </div>
        """,
        unsafe_allow_html=True,
    )

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
            if state["name"] == selected_state_name
        ),
        None,
    )

    if selected_state is None:

        st.error(
            "Unable to identify the selected state."
        )

        return

    state_id = selected_state["id"]

    # ========================================================
    # LGAS
    # ========================================================

    try:

        lgas = get_lgas(state_id)

    except Exception:

        st.error(
            "We couldn't load the Local Government Areas "
            "for this state."
        )

        return

    if not lgas:

        st.warning(
            "No Local Government Areas were found "
            "for this state."
        )

        return

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
            if lga["name"] == selected_lga_name
        ),
        None,
    )

    if selected_lga is None:

        st.error(
            "Unable to identify the selected LGA."
        )

        return

    lga_id = selected_lga["id"]

    # ========================================================
    # CONTACT
    # ========================================================

    st.markdown(
        '<div class="section-divider"></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="form-section-title">
            Contact information
        </div>

        <div class="form-section-description">
            These details help Examina identify and contact
            your school when necessary.
        </div>
        """,
        unsafe_allow_html=True,
    )

    address = st.text_area(
        "School address *",
        placeholder="Enter the full school address",
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

    # ========================================================
    # SECURITY
    # ========================================================

    st.markdown(
        """
        <div class="security-note">

            <div class="security-icon">
                ✓
            </div>

            <div>
                Your registration is stored securely.
                Your school will initially remain
                <strong>pending verification</strong> until
                the required verification process is completed.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    # ========================================================
    # SUBMIT
    # ========================================================

    submitted = st.button(
        "Create school workspace →",
        use_container_width=True,
        type="primary",
    )

    if submitted:

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

        if not address.strip():

            st.error(
                "Please enter the school address."
            )

            return

        # ----------------------------------------------------
        # CREATE SCHOOL
        # ----------------------------------------------------

        try:

            result = create_school(
                name=school_name.strip(),
                registration_number=registration_number.strip(),
                state=selected_state["name"],
                local_government=selected_lga["name"],
                lga_id=selected_lga["id"],
                address=address.strip(),
                phone=phone.strip(),
                email=email.strip(),
                motto=motto.strip(),
            )

        except Exception as error:

            st.error(
                "We couldn't create the school workspace."
            )

            # Don't expose database internals to users.
            with st.expander("Technical details"):

                st.code(str(error))

            return

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        if result:

            school = result[0]

            st.session_state["school_id"] = school["id"]

            st.session_state["school"] = school

            st.session_state["page"] = "dashboard"

            st.success(
                "School workspace created successfully."
            )

            st.rerun()

        else:

            st.error(
                "The school could not be created. "
                "Please try again."
            )

    st.markdown(
        '<div class="section-divider"></div>',
        unsafe_allow_html=True,
    )

    # ========================================================
    # EXISTING SCHOOL
    # ========================================================

    st.caption(
        "Already registered your school?"
    )

    if st.button(
        "Sign in instead",
        use_container_width=True,
    ):

        st.session_state["page"] = "login"

        st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True,
    )

    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown(
        """
        <div class="register-footer">
            Examina AI · Secure school management
        </div>
        """,
        unsafe_allow_html=True,
    )
