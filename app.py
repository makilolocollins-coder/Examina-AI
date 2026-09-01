# ============================================================
# EXAMINA AI
# MAIN APPLICATION
# ============================================================

import streamlit as st

from database.database import (
    test_database_connection,
    get_states,
    get_lgas,
    create_school,
)

from auth.authentication import (
    initialize_auth,
    is_authenticated,
    logout_user,
)

from auth.login import show_login


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Examina AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# INITIALIZE AUTHENTICATION
# ============================================================

initialize_auth()


# ============================================================
# DATABASE CHECK
# ============================================================

def check_configuration():

    try:

        success, result = test_database_connection()

        return success, result

    except Exception as error:

        return False, str(error)


# ============================================================
# HOME PAGE
# ============================================================

def show_home():

    st.title("Examina AI 🎓")

    st.subheader(
        "Intelligent school management, academic records, "
        "examination results and secure digital learning."
    )

    st.write(
        "Examina AI brings school administration, student "
        "records, teachers, classes, subjects and examination "
        "management into one platform."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🏫 Register your school",
            use_container_width=True,
            type="primary",
        ):

            st.session_state["page"] = "register"

            st.rerun()

    with col2:

        if st.button(
            "🔐 Sign in",
            use_container_width=True,
        ):

            st.session_state["page"] = "login"

            st.rerun()

    st.divider()

    st.header("Everything your school needs")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.subheader("🏫 School Management")

        st.write(
            "Manage schools, teachers, students, "
            "classes and subjects."
        )

    with col2:

        st.subheader("📊 Academic Results")

        st.write(
            "Manage tests, examinations, grades, "
            "totals and student positions."
        )

    with col3:

        st.subheader("🤖 AI Examination")

        st.write(
            "Support handwritten examination scanning "
            "and intelligent marking."
        )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success("✓ Secure authentication")

    with col2:
        st.success("✓ School-level data isolation")

    with col3:
        st.success("✓ Controlled result publishing")

    st.divider()

    st.caption(
        "Examina AI · Intelligent School Management"
    )


# ============================================================
# SCHOOL REGISTRATION
# ============================================================

