
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# ============================================
# AYANFE AI V2 — STREAMLIT WEBSITE
# ============================================

PROJECT = Path(__file__).parent

if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))

from memory import (
    create_chat,
    load_chat,
    add_message,
    list_chats
)

from ayanfe_brain import ask_ayanfe


# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="AYANFE AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================
# CUSTOM DESIGN
# ============================================

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 7rem;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128,128,128,0.18);
}

.sidebar-title {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 20px;
}

/* Welcome */

.welcome {
    text-align: center;
    padding-top: 12vh;
}

.welcome h1 {
    font-size: 42px;
    margin-bottom: 8px;
}

.welcome p {
    font-size: 18px;
    opacity: 0.7;
}

/* Cards */

div.stButton > button {
    border-radius: 12px;
    min-height: 48px;
}

/* Messages */

[data-testid="stChatMessage"] {
    border-radius: 14px;
}

/* Bottom composer */

[data-testid="stChatInput"] {
    position: fixed;
    bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


# ============================================
# SESSION STATE
# ============================================

if "chat_id" not in st.session_state:
    chat = create_chat()
    st.session_state.chat_id = chat["chat_id"]

if "started" not in st.session_state:
    st.session_state.started = False


# ============================================
# SIDEBAR
# ============================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🧠 AYANFE AI</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "＋ New Chat",
        use_container_width=True
    ):
        chat = create_chat()

        st.session_state.chat_id = chat["chat_id"]
        st.session_state.started = False

        st.rerun()

    st.divider()

    st.markdown("### 🗂 History")

    history = list_chats()

    if history:

        for item in history:

            chat_id = item["chat_id"]

            if item["message_count"] == 0:
                title = "New conversation"
            else:
                chat = load_chat(chat_id)

                first_user_message = next(
                    (
                        m["content"]
                        for m in chat["messages"]
                        if m["role"] == "user"
                    ),
                    "Conversation"
                )

                title = first_user_message[:32]

            if st.button(
                title,
                key=f"history_{chat_id}",
                use_container_width=True
            ):
                st.session_state.chat_id = chat_id
                st.session_state.started = True
                st.rerun()

    st.divider()

    st.caption("AYANFE AI")
    st.caption("Created by Ayanfe")


# ============================================
# LOAD CURRENT CHAT
# ============================================

current_chat = load_chat(
    st.session_state.chat_id
)

if current_chat is None:
    current_chat = create_chat()
    st.session_state.chat_id = current_chat["chat_id"]


# ============================================
# WELCOME SCREEN
# ============================================

if not current_chat["messages"]:

    st.markdown(
        """
        <div class="welcome">
            <h1>🧠 AYANFE AI</h1>
            <p>What do you want to do today?</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📚 Study", use_container_width=True):
            st.session_state.started = True
            st.session_state.prefill = "Help me study "
            st.rerun()

    with col2:
        if st.button("✍️ Write", use_container_width=True):
            st.session_state.started = True
            st.session_state.prefill = "Help me write "
            st.rerun()

    with col3:
        if st.button("🔬 Research", use_container_width=True):
            st.session_state.started = True
            st.session_state.prefill = "Help me research "
            st.rerun()

    col4, col5, col6 = st.columns(3)

    with col4:
        if st.button("💻 Code", use_container_width=True):
            st.session_state.started = True
            st.session_state.prefill = "Help me with programming "
            st.rerun()

    with col5:
        if st.button("⚽ Sports", use_container_width=True):
            st.session_state.started = True
            st.session_state.prefill = "Give me the latest sports information "
            st.rerun()

    with col6:
        if st.button("💡 Ask Anything", use_container_width=True):
            st.session_state.started = True
            st.session_state.prefill = ""
            st.rerun()


# ============================================
# DISPLAY CONVERSATION
# ============================================

for message in current_chat["messages"]:

    role = message["role"]

    if role == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])

    elif role == "assistant":
        with st.chat_message("assistant", avatar="🧠"):
            st.markdown(message["content"])


# ============================================
# FILE UPLOAD
# ============================================

uploaded_file = st.file_uploader(
    "＋ Attach a file",
    type=[
        "pdf",
        "docx",
        "txt",
        "png",
        "jpg",
        "jpeg",
        "webp"
    ],
    label_visibility="collapsed"
)


# ============================================
# MAIN COMPOSER
# ============================================

placeholder = "Ask AYANFE anything..."

if "prefill" in st.session_state:
    if st.session_state.prefill:
        placeholder = st.session_state.prefill

user_input = st.chat_input(
    placeholder
)


# ============================================
# PROCESS MESSAGE
# ============================================

if user_input:

    st.session_state.started = True

    add_message(
        st.session_state.chat_id,
        "user",
        user_input
    )

    # Reload conversation
    current_chat = load_chat(
        st.session_state.chat_id
    )

    history_for_ai = [
        {
            "role": m["role"],
            "content": m["content"]
        }
        for m in current_chat["messages"][-20:]
    ]

    try:

        answer = ask_ayanfe(
            user_input,
            conversation_history=history_for_ai
        )

    except Exception as e:

        error_text = str(e)

        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:

            answer = (
                "I’m connected to AYANFE AI, but the Gemini free-tier "
                "quota is currently exhausted. The website and memory "
                "systems are working; AI generation will resume when "
                "the available quota resets or a usable API quota is "
                "provided."
            )

        else:

            answer = (
                "AYANFE encountered a temporary AI connection problem.\n\n"
                f"Details: {error_text}"
            )

    add_message(
        st.session_state.chat_id,
        "assistant",
        answer
    )

    st.rerun()
