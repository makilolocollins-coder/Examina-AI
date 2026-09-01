# ============================================================
# EXAMINA AI
# MAIN APPLICATION
# ============================================================

import streamlit as st

from database.supabase_client import get_supabase_client

from database.database import (
    test_database_connection,
)

from auth.authentication import (
    initialize_auth,
    is_authenticated,
    logout_user,
)

from auth.login import show_login


# ============================================================
# PAGE CONFIGURATION
# MUST BE THE FIRST STREAMLIT COMMAND
# ============================================================

st.set_page_config(
    page_title="Examina AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# INITIALIZE SESSION
# ============================================================

initialize_auth()


# ============================================================
# DATABASE CONNECTION
# ============================================================

def check_configuration():

    success, result = (
        test_database_connection()
    )

    return success, result


# ============================================================
# GLOBAL STYLING
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f8fafc;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    .hero {
        padding: 4rem;
        border-radius: 28px;
        background:
            linear-gradient(
                135deg,
                #0f172a,
                #172554,
                #312e81
            );
        color: white;
    }

    .hero h1 {
        font-size: 3.5rem;
        margin-bottom: 1rem;
    }

    .hero p {
        font-size: 1.1rem;
        color: #cbd5e1;
        max-width: 700px;
        line-height: 1.7;
    }

    .feature {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 1.5rem;
        min-height: 180px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HOME PAGE
# ============================================================

def show_home():

    st.markdown(
        """
        <div class="hero">

            <h1>
                Examina AI 🎓
            </h1>

            <p>
                Intelligent school management,
                academic records, examination results
                and secure digital learning in one platform.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.write("")


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "🏫 Register your school",
            use_container_width=True,
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


    st.write("")
    st.write("")


    st.subheader(
        "Everything your school needs"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            """
            <div class="feature">
                <h3>🏫 School Management</h3>
                <p>
                    Manage students, teachers,
                    classes and subjects.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


    with col2:

        st.markdown(
            """
            <div class="feature">
                <h3>📊 Results</h3>
                <p>
                    Manage tests, examinations,
                    grades and student positions.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


    with col3:

        st.markdown(
            """
            <div class="feature">
                <h3>🤖 AI Examination</h3>
                <p>
                    Scan handwritten answer sheets
                    and support intelligent marking.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# DASHBOARD
# ============================================================

def show_dashboard():

    user = st.session_state.get(
        "user",
        {}
    )


    st.title("Dashboard")

    st.write(
        f"Welcome, {user.get('email', 'User')}"
    )


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


    st.write("")
    st.info(
        "Your Examina AI workspace is ready. "
        "We will now build the school registration "
        "and management modules."
    )


    if st.button("Logout"):

        logout_user()

        st.rerun()


# ============================================================
# REGISTRATION PLACEHOLDER
# ============================================================

def show_register():

    st.title(
        "Register your school"
    )

    st.info(
        "The school registration module is the next "
        "section we will connect to your Supabase tables."
    )


    if st.button(
        "← Back",
        use_container_width=True,
    ):

        st.session_state["page"] = "home"

        st.rerun()


# ============================================================
# APPLICATION ROUTER
# ============================================================

def main():

    # --------------------------------------------------------
    # CHECK SUPABASE
    # --------------------------------------------------------

    success, result = (
        check_configuration()
    )


    if not success:

        st.error(
            "Supabase connection failed."
        )

        st.code(
            str(result)
        )

        st.info(
            "Check that Streamlit Secrets contains "
            "SUPABASE_URL and SUPABASE_KEY."
        )

        st.stop()


    # --------------------------------------------------------
    # GET PAGE
    # --------------------------------------------------------

    page = st.session_state.get(
        "page",
        "home",
    )


    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    if page == "login":

        show_login()

        return


    # --------------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------------

    if page == "dashboard":

        if not is_authenticated():

            st.session_state["page"] = "login"

            st.rerun()


        show_dashboard()

        return


    # --------------------------------------------------------
    # SCHOOL REGISTRATION
    # --------------------------------------------------------

    if page == "register":

        show_register()

        return


    # --------------------------------------------------------
    # HOME
    # --------------------------------------------------------

    show_home()


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    main()
