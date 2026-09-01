import streamlit as st
from supabase import create_client


@st.cache_resource
def get_supabase_client():

    database_url = st.secrets.get("DATABASE_URL")
    database_key = st.secrets.get("DATABASE_KEY")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is missing from Streamlit Secrets."
        )

    if not database_key:
        raise RuntimeError(
            "DATABASE_KEY is missing from Streamlit Secrets."
        )

    return create_client(
        database_url,
        database_key,
    )
