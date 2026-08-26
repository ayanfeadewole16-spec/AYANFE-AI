# ============================================
# AYANFE AI V2 — MASTER ROUTER
# ============================================

from datetime import datetime


# ============================================
# INTENT DETECTION
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

    # Live information
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
        "football results",
        "football table"
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
        "math",
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

    return "general"


# ============================================
# ROUTE REQUEST
# ============================================

def route_request(user_input):

    intent = detect_intent(user_input)

    return {
        "intent": intent,

        # Gemini remains the fallback for now.
        # Specialist systems will be connected
        # to these intents next.
        "use_gemini": intent in [
            "general",
            "education",
            "programming",
            "writing"
        ]
    }
