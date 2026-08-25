
# ============================================
# AYANFE AI V2 — PERSISTENT MEMORY
# ============================================

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path


PROJECT = Path("/content/drive/MyDrive/AYANFE_AI_V2")
MEMORY_DIR = PROJECT / "memory"

MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def create_chat():
    """
    Create a new conversation with a unique chat ID.
    """

    chat_id = str(uuid.uuid4())

    chat = {
        "chat_id": chat_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "messages": []
    }

    save_chat(chat)

    return chat


def get_chat_path(chat_id):
    return MEMORY_DIR / f"{chat_id}.json"


def save_chat(chat):
    """
    Save a complete conversation permanently.
    """

    chat["updated_at"] = datetime.now(timezone.utc).isoformat()

    path = get_chat_path(chat["chat_id"])

    with open(path, "w", encoding="utf-8") as f:
        json.dump(chat, f, indent=2, ensure_ascii=False)

    return True


def load_chat(chat_id):
    """
    Load an existing conversation.
    """

    path = get_chat_path(chat_id)

    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def add_message(chat_id, role, content):
    """
    Add a user or assistant message to a conversation.
    """

    chat = load_chat(chat_id)

    if chat is None:
        return None

    chat["messages"].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

    save_chat(chat)

    return chat


def list_chats():
    """
    Return all saved conversations.
    """

    chats = []

    for path in MEMORY_DIR.glob("*.json"):

        try:
            with open(path, "r", encoding="utf-8") as f:
                chat = json.load(f)

            chats.append({
                "chat_id": chat["chat_id"],
                "created_at": chat.get("created_at"),
                "updated_at": chat.get("updated_at"),
                "message_count": len(chat.get("messages", []))
            })

        except Exception:
            continue

    chats.sort(
        key=lambda x: x.get("updated_at", ""),
        reverse=True
    )

    return chats


def delete_chat(chat_id):
    """
    Delete a conversation.
    """

    path = get_chat_path(chat_id)

    if path.exists():
        path.unlink()
        return True

    return False
