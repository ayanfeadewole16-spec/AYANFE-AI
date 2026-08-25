
# ============================================
# AYANFE AI V2 — CHAT MANAGER
# ============================================

from memory import (
    create_chat,
    load_chat,
    list_chats,
    add_message,
    delete_chat
)


def new_chat():
    """
    Start a completely new conversation.
    """
    return create_chat()


def get_chat(chat_id):
    """
    Open an existing conversation.
    """
    return load_chat(chat_id)


def send_message(chat_id, role, content):
    """
    Save a message to a specific conversation.
    """
    return add_message(chat_id, role, content)


def get_history():
    """
    Get saved conversations for the sidebar/history.
    """
    return list_chats()


def remove_chat(chat_id):
    """
    Delete a conversation.
    """
    return delete_chat(chat_id)
