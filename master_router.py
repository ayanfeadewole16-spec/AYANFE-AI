# ============================================
# AYANFE AI V2 — MASTER ROUTER
# ============================================

from live_detector import detect_live_requirement
from youtube import is_youtube_request
from education import is_education_request


def detect_intent(user_input):

    text = user_input.strip().lower()

    # ----------------------------------------
    # IDENTITY
    # ----------------------------------------

    if any(x in text for x in [
        "who created you",
        "who made you",
        "who built you",
        "who is your creator"
    ]):
        return "identity"


    # ----------------------------------------
    # GREETINGS / CASUAL
    # ----------------------------------------

    if text in [
        "hi",
        "hello",
        "hey",
        "hi ayanfe",
        "hello ayanfe",
        "hey ayanfe",
        "good morning",
        "good afternoon",
        "good evening",
        "how are you",
        "how are you?",
        "how are you today",
        "how are you today?",
        "how is it going",
        "how's it going",
        "how are things"
    ]:
        return "greeting"


    # ----------------------------------------
    # DATE / TIME
    # ----------------------------------------

    if any(x in text for x in [
        "what time is it",
        "current time",
        "what is today's date",
        "what date is it",
        "today's date",
        "what day is it",
        "what day is today",
        "time in",
        "date in"
    ]):
        return "datetime"


    # ----------------------------------------
    # YOUTUBE
    # ----------------------------------------

    if is_youtube_request(text):
        return "youtube"


    # ----------------------------------------
    # LIVE INFORMATION
    # ----------------------------------------

    live = detect_live_requirement(text)

    if live.get("needs_live_search"):
        return "live"


    # ----------------------------------------
    # EDUCATION
    # ----------------------------------------

    if is_education_request(text):
        return "education"


    # ----------------------------------------
    # PROGRAMMING
    # ----------------------------------------

    if any(x in text for x in [
        "python",
        "javascript",
        "programming",
        "code",
        "coding",
        "debug",
        "program",
        "html",
        "css"
    ]):
        return "programming"


    # ----------------------------------------
    # WRITING
    # ----------------------------------------

    if any(x in text for x in [
        "write",
        "rewrite",
        "essay",
        "letter",
        "caption",
        "story",
        "email",
        "paragraph",
        "application"
    ]):
        return "writing"


    # ----------------------------------------
    # GENERAL
    # ----------------------------------------

    return "general"


def route_request(user_input):

    intent = detect_intent(user_input)

    # Gemini is NOT automatically required
    # for specialist/local requests.

    return {
        "intent": intent,

        "use_gemini": intent == "general",

        "needs_live_search": intent == "live",

        "needs_youtube": intent == "youtube",

        "needs_education": intent == "education"
    }
