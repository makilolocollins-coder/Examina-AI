import streamlit as st

st.set_page_config(
    page_title="Examina AI",
    page_icon="🎓",
)

st.markdown(
    """
    <div style="
        background: #312e81;
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
    ">
        <h1>Examina AI 🎓</h1>
        <p>
            Intelligent school management,
            academic records and examination results.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
