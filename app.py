
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
# AYANFE SMART LOCAL RESPONSE SYSTEM
# ============================================

def fast_ayanfe_response(text):

    clean = text.strip().lower()

    # CREATOR
    if clean in [
        "who created you?",
        "who made you?",
        "who built you?",
        "who is your creator?",
        "who created ayanfe?"
    ]:
        return (
            "I was created by Ayanfe. "
            "I am AYANFE AI, a modern general-purpose "
            "AI assistant and learning companion."
        )

    # GREETINGS
    if clean in [
        "hi",
        "hello",
        "hey",
        "hey ayanfe",
        "hi ayanfe",
        "hello ayanfe"
    ]:
        return (
            "Hello! 👋 I'm AYANFE AI. "
            "What would you like to do today?"
        )

    # CAPABILITIES
    if clean in [
        "what can you do?",
        "what can you do",
        "what are your features?",
        "help"
    ]:
        return (
            "I can help with education, writing, programming, "
            "research, current information, sports, files, "
            "YouTube, everyday questions and more."
        )

    return None


# ============================================
# COMPOSER STATE
# ============================================

if "show_attachments" not in st.session_state:
    st.session_state.show_attachments = False


# ============================================
# FIXED COMPOSER DESIGN
# ============================================

st.markdown("""
<style>

.main .block-container {
    padding-bottom: 130px !important;
}

.st-key-ayanfe_composer {
    position: fixed;
    bottom: 15px;
    left: 50%;
    transform: translateX(-50%);
    width: min(900px, 90vw);
    z-index: 999999;
    background: white;
    padding: 10px 12px;
    border-radius: 18px;
    border: 1px solid rgba(0,0,0,0.10);
    box-shadow: 0 5px 25px rgba(0,0,0,0.12);
}

</style>
""", unsafe_allow_html=True)


# ============================================
# MAIN AYANFE COMPOSER
# ============================================

with st.container(key="ayanfe_composer"):

    with st.form(
        "ayanfe_message_form",
        clear_on_submit=True
    ):

        col1, col2, col3, col4 = st.columns(
            [0.7, 5.8, 0.9, 0.8]
        )

        # PLUS
        with col1:

            plus_clicked = st.form_submit_button(
                "＋",
                use_container_width=True
            )

        # TEXT INPUT
        with col2:

            typed_message = st.text_input(
                "message",
                placeholder="Ask AYANFE anything...",
                label_visibility="collapsed"
            )

        # VOICE
        with col3:

            voice_audio = st.audio_input(
                "🎙️",
                label_visibility="collapsed"
            )

        # SEND
        with col4:

            send_clicked = st.form_submit_button(
                "➤",
                use_container_width=True
            )


# ============================================
# PLUS / ATTACHMENTS
# ============================================

if plus_clicked:

    st.session_state.show_attachments = True


if st.session_state.show_attachments:

    uploaded_file = st.file_uploader(
        "Choose a file or image",
        type=[
            "pdf",
            "docx",
            "txt",
            "png",
            "jpg",
            "jpeg",
            "webp"
        ],
        key="ayanfe_attachment"
    )

    if uploaded_file:

        st.success(
            f"📎 Attached: {uploaded_file.name}"
        )


# ============================================
# VOICE
# ============================================

if voice_audio:

    st.info(
        "🎙️ Recording received. "
        "Voice-to-text connection is the next step."
    )


# ============================================
# PROCESS MESSAGE
# ============================================

if send_clicked and typed_message.strip():

    user_input = typed_message.strip()

    st.session_state.started = True

    add_message(
        st.session_state.chat_id,
        "user",
        user_input
    )

    # ----------------------------------------
    # LOCAL AYANFE BRAIN FIRST
    # ----------------------------------------

    answer = fast_ayanfe_response(
        user_input
    )

    # ----------------------------------------
    # AI FALLBACK ONLY WHEN NECESSARY
    # ----------------------------------------

    if answer is None:

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

            if (
                "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
            ):

                answer = (
                    "AYANFE is temporarily unable to "
                    "generate a full AI response. "
                    "Please try again later."
                )

            else:

                answer = (
                    "AYANFE is temporarily unavailable. "
                    "Please try again shortly."
                )

    # ----------------------------------------
    # SAVE ANSWER
    # ----------------------------------------

    add_message(
        st.session_state.chat_id,
        "assistant",
        answer
    )

    st.rerun()
