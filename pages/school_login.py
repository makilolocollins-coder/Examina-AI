# ============================================================
# EXAMINA AI
# SCHOOL LOGIN
# ============================================================

import streamlit as st

from database.auth import (
    create_school_account,
    get_school_account_eligibility,
    get_school_user_profile,
    login_school,
    logout_user,
)


# ============================================================
# SCHOOL ACCOUNT SETUP
# ============================================================

def show_account_setup():

    st.title("School Account Setup")

    st.caption(
        "Create the login account for your approved school."
    )

    st.info(
        "Your school must already be approved by Examina AI "
        "before an account can be created."
    )

    with st.form("school_account_setup"):

        registration_number = st.text_input(
            "School Registration Number"
        )

        email = st.text_input(
            "School Registered Email"
        )

        full_name = st.text_input(
            "Account Holder Name"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Create School Account",
            type="primary",
            use_container_width=True
        )

    if not submitted:
        return

    registration_number = (
        registration_number.strip()
    )

    email = (
        email.strip().lower()
    )

    full_name = (
        full_name.strip()
    )

    if not registration_number:

        st.error(
            "Enter your school registration number."
        )

        return

    if not email:

        st.error(
            "Enter the school's registered email."
        )

        return

    if not full_name:

        st.error(
            "Enter the account holder's name."
        )

        return

    if not password:

        st.error(
            "Create a password."
        )

        return

    if len(password) < 8:

        st.error(
            "Password must contain at least 8 characters."
        )

        return

    if password != confirm_password:

        st.error(
            "Passwords do not match."
        )

        return

    # --------------------------------------------------------
    # CHECK SCHOOL ELIGIBILITY
    # --------------------------------------------------------

    try:

        school = get_school_account_eligibility(
            registration_number,
            email
        )

    except Exception as error:

        st.error(
            f"Could not verify school: {error}"
        )

        return

    if not school:

        st.error(
            "We could not find an approved school "
            "matching that registration number and email."
        )

        return

    school_id = school["school_id"]

    school_name = school["school_name"]

    # --------------------------------------------------------
    # CREATE AUTH ACCOUNT
    # --------------------------------------------------------

    try:

        response = create_school_account(
            email=email,
            password=password,
            school_id=school_id,
            full_name=full_name,
        )

        user = getattr(
            response,
            "user",
            None
        )

        session = getattr(
            response,
            "session",
            None
        )

        if not user:

            st.error(
                "The school account could not be created."
            )

            return

        if session:

            profile = get_school_user_profile(
                user.id
            )

            if not profile:

                logout_user()

                st.error(
                    "The school account was created, "
                    "but the school profile could not be linked."
                )

                return

            st.session_state.school_authenticated = True

            st.session_state.school_user = profile

            st.success(
                f"{school_name} account created successfully."
            )

            st.rerun()

        else:

            st.success(
                "School account created successfully."
            )

            st.info(
                "Please check the registered school email "
                "and confirm your email address before logging in."
            )

    except Exception as error:

        st.error(
            f"Could not create school account: {error}"
        )


# ============================================================
# SCHOOL LOGIN
# ============================================================

def show_school_login():

    st.title("School Portal")

    st.caption(
        "Sign in to access Examina AI."
    )

    with st.form("school_login"):

        email = st.text_input(
            "School Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Login",
            type="primary",
            use_container_width=True
        )

    if not submitted:
        return

    email = email.strip().lower()

    if not email:

        st.error(
            "Enter your school email."
        )

        return

    if not password:

        st.error(
            "Enter your password."
        )

        return

    try:

        response = login_school(
            email,
            password
        )

        user = getattr(
            response,
            "user",
            None
        )

        if not user:

            st.error(
                "Login failed."
            )

            return

        profile = get_school_user_profile(
            user.id
        )

        if not profile:

            logout_user()

            st.error(
                "This account is not linked to an active "
                "approved school."
            )

            return

        st.session_state.school_authenticated = True

        st.session_state.school_user = profile

        st.rerun()

    except Exception as error:

        st.error(
            f"Login failed: {error}"
        )


# ============================================================
# SCHOOL LOGIN PAGE
# ============================================================

def show_school_portal():

    if (
        st.session_state.get(
            "school_authenticated",
            False
        )
    ):

        from pages.school_dashboard import (
            show_school_dashboard
        )

        show_school_dashboard()

        return

    login_tab, setup_tab = st.tabs(
        [
            "School Login",
            "Create School Account",
        ]
    )

    with login_tab:

        show_school_login()

    with setup_tab:

        show_account_setup()
