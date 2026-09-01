# ============================================================
# EXAMINA AI
# SUPABASE CLIENT
# ============================================================

import streamlit as st
from supabase import create_client, Client


# ============================================================
# GET SUPABASE CLIENT
# ============================================================

def get_supabase_client() -> Client:

    try:
        supabase_url = st.secrets["SUPABASE_URL"]
        supabase_key = st.secrets["SUPABASE_KEY"]

    except KeyError as error:
        raise RuntimeError(
            "The application configuration is incomplete. "
            "Please add SUPABASE_URL and SUPABASE_KEY "
            "to Streamlit Secrets."
        ) from error

    if not supabase_url:
        raise RuntimeError(
            "SUPABASE_URL is empty."
        )

    if not supabase_key:
        raise RuntimeError(
            "SUPABASE_KEY is empty."
        )

    try:
        supabase = create_client(
            supabase_url,
            supabase_key,
        )

        return supabase

    except Exception as error:
        raise RuntimeError(
            f"Failed to connect to Supabase: {error}"
        ) from error
