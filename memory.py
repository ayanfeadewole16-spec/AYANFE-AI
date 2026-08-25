# ============================================
# AYANFE AI V2 — DEPLOYMENT-SAFE MEMORY
# ============================================

from pathlib import Path
import sqlite3
import uuid
from datetime import datetime


# Streamlit Cloud's project directory is read-only.
# /tmp is writable during the running app.
MEMORY_DIR = Path("/tmp/ayanfe_ai_memory")
MEMORY_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = MEMORY_DIR / "ayanfe_memory.db"


def get_connection():
    conn = sqlite3.connect(
        str(DB_PATH),
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn


def initialize_database():

    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            chat_id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def create_chat():

    initialize_database()

    chat_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO chats
        (chat_id, created_at, updated_at)
        VALUES (?, ?, ?)
        """,
        (chat_id, now, now)
    )

    conn.commit()
    conn.close()

    return {
        "chat_id": chat_id,
        "messages": []
    }


def add_message(chat_id, role, content):

    initialize_database()

    now = datetime.now().isoformat()

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO messages
        (chat_id, role, content, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (chat_id, role, content, now)
    )

    conn.execute(
        """
        UPDATE chats
        SET updated_at = ?
        WHERE chat_id = ?
        """,
        (now, chat_id)
    )

    conn.commit()
    conn.close()


def load_chat(chat_id):

    initialize_database()

    conn = get_connection()

    chat = conn.execute(
        """
        SELECT *
        FROM chats
        WHERE chat_id = ?
        """,
        (chat_id,)
    ).fetchone()

    if chat is None:
        conn.close()
        return None

    messages = conn.execute(
        """
        SELECT role, content, created_at
        FROM messages
        WHERE chat_id = ?
        ORDER BY id ASC
        """,
        (chat_id,)
    ).fetchall()

    conn.close()

    return {
        "chat_id": chat["chat_id"],
        "created_at": chat["created_at"],
        "updated_at": chat["updated_at"],
        "messages": [
            {
                "role": message["role"],
                "content": message["content"],
                "created_at": message["created_at"]
            }
            for message in messages
        ]
    }


def list_chats():

    initialize_database()

    conn = get_connection()

    chats = conn.execute(
        """
        SELECT
            c.chat_id,
            c.created_at,
            c.updated_at,
            COUNT(m.id) AS message_count
        FROM chats c
        LEFT JOIN messages m
            ON c.chat_id = m.chat_id
        GROUP BY c.chat_id
        ORDER BY c.updated_at DESC
        """
    ).fetchall()

    conn.close()

    return [
        {
            "chat_id": chat["chat_id"],
            "created_at": chat["created_at"],
            "updated_at": chat["updated_at"],
            "message_count": chat["message_count"]
        }
        for chat in chats
    ]


initialize_database()
