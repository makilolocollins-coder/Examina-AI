# ============================================================
# EXAMINA AI
# MAIN APPLICATION
# ============================================================

import streamlit as st

from database.database import test_database_connection

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
# INITIALIZE AUTHENTICATION
# ============================================================

initialize_auth()


# ============================================================
# GLOBAL STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GENERAL
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 85% 5%,
                rgba(79, 70, 229, 0.08),
                transparent 28%
            ),
            radial-gradient(
                circle at 5% 35%,
                rgba(34, 197, 94, 0.05),
                transparent 25%
            ),
            #f8fafc;
    }

    .block-container {
        max-width: 1180px;
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


    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        position: relative;
        overflow: hidden;

        padding: 4rem 3rem;

        border-radius: 28px;

        background:
            radial-gradient(
                circle at 90% 20%,
                rgba(129, 140, 248, 0.22),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #0f172a 0%,
                #172554 50%,
                #312e81 100%
            );

        box-shadow:
            0 25px 60px rgba(15, 23, 42, 0.15);

        margin-bottom: 2rem;
    }


    .hero h1 {
        color: white;

        font-size: clamp(
            2.5rem,
            6vw,
            4.5rem
        );

        line-height: 1;

        letter-spacing: -0.06em;

        font-weight: 800;

        margin: 0 0 1rem 0;
    }


    .hero p {
        color: #cbd5e1;

        font-size: 1.05rem;

        line-height: 1.7;

        max-width: 700px;

        margin: 0;
    }


    /* ========================================================
       SECTION
       ======================================================== */

    .section-title {
        color: #0f172a;

        font-size: 2rem;

        font-weight: 800;

        letter-spacing: -0.04em;

        margin-top: 2rem;

        margin-bottom: 0.5rem;
    }


    .section-description {
        color: #64748b;

        line-height: 1.7;

        margin-bottom: 1.5rem;
    }


    /* ========================================================
       FEATURE CARDS
       ======================================================== */

    .feature {
        height: 100%;

        padding: 1.5rem;

        border-radius: 20px;

        background: white;

        border: 1px solid #e2e8f0;

        box-shadow:
            0 10px 30px rgba(
                15,
                23,
                42,
                0.05
            );
    }


    .feature h3 {
        color: #0f172a;

        font-size: 1.05rem;

        font-weight: 750;

        margin-bottom: 0.5rem;
    }


    .feature p {
        color: #64748b;

        font-size: 0.9rem;

        line-height: 1.6;

        margin: 0;
    }


    /* ========================================================
       DASHBOARD
       ======================================================== */

    .dashboard-header {
        padding: 2rem;

        border-radius: 24px;

        background: white;

        border: 1px solid #e2e8f0;

        margin-bottom: 1.5rem;
    }


    .dashboard-header h1 {
        margin: 0;

        color: #0f172a;

        font-weight: 800;
    }


    .dashboard-header p {
        color: #64748b;

        margin-top: 0.5rem;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .exa-footer {
        text-align: center;

        color: #94a3b8;

        font-size: 0.78rem;

        padding-top: 3rem;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        min-height: 48px;

        border-radius: 13px;

        font-weight: 700;

        border: 1px solid #e2e8f0;

        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease;
    }


    .stButton > button:hover {
        transform: translateY(-1px);

        box-shadow:
            0 10px 25px
            rgba(15, 23, 42, 0.10);
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero {
            padding: 2.5rem 1.5rem;

            border-radius: 22px;
        }

        .hero h1 {
            font-size: 2.7rem;
        }

        .hero p {
            font-size: 0.95rem;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATABASE CONFIGURATION CHECK
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

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    st.markdown(
        """
        <section class="hero">

            <h1>
                Examina AI 🎓
            </h1>

            <p>
                Intelligent school management,
                academic records, examination results
                and secure digital learning in one platform.
            </p>

        </section>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # PRIMARY ACTIONS
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # FEATURES
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="section-title">
            Everything your school needs
        </div>

        <div class="section-description">
            Examina AI brings school administration,
            academic records and examination management
            together in one secure platform.
        </div>
        """,
        unsafe_allow_html=True,
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            """
            <div class="feature">

                <h3>
                    🏫 School Management
                </h3>

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

                <h3>
                    📊 Academic Results
                </h3>

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

                <h3>
                    🤖 AI Examination
                </h3>

                <p>
                    Scan handwritten answer sheets
                    and support intelligent marking.
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )


    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="exa-footer">

            Examina AI · Intelligent School Management

            <br>

            Secure academic administration
            for modern schools.

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
        {},
    )


    email = (
        user.get("email", "User")
        if isinstance(user, dict)
        else "User"
    )


    st.markdown(
        f"""
        <div class="dashboard-header">

            <h1>
                Dashboard
            </h1>

            <p>
                Welcome, {email}
            </p>

        </div>
        """,
        unsafe_allow_html=True,
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
        "School management modules will appear here."
    )


    if st.button(
        "Logout",
        use_container_width=True,
    ):

        logout_user()

        st.session_state["page"] = "home"

        st.rerun()


# ============================================================
# SCHOOL REGISTRATION
# ============================================================

def show_register():

    st.title(
        "Register your school"
    )


    st.info(
        "School registration will be connected "
        "to the Supabase school tables here."
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
    # TEST DATABASE CONNECTION
    # --------------------------------------------------------

    success, result = check_configuration()


    if not success:

        st.error(
            "Supabase connection failed."
        )

        st.code(
            str(result)
        )

        st.warning(
            "Check that your Streamlit Secrets "
            "contain DATABASE_URL and DATABASE_KEY."
        )

        st.stop()


    # --------------------------------------------------------
    # CURRENT PAGE
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

            return


        show_dashboard()

        return


    # --------------------------------------------------------
    # REGISTER
    # --------------------------------------------------------

    if page == "register":

        show_register()

        return


    # --------------------------------------------------------
    # HOME
    # --------------------------------------------------------

    show_home()


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
