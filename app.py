# ============================================================
# EXAMINA AI
# MAIN APPLICATION
# ============================================================

import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Examina AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

try:
    from database.database import create_database

    create_database()

except Exception as error:
    st.error("Database initialization failed.")
    st.exception(error)
    st.stop()


# ============================================================
# APPLICATION HEADER
# ============================================================

st.title("🎓 Examina AI")

st.caption(
    "AI-Powered Education Platform"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎓 Examina AI")

st.sidebar.caption(
    "AI-Powered Education Platform"
)

st.sidebar.divider()


page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "📝 Exam Scanner",
        "🤖 AI Teacher",
        "🔍 Question Solver",
        "📚 Courses",
        "👨‍🏫 Tutors",
        "🏫 Schools",
        "📊 Results",
        "👨‍🏫 Teacher Portal",
        "🏫 Principal Portal",
        "🎓 Student Portal",
        "👤 Profile",
    ],
)


st.sidebar.divider()

st.sidebar.caption(
    "Examina AI • Education Technology"
)


# ============================================================
# PAGE LOADER
# ============================================================

def load_page(module_name, function_name="show"):
    """
    Safely import and execute a page.

    This prevents one broken page from making it appear
    that the whole application is only showing Home.
    """

    try:

        module = __import__(
            module_name,
            fromlist=[function_name],
        )

        page_function = getattr(
            module,
            function_name,
        )

        page_function()

    except ModuleNotFoundError as error:

        st.error(
            f"Page module could not be found: "
            f"`{module_name}`"
        )

        st.exception(error)

    except AttributeError as error:

        st.error(
            f"The page `{module_name}` does not contain "
            f"the function `{function_name}()`."
        )

        st.exception(error)

    except Exception as error:

        st.error(
            f"Error loading `{module_name}`."
        )

        st.exception(error)


# ============================================================
# PAGE ROUTING
# ============================================================


if page == "🏠 Home":

    load_page(
        "pages.home",
        "show",
    )


elif page == "📝 Exam Scanner":

    load_page(
        "pages.exam_scanner",
        "show",
    )


elif page == "🤖 AI Teacher":

    load_page(
        "pages.ai_teacher",
        "show",
    )


elif page == "🔍 Question Solver":

    load_page(
        "pages.question_solver",
        "show",
    )


elif page == "📚 Courses":

    load_page(
        "pages.courses",
        "show",
    )


elif page == "👨‍🏫 Tutors":

    load_page(
        "pages.tutors",
        "show",
    )


elif page == "🏫 Schools":

    load_page(
        "pages.schools",
        "show",
    )


elif page == "📊 Results":

    load_page(
        "pages.results",
        "show",
    )


elif page == "👨‍🏫 Teacher Portal":

    load_page(
        "pages.teacher_portal",
        "show_teacher_portal",
    )


elif page == "🏫 Principal Portal":

    load_page(
        "pages.principal_portal",
        "show_principal_portal",
    )


elif page == "🎓 Student Portal":

    load_page(
        "pages.student_portal",
        "show_student_portal",
    )


elif page == "👤 Profile":

    load_page(
        "pages.profile",
        "show",
    )