def show_register():

    st.title("🏫 Register Your School")

    st.write(
        "Create your school's Examina AI workspace."
    )

    st.divider()

    # ========================================================
    # SCHOOL INFORMATION
    # ========================================================

    st.subheader("School Information")

    school_name = st.text_input(
        "School name *",
        placeholder="Example: Bright Future College",
    )

    registration_number = st.text_input(
        "School registration number *",
        placeholder="Example: SCH-2026-001",
    )

    address = st.text_area(
        "School address",
        placeholder="Enter the full school address",
    )

    phone = st.text_input(
        "School phone number",
        placeholder="08012345678",
    )

    email = st.text_input(
        "School email",
        placeholder="school@example.com",
    )

    motto = st.text_input(
        "School motto",
        placeholder="Example: Knowledge Is Power",
    )

    st.divider()

    # ========================================================
    # SCHOOL LOCATION
    # ========================================================

    st.subheader("School Location")

    # --------------------------------------------------------
    # LOAD STATES
    # --------------------------------------------------------

    try:

        states = get_states()

    except Exception as error:

        st.error(
            "Unable to load Nigerian states."
        )

        with st.expander("Technical details"):

            st.code(str(error))

        return

    if not states:

        st.warning(
            "No states are currently available in the database."
        )

        return

    # --------------------------------------------------------
    # STATE
    # --------------------------------------------------------

    state_names = [
        state["name"]
        for state in states
        if state.get("name")
    ]

    if not state_names:

        st.error(
            "The states table contains no usable state names."
        )

        return

    selected_state_name = st.selectbox(
        "State *",
        state_names,
    )

    selected_state = next(
        (
            state
            for state in states
            if state.get("name")
            == selected_state_name
        ),
        None,
    )

    if selected_state is None:

        st.error(
            "Unable to identify the selected state."
        )

        return

    state_id = selected_state["id"]

    # --------------------------------------------------------
    # LOAD LGAs
    # --------------------------------------------------------

    try:

        lgas = get_lgas(state_id)

    except Exception as error:

        st.error(
            "Unable to load Local Government Areas."
        )

        with st.expander("Technical details"):

            st.code(str(error))

        return

    if not lgas:

        st.warning(
            "No Local Government Areas were found "
            "for this state."
        )

        return

    # --------------------------------------------------------
    # LGA
    # --------------------------------------------------------

    lga_names = [
        lga["name"]
        for lga in lgas
        if lga.get("name")
    ]

    if not lga_names:

        st.error(
            "The selected state has no usable LGA names."
        )

        return

    selected_lga_name = st.selectbox(
        "Local Government Area *",
        lga_names,
    )

    selected_lga = next(
        (
            lga
            for lga in lgas
            if lga.get("name")
            == selected_lga_name
        ),
        None,
    )

    if selected_lga is None:

        st.error(
            "Unable to identify the selected LGA."
        )

        return

    lga_id = selected_lga["id"]

    st.divider()

    # ========================================================
    # REGISTRATION
    # ========================================================

    if st.button(
        "🏫 Create School",
        use_container_width=True,
        type="primary",
    ):

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not school_name.strip():

            st.error(
                "School name is required."
            )

            return

        if not registration_number.strip():

            st.error(
                "School registration number is required."
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

                state=selected_state_name,

                local_government=(
                    selected_lga_name
                ),

                lga_id=lga_id,

                address=address.strip(),

                phone=phone.strip(),

                email=email.strip(),

                motto=motto.strip(),
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

            st.session_state["school_id"] = (
                school["id"]
            )

            st.session_state["school"] = school

            st.session_state["page"] = (
                "dashboard"
            )

            st.success(
                "School registered successfully."
            )

            st.rerun()

        else:

            st.error(
                "School registration returned no record."
            )

    st.write("")

    # ========================================================
    # BACK
    # ========================================================

    if st.button(
        "← Back to home",
        use_container_width=True,
    ):

        st.session_state["page"] = "home"

        st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

def show_dashboard():

    user = st.session_state.get(
        "user",
        {},
    )

    if isinstance(user, dict):

        email = user.get(
            "email",
            "User",
        )

    else:

        email = "User"

    st.title("Dashboard 🎓")

    st.write(
        f"Welcome, {email}"
    )

    st.divider()

    # ========================================================
    # SCHOOL INFORMATION
    # ========================================================

    school = st.session_state.get(
        "school"
    )

    if school:

        st.subheader(
            school.get(
                "name",
                "Your School",
            )
        )

        registration_number = school.get(
            "registration_number"
        )

        if registration_number:

            st.caption(
                f"Registration number: "
                f"{registration_number}"
            )

        location = []

        if school.get("local_government"):

            location.append(
                school["local_government"]
            )

        if school.get("state"):

            location.append(
                school["state"]
            )

        if location:

            st.caption(
                "Location: "
                + ", ".join(location)
            )

    # ========================================================
    # DASHBOARD METRICS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Students",
            "0",
        )

    with col2:

        st.metric(
            "Teachers",
            "0",
        )

    with col3:

        st.metric(
            "Classes",
            "0",
        )

    with col4:

        st.metric(
            "Subjects",
            "0",
        )

    st.divider()

    st.info(
        "Your Examina AI workspace is ready."
    )

    if st.button(
        "Logout",
        use_container_width=True,
    ):

        logout_user()

        st.session_state["page"] = "home"

        st.session_state.pop(
            "school_id",
            None,
        )

        st.session_state.pop(
            "school",
            None,
        )

        st.rerun()


# ============================================================
# APPLICATION ROUTER
# ============================================================

def main():

    # ========================================================
    # DATABASE CONNECTION CHECK
    # ========================================================

    success, result = check_configuration()

    if not success:

        st.error(
            "Unable to connect to the Examina database."
        )

        st.stop()

    # ========================================================
    # CURRENT PAGE
    # ========================================================

    page = st.session_state.get(
        "page",
        "home",
    )

    # ========================================================
    # LOGIN
    # ========================================================

    if page == "login":

        show_login()

        return

    # ========================================================
    # REGISTER
    # ========================================================

    if page == "register":

        show_register()

        return

    # ========================================================
    # DASHBOARD
    # ========================================================

    if page == "dashboard":

        if not is_authenticated():

            st.session_state["page"] = "login"

            st.rerun()

            return

        show_dashboard()

        return

    # ========================================================
    # HOME
    # ========================================================

    show_home()


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
