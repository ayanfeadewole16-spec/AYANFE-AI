
# ============================================
# AYANFE AI V2 — MASTER ROUTER
# ============================================

import re


LIVE_KEYWORDS = [
    "today",
    "yesterday",
    "latest",
    "recent",
    "currently",
    "current",
    "right now",
    "news",
    "this week",
    "this month",
    "who won",
    "score",
    "scores",
    "result",
    "results",
    "standings",
    "table",
    "announcement",
]


YOUTUBE_KEYWORDS = [
    "youtube",
    "youtube video",
    "video on youtube",
    "find me a video",
    "find a video",
]


EDUCATION_KEYWORDS = [
    "solve",
    "explain",
    "homework",
    "assignment",
    "study",
    "revision",
    "quiz",
    "practice question",
    "waec",
    "jamb",
    "neco",
    "mathematics",
    "math",
    "physics",
    "chemistry",
    "biology",
    "english",
    "literature",
    "economics",
    "government",
    "computer science",
]


FILE_KEYWORDS = [
    "pdf",
    "document",
    "file",
    "uploaded",
    "attachment",
    "this image",
    "this photo",
]


def contains_keyword(text, keywords):
    text = text.lower()
    return any(keyword in text for keyword in keywords)


def detect_request_type(user_message):
    """
    Determine which AYANFE system should handle a request.
    """

    text = user_message.strip()

    if not text:
        return "empty"

    # YouTube has priority when explicitly requested
    if contains_keyword(text, YOUTUBE_KEYWORDS):
        return "youtube"

    # Files/images
    if contains_keyword(text, FILE_KEYWORDS):
        return "files"

    # Current/live information
    if contains_keyword(text, LIVE_KEYWORDS):
        return "live_search"

    # Education
    if contains_keyword(text, EDUCATION_KEYWORDS):
        return "education"

    # Everything else
    return "general"


def route_request(user_message):
    request_type = detect_request_type(user_message)

    return {
        "type": request_type,
        "message": user_message
    }
