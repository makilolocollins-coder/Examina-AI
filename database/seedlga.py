import json
import os
import sys
from pathlib import Path

from supabase import create_client


# ============================================================
# EXAMINA AI
# NIGERIA ADMINISTRATIVE DATA SEEDER
# ============================================================

def get_supabase_credentials():

    # First try Streamlit Secrets
    try:
        import streamlit as st

        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]

        if url and key:
            return url, key

    except Exception:
        pass


    # Then try environment variables
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if url and key:
        return url, key


    raise RuntimeError(
        "Supabase credentials are missing. "
        "Configure SUPABASE_URL and SUPABASE_KEY."
    )


SUPABASE_URL, SUPABASE_KEY = (
    get_supabase_credentials()
)


BASE_DIR = Path(__file__).resolve().parent

JSON_FILE = BASE_DIR / "all-lga.json"


supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
)
