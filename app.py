import streamlit as st


# ============================================================
# EXAMINA AI
# Main Application
# ============================================================

from database.database import create_database

create_database()

st.set_page_config(
    page_title="Examina AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# APPLICATION HEADER
# ============================================================

st.title("🎓 Examina AI")

st.subheader("AI-Powered Education Platform")

st.write(
    "Examina AI brings examination tools, AI learning, "
    "question solving, tutors, courses, and school management "
    "into one platform."
)

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("🎓 Examina AI")

st.sidebar.write("Navigate")

page = st.sidebar.radio(
    "Select a section",
    [
        "🏠 Home",
        "📝 Exam Scanner",
        "🤖 AI Teacher",
        "🔍 Question Solver",
        "📚 Courses",
        "👨‍🏫 Tutors",
        "🏫 Schools",
        "📊 Results",
        "👤 Profile"
    ]
)

# ============================================================
# PAGE ROUTING
# ============================================================
 # ================================================================

if page == "🏠 Home":
    from pages.home import show
    show()

elif page == "📝 Exam Scanner":
    from pages.exam_scanner import show
    show()

elif page == "🤖 AI Teacher":
    from pages.ai_teacher import show
    show()

elif page == "🔍 Question Solver":
    from pages.question_solver import show
    show()

elif page == "📚 Courses":
    from pages.courses import show
    show()

elif page == "👨‍🏫 Tutors":
    from pages.tutors import show
    show()

elif page == "🏫 Schools":
    from pages.schools import show
    show()

elif page == "📊 Results":
    from pages.results import show
    show()

elif page == "👤 Profile":
    from pages.profile import show
    show()
