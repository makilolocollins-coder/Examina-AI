import streamlit as st

from config.settings import DATABASE_URL

st.title("Examina AI")

st.write("Database configuration test")

st.write(
    "DATABASE_URL detected:",
    bool(DATABASE_URL)
)

st.write(
    "Starts with postgresql://:",
    DATABASE_URL.startswith("postgresql://")
)

st.write(
    "Starts with postgres://:",
    DATABASE_URL.startswith("postgres://")
)

st.write(
    "URL length:",
    len(DATABASE_URL)
)
