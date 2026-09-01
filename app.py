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
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {
        font-family: "Inter", sans-serif;
    }

    .stApp {
        background: #f8fafc;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

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
       BRAND
       ======================================================== */

    .exa-brand {
        display: flex;
        align-items: center;
        gap: 11px;
        margin-bottom: 3rem;
    }

    .exa-mark {
        width: 42px;
        height: 42px;
        border-radius: 12px;

        display: flex;
        align-items: center;
        justify-content: center;

        background: #111827;
        color: white;

        font-size: 20px;

        box-shadow:
            0 8px 20px rgba(15, 23, 42, 0.12);
    }

    .exa-name {
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: #111827;
    }

    .exa-ai {
        color: #4f46e5;
    }

    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1rem;
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

    # --------------------------------------------------------
    # REGISTRATION IS THE FIRST PAGE
    # --------------------------------------------------------

    show_register()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()
