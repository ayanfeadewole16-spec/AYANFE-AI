# ============================================
# AYANFE AI V2 — MAIN STREAMLIT APPLICATION
# ============================================

import os
import tempfile
from pathlib import Path

import streamlit as st

from ayanfe_brain import ask_ayanfe
import memory

create_chat = memory.create_chat
load_chat = memory.load_chat
list_chats = memory.list_chats
add_message = memory.add_message
delete_chat = memory.delete_chat


# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="AYANFE AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================
# SESSION STATE
# ============================================

if "chat_id" not in st.session_state:

    new_chat = create_chat()

    st.session_state.chat_id = (
        new_chat["chat_id"]
    )


if "started" not in st.session_state:

    st.session_state.started = False


if "show_attachments" not in st.session_state:

    st.session_state.show_attachments = False


if "uploaded_file" not in st.session_state:

    st.session_state.uploaded_file = None


# ============================================
# CUSTOM CSS
# ============================================

st.markdown(
    """
    <style>

    /* Main application */

    .stApp {
        overflow-x: hidden;
    }


    /* Hide Streamlit decoration */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* Main content */

    .main .block-container {

        max-width: 1000px;

        padding-top: 30px;

        padding-bottom: 120px;
    }


    /* AYANFE title */

    .ayanfe-title {

        text-align: center;

        font-size: 42px;

        font-weight: 700;

        margin-top: 20px;

        margin-bottom: 5px;
    }


    .ayanfe-subtitle {

        text-align: center;

        opacity: 0.65;

        margin-bottom: 35px;
    }


    /* Chat messages */

    [data-testid="stChatMessage"] {

        border-radius: 16px;

        margin-bottom: 10px;
    }


    /* Fixed composer */

    .composer-area {

        position: fixed;

        left: 0;

        right: 0;

        bottom: 0;

        z-index: 999;

        padding: 10px 20px 15px 20px;

        background: rgba(255,255,255,0.96);

        border-top: 1px solid rgba(128,128,128,0.20);

        backdrop-filter: blur(12px);
    }


    /* Dark mode */

    @media (prefers-color-scheme: dark) {

        .composer-area {

            background: rgba(20,20,20,0.96);

        }
    }


    /* Attachment buttons */

    .attachment-title {

        font-weight: 600;

        margin-bottom: 5px;
    }


    /* Sidebar */

    .sidebar-title {

        font-size: 22px;

        font-weight: 700;

        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================
# SIDEBAR
# ============================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🧠 AYANFE AI</div>',
        unsafe_allow_html=True
    )


    # ----------------------------------------
    # NEW CHAT
    # ----------------------------------------

    if st.button(
        "＋ New Chat",
        use_container_width=True
    ):

        new_chat = create_chat()

        st.session_state.chat_id = (
            new_chat["chat_id"]
        )

        st.session_state.started = False

        st.session_state.show_attachments = False

        st.session_state.uploaded_file = None

        st.rerun()


    st.divider()


    # ----------------------------------------
    # CHAT HISTORY
    # ----------------------------------------

    st.markdown("### 💬 Chats")

    chats = list_chats()


    for chat in chats:

        chat_id = chat["chat_id"]

        label = (
            "New conversation"
            if chat["message_count"] == 0
            else f"Conversation ({chat['message_count']} messages)"
        )


        if st.button(
            label,
            key=f"chat_{chat_id}",
            use_container_width=True
        ):

            st.session_state.chat_id = chat_id

            loaded = load_chat(chat_id)

            st.session_state.started = bool(
                loaded
                and loaded.get("messages")
            )

            st.rerun()


    st.divider()


    # ----------------------------------------
    # DELETE CURRENT CHAT
    # ----------------------------------------

    if st.button(
        "🗑️ Delete current chat",
        use_container_width=True
    ):

        delete_chat(
            st.session_state.chat_id
        )

        new_chat = create_chat()

        st.session_state.chat_id = (
            new_chat["chat_id"]
        )

        st.session_state.started = False

        st.rerun()


    st.divider()


    st.caption(
        "AYANFE AI V2\n"
        "Created by Ayanfe"
    )


# ============================================
# HEADER
# ============================================

if not st.session_state.started:

    st.markdown(
        '<div class="ayanfe-title">AYANFE AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="ayanfe-subtitle">'
        'Your AI assistant and learning companion'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================
# LOAD CURRENT CHAT
# ============================================

current_chat = load_chat(
    st.session_state.chat_id
)


if current_chat is None:

    current_chat = create_chat()

    st.session_state.chat_id = (
        current_chat["chat_id"]
    )


# ============================================
# DISPLAY CHAT
# ============================================

for message in current_chat["messages"]:

    role = message["role"]

    content = message["content"]


    if role == "user":

        with st.chat_message("user"):

            st.markdown(content)


    else:

        with st.chat_message("assistant"):

            st.markdown(content)


# ============================================
# ATTACHMENT MENU
# ============================================

if st.session_state.show_attachments:

    st.markdown(
        '<div class="attachment-title">'
        'Add to your message'
        '</div>',
        unsafe_allow_html=True
    )


    attachment_type = st.radio(
        "Choose attachment",
        [
            "📄 File",
            "🖼️ Image",
            "🎥 Video"
        ],
        horizontal=True,
        label_visibility="collapsed"
    )


    if attachment_type == "📄 File":

        uploaded = st.file_uploader(
            "Choose a file",
            type=[
                "pdf",
                "docx",
                "txt"
            ],
            label_visibility="collapsed"
        )


    elif attachment_type == "🖼️ Image":

        uploaded = st.file_uploader(
            "Choose an image",
            type=[
                "png",
                "jpg",
                "jpeg",
                "webp"
            ],
            label_visibility="collapsed"
        )


    else:

        uploaded = st.file_uploader(
            "Choose a video",
            type=[
                "mp4",
                "mov",
                "webm"
            ],
            label_visibility="collapsed"
        )


    if uploaded is not None:

        st.session_state.uploaded_file = uploaded


# ============================================
# VOICE INPUT
# ============================================

voice_audio = None


with st.container():

    st.markdown(
        '<div class="composer-area">',
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(
        [0.7, 6.5, 0.9]
    )


    # ----------------------------------------
    # PLUS BUTTON
    # ----------------------------------------

    with col1:

        if st.button(
            "＋",
            key="plus_button",
            help="Add file, image or video"
        ):

            st.session_state.show_attachments = (
                not st.session_state.show_attachments
            )

            st.rerun()


    # ----------------------------------------
    # TEXT INPUT
    # ----------------------------------------

    with col2:

        user_input = st.chat_input(
            "Ask AYANFE anything..."
        )


    # ----------------------------------------
    # MICROPHONE
    # ----------------------------------------

    with col3:

        voice_audio = st.audio_input(
            "🎙️",
            key="voice_recorder"
        )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================
# VOICE PROCESSING
# ============================================

if voice_audio is not None:

    try:

        from voice import transcribe_audio


        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as temp_file:

            temp_file.write(
                voice_audio.getvalue()
            )

            temp_path = temp_file.name


        result = transcribe_audio(
            temp_path
        )


        try:

            os.remove(temp_path)

        except Exception:

            pass


        if result.get("success"):

            user_input = result["text"]

        else:

            st.warning(
                result.get(
                    "error",
                    "Voice transcription failed."
                )
            )

            user_input = None


    except Exception:

        st.warning(
            "Voice input is temporarily unavailable."
        )

        user_input = None


# ============================================
# PROCESS MESSAGE
# ============================================

if user_input:

    st.session_state.started = True


    # ----------------------------------------
    # ATTACHMENT INFORMATION
    # ----------------------------------------

    attachment = (
        st.session_state.uploaded_file
    )


    message_for_ai = user_input


    if attachment is not None:

        message_for_ai += (
            "\n\n[Attached file: "
            f"{attachment.name}]"
        )


    # ----------------------------------------
    # SAVE USER MESSAGE
    # ----------------------------------------

    add_message(
        st.session_state.chat_id,
        "user",
        message_for_ai
    )


    # ----------------------------------------
    # RELOAD CONVERSATION
    # ----------------------------------------

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


    # ----------------------------------------
    # ASK AYANFE
    # ----------------------------------------

    answer = ask_ayanfe(
        user_input,
        conversation_history=history_for_ai
    )


    # ----------------------------------------
    # SAVE ANSWER
    # ----------------------------------------

    add_message(
        st.session_state.chat_id,
        "assistant",
        answer
    )


    # ----------------------------------------
    # CLEAR ATTACHMENT
    # ----------------------------------------

    st.session_state.uploaded_file = None

    st.session_state.show_attachments = False


    # ----------------------------------------
    # REFRESH
    # ----------------------------------------

    st.rerun()
