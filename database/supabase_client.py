import streamlit as st
from supabase import create_client


@st.cache_resource
def get_supabase_client():

    try:
        supabase_url = st.secrets["SUPABASE_URL"]
        supabase_key = st.secrets["SUPABASE_KEY"]

    except KeyError as error:

        raise RuntimeError(
            f"{error.args[0]} is missing. "
            "Check that Streamlit Secrets contains "
            "SUPABASE_URL and SUPABASE_KEY."
        )

    if not supabase_url:

        raise RuntimeError(
            "SUPABASE_URL is missing."
        )

    if not supabase_key:

        raise RuntimeError(
            "SUPABASE_KEY is missing."
        )

    return create_client(
        supabase_url,
        supabase_key,
    )
