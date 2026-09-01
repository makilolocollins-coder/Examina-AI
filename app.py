# ============================================================
# EXAMINA AI
# SECURE SCHOOL MANAGEMENT & EXAMINATION PLATFORM
# ============================================================

import streamlit as st

from services.supabase_client import get_supabase_client
from auth.authentication import is_authenticated
from auth.login import show_login

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Examina AI | Intelligent School Management",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# SUPABASE CONNECTION
# ============================================================

@st.cache_resource
def init_supabase():
    """
    Initialize the Supabase client.

    Credentials are loaded only from Streamlit Secrets.
    No credentials are stored in the repository.
    """
    return get_supabase_client()


# ============================================================
# GLOBAL UI
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
        background:
            radial-gradient(
                circle at 85% 5%,
                rgba(91, 82, 255, 0.10),
                transparent 28%
            ),
            radial-gradient(
                circle at 5% 35%,
                rgba(34, 197, 94, 0.06),
                transparent 25%
            ),
            #f8fafc;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* ========================================================
       NAVIGATION
       ======================================================== */

    .exa-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.4rem 0 1.2rem 0;
        margin-bottom: 2rem;
    }

    .exa-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .exa-logo {
        width: 44px;
        height: 44px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(
            135deg,
            #111827,
            #3730a3
        );
        color: white;
        font-size: 22px;
        box-shadow:
            0 10px 25px rgba(49, 46, 129, 0.20);
    }

    .exa-brand-name {
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: #111827;
    }

    .exa-brand-ai {
        color: #4f46e5;
    }

    .exa-nav-tag {
        font-size: 0.78rem;
        font-weight: 600;
        color: #64748b;
        padding: 8px 13px;
        border: 1px solid #e2e8f0;
        background: rgba(255,255,255,0.75);
        border-radius: 999px;
    }

    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        position: relative;
        overflow: hidden;
        border-radius: 30px;
        padding: 4.5rem 4rem;
        background:
            radial-gradient(
                circle at 90% 20%,
                rgba(129, 140, 248, 0.22),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #0f172a 0%,
                #172554 50%,
                #312e81 100%
            );
        box-shadow:
            0 30px 70px rgba(15, 23, 42, 0.18);
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        right: -100px;
        bottom: -120px;
        border-radius: 50%;
        background: rgba(255,255,255,0.06);
    }

    .hero-eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 13px;
        border-radius: 999px;
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.14);
        color: #c7d2fe;
        font-size: 0.78rem;
        font-weight: 700;
        margin-bottom: 1.2rem;
    }

    .hero-title {
        color: white;
        font-size: clamp(2.5rem, 6vw, 4.8rem);
        line-height: 0.98;
        letter-spacing: -0.065em;
        font-weight: 800;
        max-width: 780px;
        margin: 0;
    }

    .hero-title span {
        color: #a5b4fc;
    }

    .hero-description {
        max-width: 690px;
        color: #cbd5e1;
        font-size: 1.05rem;
        line-height: 1.75;
        margin-top: 1.5rem;
    }

    .hero-note {
        margin-top: 1.5rem;
        color: #94a3b8;
        font-size: 0.82rem;
    }

    /* ========================================================
       SECTIONS
       ======================================================== */

    .section-label {
        color: #4f46e5;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .section-title {
        color: #0f172a;
        font-size: 2rem;
        line-height: 1.1;
        font-weight: 800;
        letter-spacing: -0.045em;
        margin-bottom: 0.5rem;
    }

    .section-description {
        color: #64748b;
        line-height: 1.7;
        max-width: 680px;
    }

    /* ========================================================
       FEATURE CARDS
       ======================================================== */

    .feature-card {
        height: 100%;
        padding: 1.6rem;
        border-radius: 22px;
        background: rgba(255,255,255,0.90);
        border: 1px solid #e2e8f0;
        box-shadow:
            0 12px 35px rgba(15, 23, 42, 0.055);
    }

    .feature-icon {
        width: 46px;
        height: 46px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 14px;
        background: #eef2ff;
        font-size: 21px;
        margin-bottom: 1rem;
    }

    .feature-title {
        color: #0f172a;
        font-size: 1.02rem;
        font-weight: 750;
        margin-bottom: 0.45rem;
    }

    .feature-text {
        color: #64748b;
        font-size: 0.88rem;
        line-height: 1.65;
    }

    /* ========================================================
       TRUST STRIP
       ======================================================== */

    .trust-strip {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        padding: 1.2rem 1.5rem;
        border-radius: 18px;
        background: white;
        border: 1px solid #e2e8f0;
        box-shadow:
            0 10px 30px rgba(15, 23, 42, 0.04);
    }

    .trust-item {
        display: flex;
        align-items: center;
        gap: 9px;
        color: #475569;
        font-size: 0.83rem;
        font-weight: 650;
    }

    .trust-check {
        color: #16a34a;
        font-weight: 900;
    }

    /* ========================================================
       CTA
       ======================================================== */

    .cta {
        text-align: center;
        padding: 3rem 2rem;
        border-radius: 28px;
        background: white;
        border: 1px solid #e2e8f0;
        box-shadow:
            0 20px 50px rgba(15, 23, 42, 0.07);
    }

    .cta-title {
        font-size: 2rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.045em;
    }

    .cta-text {
        color: #64748b;
        max-width: 600px;
        margin: 0.7rem auto 1.4rem auto;
        line-height: 1.7;
    }

    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        width: 100%;
        min-height: 48px;
        border-radius: 13px;
        font-weight: 700;
        border: 1px solid #e2e8f0;
        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow:
            0 10px 25px rgba(15, 23, 42, 0.10);
    }

    /* ========================================================
       FOOTER
       ======================================================== */

    .exa-footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.78rem;
        padding-top: 2rem;
    }

    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero {
            padding: 2.6rem 1.5rem;
            border-radius: 24px;
        }

        .hero-title {
            font-size: 2.65rem;
        }

        .hero-description {
            font-size: 0.95rem;
        }

        .trust-strip {
            flex-direction: column;
        }

        .exa-nav-tag {
            display: none;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# MAIN
# ============================================================

def main():

    # ========================================================
    # SUPABASE CONNECTION
    # ========================================================

    try:
        supabase = init_supabase()

        st.session_state["supabase_ready"] = (
            supabase is not None
        )

    except Exception:
        st.error(
            "The application configuration is incomplete. "
            "Please contact the system administrator."
        )
        st.stop()


    # ========================================================
    # PAGE ROUTING
    # ========================================================

    if st.session_state.get("page") == "login":
        show_login()
        st.stop()


    # ========================================================
    # NAVIGATION
    # ========================================================

    st.markdown(
        """
        <div class="exa-nav">

            <div class="exa-brand">

                <div class="exa-logo">
                    🎓
                </div>

                <div class="exa-brand-name">
                    Examina
                    <span class="exa-brand-ai">AI</span>
                </div>

            </div>

            <div class="exa-nav-tag">
                Intelligent School Management
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # HERO
    # ========================================================

    st.markdown(
        """
        <section class="hero">

            <div class="hero-eyebrow">
                ✦ Built for modern schools
            </div>

            <h1 class="hero-title">
                Run your school.<br>
                <span>Smarter.</span>
            </h1>

            <p class="hero-description">
                Examina AI brings student records, teachers,
                classes, results, approvals and professional
                report cards into one secure school management
                platform.
            </p>

            <p class="hero-note">
                Secure by design · Role-based access ·
                School-controlled data
            </p>

        </section>
        """,
        unsafe_allow_html=True,
    )


    st.write("")


    # ========================================================
    # PRIMARY ACTIONS
    # ========================================================

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:

        if st.button(
            "🏫  Register your school",
            use_container_width=True,
        ):
            st.session_state["page"] = "register"
            st.rerun()


    with col2:

        if st.button(
            "🔐  Sign in",
            use_container_width=True,
        ):
            st.session_state["page"] = "login"
            st.rerun()


    with col3:

        if st.button(
            "ℹ️  How Examina works",
            use_container_width=True,
        ):
            st.session_state["page"] = "about"
            st.rerun()


    # ========================================================
    # FEATURES
    # ========================================================

    st.write("")

    st.markdown(
        """
        <div style="
            margin-top:2.5rem;
            margin-bottom:1.4rem;
        ">

            <div class="section-label">
                One platform
            </div>

            <div class="section-title">
                Everything your school needs.
            </div>

            <div class="section-description">
                From registration to final report cards,
                Examina is designed around the real workflow
                of modern schools.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    features = [

        (
            "🏫",
            "School Management",
            "Manage your school's identity, classes, "
            "teachers, students and academic structure "
            "from one workspace.",
        ),

        (
            "📊",
            "Spreadsheet Results",
            "Teachers enter continuous assessment "
            "and examination scores in a familiar "
            "spreadsheet-style workflow.",
        ),

        (
            "✅",
            "Principal Approval",
            "Results move through a controlled approval "
            "process before becoming visible to students.",
        ),

        (
            "🔐",
            "Private by Design",
            "Role-based access and database-level "
            "security keep school information separated.",
        ),

        (
            "👨‍🎓",
            "Student Portal",
            "Students access their own published academic "
            "results without exposing other students' data.",
        ),

        (
            "📄",
            "Professional Reports",
            "Generate branded report cards using the "
            "school logo, motto, address and student photo.",
        ),
    ]


    feature_cols = st.columns(3)


    for index, feature in enumerate(features):

        icon, title, description = feature

        with feature_cols[index % 3]:

            st.markdown(
                f"""
                <div class="feature-card">

                    <div class="feature-icon">
                        {icon}
                    </div>

                    <div class="feature-title">
                        {title}
                    </div>

                    <div class="feature-text">
                        {description}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

        if index % 3 == 2:
            st.write("")


    # ========================================================
    # TRUST
    # ========================================================

    st.write("")

    st.markdown(
        """
        <div class="trust-strip">

            <div class="trust-item">
                <span class="trust-check">✓</span>
                School-level data isolation
            </div>

            <div class="trust-item">
                <span class="trust-check">✓</span>
                Role-based permissions
            </div>

            <div class="trust-item">
                <span class="trust-check">✓</span>
                Principal-controlled publishing
            </div>

            <div class="trust-item">
                <span class="trust-check">✓</span>
                Secure authentication
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # CTA
    # ========================================================

    st.write("")

    st.markdown(
        """
        <div class="cta">

            <div class="cta-title">
                Ready to bring your school online?
            </div>

            <div class="cta-text">
                Create your school's secure Examina
                workspace and start managing academic
                information in one place.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown(
        """
        <div class="exa-footer">

            Examina AI · Intelligent School Management

            <br>

            Secure academic administration for modern schools

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
