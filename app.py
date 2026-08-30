import streamlit as st

from database.database import create_database


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Examina AI",
    page_icon="🎓",
    layout="wide",
)


# ============================================================
# DATABASE
# ============================================================

try:

    create_database()

except Exception as error:

    st.error(
        "Unable to connect to the Examina AI database."
    )

    st.code(
        str(error)
    )

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.title("🎓 Examina AI")

st.subheader(
    "AI-Powered School Examination & Assessment Platform"
)

st.success(
    "Database connection successful."
)


# ============================================================
# STATUS
# ============================================================

st.write(
    "Examina AI v2 database foundation is ready."
)

st.info(
    "Next stage: authentication and school registration."
)
