# ============================================
# AYANFE AI V2 — SMART MASTER ROUTER
# ============================================

import re


# ============================================
# NORMALIZE USER INPUT
# ============================================

def normalize(text):

    text = text.lower().strip()

    # Remove unnecessary punctuation
    text = re.sub(r"[^\w\s']", " ", text)

    # Remove repeated spaces
    text = re.sub(r"\s+", " ", text)

    return text


# ============================================
# DATE / TIME DETECTION
# ============================================

def is_datetime_request(text):

    date_words = [
        "date",
        "day",
        "calendar"
    ]

    time_words = [
        "time",
        "clock"
    ]

    today_words = [
        "today",
        "todays",
        "this day",
        "now"
    ]

    if (
        any(word in text for word in date_words)
        and
        any(word in text for word in today_words)
    ):
        return True

    if (
        "what day" in text
        and
        ("today" in text or "now" in text)
    ):
        return True

    if (
        any(word in text for word in time_words)
        and
        any(word in text for word in [
            "current",
            "now",
            "today"
        ])
    ):
        return True

    return False


# ============================================
# LIVE INFORMATION DETECTION
# ============================================

def is_live_request(text):

    live_words = [
        "latest",
        "recent",
        "currently",
        "current",
        "right now",
        "today",
        "this week",
        "this month",
        "breaking",
        "new update",
        "new updates",
        "update",
        "news"
    ]

    return any(
        word in text
        for word in live_words
    )


# ============================================
# FOOTBALL / SPORTS DETECTION
# ============================================

def is_sports_request(text):

    sports_words = [
        "football",
        "soccer",
        "premier league",
        "epl",
        "english premier league",
        "champions league",
        "europa league",
        "conference league",
        "fifa",
        "world cup",
        "transfer",
        "transfers",
        "signing",
        "signings",
        "player moved",
        "club",
        "match",
        "matches",
        "fixture",
        "fixtures",
        "score",
        "scores",
        "league table",
        "standings"
    ]

    return any(
        word in text
        for word in sports_words
    )


# ============================================
# YOUTUBE
# ============================================

def is_youtube_request(text):

    return any(
        word in text
        for word in [
            "youtube",
            "youtube video",
            "video on youtube"
        ]
    )


# ============================================
# EDUCATION
# ============================================

def is_education_request(text):

    words = [
        "homework",
        "assignment",
        "study",
        "revision",
        "exam",
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
        "computer science",
        "teach me",
        "explain this",
        "solve this",
        "quiz me"
    ]

    return any(
        word in text
        for word in words
    )


# ============================================
# PROGRAMMING
# ============================================

def is_programming_request(text):

    words = [
        "python",
        "javascript",
        "html",
        "css",
        "programming",
        "coding",
        "code",
        "debug",
        "error in my code",
        "function",
        "class",
        "api",
        "github",
        "streamlit"
    ]

    return any(
        word in text
        for word in words
    )


# ============================================
# WRITING
# ============================================

def is_writing_request(text):

    words = [
        "write",
        "rewrite",
        "essay",
        "letter",
        "email",
        "caption",
        "speech",
        "story",
        "application",
        "paragraph"
    ]

    return any(
        word in text
        for word in words
    )


# ============================================
# INTENT DETECTION
# ============================================

def detect_intent(user_input):

    text = normalize(user_input)


    # ----------------------------------------
    # IDENTITY
    # ----------------------------------------

    if any(
        phrase in text
        for phrase in [
            "who created you",
            "who made you",
            "who built you",
            "who is your creator",
            "who developed you"
        ]
    ):
        return "identity"


    # ----------------------------------------
    # GREETING
    # ----------------------------------------

    if text in [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]:

        return "greeting"


    # ----------------------------------------
    # DATE / TIME
    # ----------------------------------------

    if is_datetime_request(text):

        return "datetime"


    # ----------------------------------------
    # YOUTUBE
    # ----------------------------------------

    if is_youtube_request(text):

        return "youtube"


    # ----------------------------------------
    # SPORTS + LIVE
    # IMPORTANT:
    # Sports live requests go to LIVE SEARCH.
    # ----------------------------------------

    if is_sports_request(text):

        if is_live_request(text):

            return "live"

        # Transfer questions are normally
        # time-sensitive even without "latest".

        if any(
            word in text
            for word in [
                "transfer",
                "transfers",
                "signing",
                "signings",
                "player moved"
            ]
        ):

            return "live"

        return "sports"


    # ----------------------------------------
    # LIVE INFORMATION
    # ----------------------------------------

    if is_live_request(text):

        return "live"


    # ----------------------------------------
    # EDUCATION
    # ----------------------------------------

    if is_education_request(text):

        return "education"


    # ----------------------------------------
    # PROGRAMMING
    # ----------------------------------------

    if is_programming_request(text):

        return "programming"


    # ----------------------------------------
    # WRITING
    # ----------------------------------------

    if is_writing_request(text):

        return "writing"


    # ----------------------------------------
    # GENERAL
    # ----------------------------------------

    return "general"


# ============================================
# ROUTE REQUEST
# ============================================

def route_request(user_input):

    intent = detect_intent(user_input)

    return {
        "intent": intent,

        # Gemini is intentionally disabled.
        "use_gemini": False
    }
