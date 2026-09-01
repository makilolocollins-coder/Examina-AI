# ============================================================
# EXAMINA AI
# SUPABASE CLIENT
# ============================================================

import os

import streamlit as st
from supabase import create_client


# ============================================================
# GET CREDENTIALS
# ============================================================

def get_supabase_credentials():

    # --------------------------------------------------------
    # STREAMLIT SECRETS
    # --------------------------------------------------------

    try:

        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]

        if url and key:

            return url, key

    except Exception:
        pass


    # --------------------------------------------------------
    # ENVIRONMENT VARIABLES
    # --------------------------------------------------------

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url:

        raise RuntimeError(
            "SUPABASE_URL is missing."
        )

    if not key:

        raise RuntimeError(
            "SUPABASE_KEY is missing."
        )

    return url, key


# ============================================================
# CREATE CLIENT
# ============================================================

@st.cache_resource
def get_supabase_client():

    url, key = get_supabase_credentials()

    return create_client(
        url,
        key,
    )
