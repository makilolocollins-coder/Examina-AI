# ============================================================
# EXAMINA AI
# SCHOOL PORTAL
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

    st.title("Create School Account")

    st.caption(
        "Create the login account for your approved school."
    )

    st.info(
        "Your school must already be approved by "
        "Examina AI before an account can be created."
    )

    with st.form("school_account_setup"):

        registration_number = st.text_input(
            "School Registration Number"
        )

        email = st.text_input(
            "Registered School Email"
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
            use_container_width=True,
        )


    if not submitted:

        return


    # --------------------------------------------------------
    # CLEAN INPUT
    # --------------------------------------------------------

    registration_number = registration_number.strip()

    email = email.strip().lower()


    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

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
    # VERIFY SCHOOL
    # --------------------------------------------------------

    try:

        school = get_school_account_eligibility(
            registration_number,
            email,
        )

    except Exception as error:

        st.error(
            f"Could not verify school: {error}"
        )

        return


    if not school:

        st.error(
            "We could not find an approved school "
            "matching that registration number and "
            "registered email."
        )

        return


    school_id = school["school_id"]

    school_name = school["school_name"]


    # --------------------------------------------------------
    # CREATE ACCOUNT
    # --------------------------------------------------------

    try:

        response = create_school_account(
            email=email,
            password=password,
            school_id=school_id,
        )

        user = getattr(
            response,
            "user",
            None,
        )

        session = getattr(
            response,
            "session",
            None,
        )


        if not user:

            st.error(
                "The school account could not be created."
            )

            return


        # ----------------------------------------------------
        # SESSION AVAILABLE
        # ----------------------------------------------------

        if session:

            profile = get_school_user_profile(
                user.id
            )


            if not profile:

                logout_user()

                st.error(
                    "The account was created, "
                    "but it could not be linked to the school."
                )

                return


            st.session_state.school_authenticated = True

            st.session_state.school_user = profile

            st.success(
                f"{school_name} account created successfully."
            )

            st.rerun()


        # ----------------------------------------------------
        # EMAIL CONFIRMATION REQUIRED
        # ----------------------------------------------------

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

    st.title("School Login")

    st.caption(
        "Sign in to access your Examina AI school portal."
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
            use_container_width=True,
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


    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    try:

        response = login_school(
            email,
            password,
        )

        user = getattr(
            response,
            "user",
            None,
        )


        if not user:

            st.error(
                "Login failed."
            )

            return


        # ----------------------------------------------------
        # GET SCHOOL PROFILE
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # STORE LOGIN STATE
        # ----------------------------------------------------

        st.session_state.school_authenticated = True

        st.session_state.school_user = profile

        st.rerun()


    except Exception as error:

        st.error(
            f"Login failed: {error}"
        )


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
    # SCHOOL PORTAL MENU
    # ========================================================

    st.title("🏫 School Portal")

    st.caption(
        "Register your school, create your account, "
        "or sign in."
    )

    st.divider()


    # ========================================================
    # THREE OPTIONS
    # ========================================================

    col1, col2, col3 = st.columns(3)


    # --------------------------------------------------------
    # REGISTER SCHOOL
    # --------------------------------------------------------

    with col1:

        st.subheader(
            "📝 Register School"
        )

        st.write(
            "Register your school for verification "
            "and approval."
        )

        if st.button(
            "Register for Approval",
            use_container_width=True,
        ):

            st.session_state.portal = "register"

            st.rerun()


    # --------------------------------------------------------
    # CREATE ACCOUNT
    # --------------------------------------------------------

    with col2:

        st.subheader(
            "🔐 Create Account"
        )

        st.write(
            "Create a login account after your school "
            "has been approved."
        )

        if st.button(
            "Create School Account",
            use_container_width=True,
        ):

            st.session_state.school_portal_page = (
                "account_setup"
            )

            st.rerun()


    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    with col3:

        st.subheader(
            "🚪 School Login"
        )

        st.write(
            "Sign in to your existing school account."
        )

        if st.button(
            "School Login",
            use_container_width=True,
        ):

            st.session_state.school_portal_page = (
                "login"
            )

            st.rerun()


    # ========================================================
    # SCHOOL PORTAL PAGE
    # ========================================================

    school_page = st.session_state.get(
        "school_portal_page",
        None,
    )


    # ========================================================
    # ACCOUNT SETUP
    # ========================================================

    if school_page == "account_setup":

        st.divider()

        if st.button(
            "← Back to School Portal",
        ):

            st.session_state.school_portal_page = None

            st.rerun()

        show_account_setup()


    # ========================================================
    # LOGIN
    # ========================================================

    elif school_page == "login":

        st.divider()

        if st.button(
            "← Back to School Portal",
        ):

            st.session_state.school_portal_page = None

            st.rerun()

        show_school_login()
