# ============================================================
# EXAMINA AI
# SCHOOL REGISTRATION PAGE
# ============================================================

import streamlit as st


# ============================================================
# REGISTRATION PAGE
# ============================================================

def show_register():

    # --------------------------------------------------------
    # PAGE-SPECIFIC CSS
    # --------------------------------------------------------

    st.markdown(
        """
        <style>

        .register-eyebrow {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #4f46e5;
            margin-bottom: 1rem;
        }

        .register-title {
            font-size: 3.5rem;
            line-height: 1.05;
            font-weight: 800;
            letter-spacing: -0.05em;
            color: #111827;
            margin: 0 0 1.2rem 0;
        }

        .register-description {
            font-size: 1.05rem;
            line-height: 1.7;
            color: #64748b;
            max-width: 550px;
            margin-bottom: 2rem;
        }

        @media (max-width: 768px) {

            .register-title {
                font-size: 2.6rem;
            }

        }

        </style>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # BRAND
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # REGISTRATION HEADER
    # --------------------------------------------------------

    st.markdown(
        """
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
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # REGISTRATION FORM
    # --------------------------------------------------------

    st.divider()

    st.subheader("School information")

    school_name = st.text_input(
        "School name",
        placeholder="Example: Bright Future College",
    )

    registration_number = st.text_input(
        "Registration number",
        placeholder="Enter your school registration number",
    )

    address = st.text_area(
        "School address",
        placeholder="Enter your school's full address",
    )

    phone = st.text_input(
        "Phone number",
        placeholder="08012345678",
    )

    email = st.text_input(
        "School email",
        placeholder="school@example.com",
    )

    if st.button(
        "Continue →",
        use_container_width=True,
        type="primary",
    ):
        st.info(
            "Registration form is ready. "
            "Next we will connect the form to Supabase."
        )
