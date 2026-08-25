
import streamlit as st

st.set_page_config(
    page_title="AYANFE Input Test",
    page_icon="🧠",
    layout="wide"
)

st.markdown(
    """
    <style>

    .test-input-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;

        padding: 12px 18px;

        background: white;

        border-top: 1px solid #ddd;

        z-index: 999;
    }

    .test-label {
        text-align: center;
        color: #777;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


st.title("🧠 AYANFE Input Bar Test")

st.write(
    "This is only a layout test. "
    "The real AYANFE chat remains untouched."
)


st.markdown(
    """
    <div class="test-input-bar">

        <div class="test-label">
            ＋ &nbsp;&nbsp;
            Ask AYANFE anything...
            &nbsp;&nbsp; 🎙️ &nbsp;&nbsp; ➤
        </div>

    </div>
    """,
    unsafe_allow_html=True
)
