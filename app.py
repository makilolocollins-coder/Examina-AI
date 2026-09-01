# ============================================================
# EXAMINA AI
# MAIN APPLICATION
# ============================================================

import streamlit as st

from pages.register import show_register


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Examina AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# GLOBAL DESIGN
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       TYPOGRAPHY
    ======================================================== */

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;750;800&display=swap'
    );

    html,
    body,
    [class*="css"] {
        font-family: "Inter", sans-serif;
    }


    /* ========================================================
       APP BACKGROUND
    ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 85% 5%,
                rgba(79, 70, 229, 0.055),
                transparent 28%
            ),
            #f8fafc;
    }


    /* ========================================================
       MAIN CONTAINER
    ======================================================== */

    .block-container {
        max-width: 1050px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ========================================================
       REMOVE STREAMLIT CHROME
    ======================================================== */

    #MainMenu {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ========================================================
       TEXT SELECTION
    ======================================================== */

    ::selection {
        background: rgba(79, 70, 229, 0.15);
    }


    /* ========================================================
       BUTTONS
    ======================================================== */

    .stButton > button {

        min-height: 46px;

        border-radius: 11px;

        font-family: "Inter", sans-serif;

        font-weight: 700;

        transition:
            transform 120ms ease,
            box-shadow 120ms ease,
            border-color 120ms ease;

    }


    .stButton > button:hover {

        transform: translateY(-1px);

        box-shadow:
            0 8px 22px rgba(15, 23, 42, 0.08);

    }


    .stButton > button:active {

        transform: translateY(0);

    }


    /* ========================================================
       INPUTS
    ======================================================== */

    .stTextInput input,
    .stTextArea textarea {

        border-radius: 10px !important;

        border-color: #cbd5e1 !important;

        background: #ffffff !important;

        font-family: "Inter", sans-serif !important;

    }


    .stTextInput input:focus,
    .stTextArea textarea:focus {

        border-color: #6366f1 !important;

        box-shadow:
            0 0 0 1px #6366f1 !important;

    }


    /* ========================================================
       SELECTBOX
    ======================================================== */

    .stSelectbox div[data-baseweb="select"] {

        border-radius: 10px !important;

    }


    /* ========================================================
       LABELS
    ======================================================== */

    label {

        color: #334155 !important;

        font-weight: 650 !important;

    }


    /* ========================================================
       DIVIDERS
    ======================================================== */

    hr {

        border-color: #e2e8f0 !important;

    }


    /* ========================================================
       ALERTS
    ======================================================== */

    .stAlert {

        border-radius: 12px !important;

    }


    /* ========================================================
       RESPONSIVE
    ======================================================== */

    @media (max-width: 700px) {

        .block-container {

            padding-left: 1rem;

            padding-right: 1rem;

            padding-top: 1.25rem;

        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# APPLICATION
# ============================================================

def main():

    show_register()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()
