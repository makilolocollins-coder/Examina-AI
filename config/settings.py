import streamlit as st


def get_supabase_config():
    """
    Read Supabase credentials from Streamlit Secrets.

    Never hardcode credentials in source code.
    """

    try:
        supabase_url = st.secrets["SUPABASE_URL"]
        supabase_key = st.secrets["SUPABASE_KEY"]
    except KeyError as exc:
        raise RuntimeError(
            "Missing Supabase configuration. "
            "Add SUPABASE_URL and SUPABASE_KEY to Streamlit Secrets."
        ) from exc

    if not supabase_url or not supabase_key:
        raise RuntimeError(
            "Supabase configuration is empty. "
            "Check Streamlit Secrets."
        )

    return supabase_url, supabase_key
