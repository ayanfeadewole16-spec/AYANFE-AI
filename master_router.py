
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
# ============================================
# AYANFE AI V2 — MASTER ROUTER
# ============================================

from datetime import datetime


# ============================================
# LOCAL INTENT DETECTION
# ============================================

def detect_intent(user_input):

    text = user_input.strip().lower()

    # Identity
    if any(x in text for x in [
        "who created you",
        "who made you",
        "who built you",
        "who is your creator"
    ]):
        return "identity"

    # Greetings
    if text in [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]:
        return "greeting"

    # Date / time
    if any(x in text for x in [
        "what time is it",
        "current time",
        "what is today's date",
        "what date is it",
        "today's date"
    ]):
        return "datetime"

    # YouTube
    if any(x in text for x in [
        "youtube",
        "youtube video",
        "find me a video",
        "find a video"
    ]):
        return "youtube"

    # Current information
    if any(x in text for x in [
        "latest",
        "recent",
        "today",
        "yesterday",
        "currently",
        "right now",
        "news",
        "current",
        "who won",
        "latest score",
        "football results"
    ]):
        return "live"

    # Education
    if any(x in text for x in [
        "explain",
        "solve",
        "teach me",
        "study",
        "quiz me",
        "practice question",
        "waec",
        "jamb",
        "neco",
        "mathematics",
        "physics",
        "chemistry",
        "biology",
        "economics",
        "government",
        "literature",
        "computer science"
    ]):
        return "education"

    # Programming
    if any(x in text for x in [
        "python",
        "javascript",
        "programming",
        "code",
        "coding",
        "debug",
        "program"
    ]):
        return "programming"

    # Writing
    if any(x in text for x in [
        "write",
        "rewrite",
        "essay",
        "letter",
        "caption",
        "story",
        "email"
    ]):
        return "writing"

    # General
    return "general"


# ============================================
# ROUTE REQUEST
# ============================================

def route_request(user_input):

    intent = detect_intent(user_input)

    return {
        "intent": intent,
        "use_gemini": intent == "general"
    }
