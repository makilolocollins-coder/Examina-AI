import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_database_url():
    value = None

    # Streamlit Cloud
    try:
        value = st.secrets.get("DATABASE_URL")
    except Exception:
        pass

    # Local fallback
    if not value:
        value = os.getenv("DATABASE_URL")

    if not value:
        raise RuntimeError("DATABASE_URL is missing.")

    value = str(value).strip()

    # Remove accidental surrounding quotes
    if len(value) >= 2:
        if value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1].strip()

    # Convert old PostgreSQL scheme
    if value.startswith("postgres://"):
        value = "postgresql://" + value[len("postgres://"):]

    return value


DATABASE_URL = get_database_url()
