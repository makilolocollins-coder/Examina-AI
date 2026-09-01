# ============================================================
# EXAMINA AI
# AUTHENTICATION STATE
# ============================================================

import streamlit as st


# ============================================================
# INITIALIZE AUTHENTICATION
# ============================================================

def initialize_auth():

    if "authenticated" not in st.session_state:

        st.session_state["authenticated"] = False

    if "user" not in st.session_state:

        st.session_state["user"] = None

    if "page" not in st.session_state:

        st.session_state["page"] = "home"


# ============================================================
# CHECK AUTHENTICATION
# ============================================================

def is_authenticated():

    return st.session_state.get(
        "authenticated",
        False,
    )


# ============================================================
# LOGIN
# ============================================================

def login_user(user):

    st.session_state["authenticated"] = True

    st.session_state["user"] = user


# ============================================================
# LOGOUT
# ============================================================

def logout_user():

    st.session_state["authenticated"] = False

    st.session_state["user"] = None

    st.session_state["page"] = "home"
