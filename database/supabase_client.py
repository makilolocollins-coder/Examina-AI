# ============================================================
# EXAMINA AI
# SUPABASE CLIENT
# ============================================================

import streamlit as st

from supabase import create_client


# ============================================================
# GET SUPABASE CLIENT
# ============================================================

@st.cache_resource
def get_supabase_client():

    try:

        database_url = st.secrets["DATABASE_URL"]
        database_key = st.secrets["DATABASE_KEY"]

    except KeyError as error:

        missing_key = error.args[0]

        raise RuntimeError(
            f"Streamlit Secret '{missing_key}' is missing."
        )

    if not database_url:

        raise RuntimeError(
            "DATABASE_URL is empty."
        )

    if not database_key:

        raise RuntimeError(
            "DATABASE_KEY is empty."
        )

    return create_client(
        database_url,
        database_key,
    )
