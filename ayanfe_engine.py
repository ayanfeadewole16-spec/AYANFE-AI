
# ============================================
# AYANFE AI V2 — CENTRAL ENGINE
# ============================================

from master_router import route_request
from live_detector import detect_live_requirement
from date_time import get_date_context
from education import is_education_request, education_context
from memory import create_chat, load_chat, add_message
from youtube import is_youtube_request
from files import get_file_info


AYANFE_NAME = "AYANFE AI"
CREATOR = "Ayanfe"


def get_ayanfe_identity():
    return {
        "name": AYANFE_NAME,
        "creator": CREATOR,
        "description": (
            "AYANFE AI is a modern general-purpose "
            "AI assistant and learning companion."
        )
    }


def process_request(user_message, chat_id=None):
    """
    Central entry point for AYANFE.

    This function currently prepares and routes requests.
    The Gemini response layer will be connected later
    when API quota is available.
    """

    # Create a chat automatically if none exists
    if chat_id is None:
        chat = create_chat()
        chat_id = chat["chat_id"]

    # Save user message
    add_message(
        chat_id,
        "user",
        user_message
    )

    # Detect request type
    route = route_request(user_message)

    # Independently check live requirement
    live = detect_live_requirement(user_message)

    result = {
        "chat_id": chat_id,
        "route": route["type"],
        "needs_live_search": live["needs_live_search"],
        "live_reason": live["reason"],
        "date_context": get_date_context(),
        "identity": get_ayanfe_identity()
    }

    # Education information
    if is_education_request(user_message):
        result["education"] = True
        result["education_context"] = education_context()
    else:
        result["education"] = False

    # YouTube information
    result["youtube_request"] = is_youtube_request(user_message)

    return result
