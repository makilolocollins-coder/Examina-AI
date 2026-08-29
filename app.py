import streamlit as st


# ============================================================
# EXAMINA AI
# Main Application
# ============================================================

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
