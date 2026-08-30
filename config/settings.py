import os

import streamlit as st
from dotenv import load_dotenv


load_dotenv()


def get_database_url() -> str:

    # --------------------------------------------------------
    # Streamlit Cloud
    # --------------------------------------------------------

    try:
        database_url = st.secrets.get("DATABASE_URL")

    except Exception:
        database_url = None

    # --------------------------------------------------------
    # Local development
    # --------------------------------------------------------

    if not database_url:
        database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not configured. "
            "Add DATABASE_URL to Streamlit Secrets "
            "or your local .env file."
        )

    database_url = str(database_url).strip()

    # --------------------------------------------------------
    # Remove accidental surrounding quotes
    # --------------------------------------------------------

    if (
        len(database_url) >= 2
        and database_url[0] == '"'
        and database_url[-1] == '"'
    ):
        database_url = database_url[1:-1]

    if (
        len(database_url) >= 2
        and database_url[0] == "'"
        and database_url[-1] == "'"
    ):
        database_url = database_url[1:-1]

    # --------------------------------------------------------
    # Supabase PostgreSQL URL
    # --------------------------------------------------------

    if database_url.startswith(
        "postgres://"
    ):
        database_url = database_url.replace(
            "postgres://",
            "postgresql://",
            1,
        )

    return database_url


DATABASE_URL = get_database_url()
