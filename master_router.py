# ============================================
# AYANFE AI V2 — FLEXIBLE MASTER ROUTER
# ============================================

import re


def normalize(text):
    """
    Clean the user's message without requiring
    exact wording.
    """
    if not text:
        return ""

    text = text.lower().strip()

    text = re.sub(r"\s+", " ", text)

    return text


def detect_intent(user_input):

    text = normalize(user_input)

    if not text:
        return "general"

    # ----------------------------------------
    # IDENTITY
    # ----------------------------------------

    identity_words = [
        "created",
        "made",
        "built",
        "creator",
        "who are you"
    ]

    if (
        any(word in text for word in identity_words)
        and (
            "you" in text
            or "ayanfe" in text
        )
    ):
        return "identity"


    # ----------------------------------------
    # DATE / TIME
    # ----------------------------------------

    if (
        ("date" in text or "day" in text)
        and (
            "today" in text
            or "now" in text
            or "current" in text
        )
    ):
        return "datetime"

    if (
        "time" in text
        and (
            "now" in text
            or "current" in text
            or "today" in text
        )
    ):
        return "datetime"


    # ----------------------------------------
    # YOUTUBE
    # ----------------------------------------
    if "youtube" in text:
        return "youtube"

    if (
        "video" in text
        and (
            "watch" in text
            or "find" in text
            or "show" in text
            or "youtube" in text
        )
    ):
        return "youtube"


    # ----------------------------------------
    # LIVE / CURRENT INFORMATION
    # ----------------------------------------

    current_signals = [
        "latest",
        "recent",
        "current",
        "currently",
        "today",
        "tonight",
        "this morning",
        "this week",
        "this month",
        "right now",
        "breaking",
        "news",
        "update",
        "happening",
        "going on",
        "new",
        "gist",
        "wetin",
        "sup"
    ]

    live_topics = [
        "football",
        "soccer",
        "premier league",
        "champions league",
        "transfer",
        "transfers",
        "match",
        "score",
        "result",
        "league",
        "player",
        "president",
        "government",
        "election",
        "world",
        "country"
    ]

    has_current_signal = any(
        word in text
        for word in current_signals
    )

    has_live_topic = any(
        word in text
        for word in live_topics
    )

    if has_current_signal:
        return "live"

    if (
        has_live_topic
        and (
            "who" in text
            or "what" in text
            or "which" in text
            or "where" in text
            or "when" in text
        )
    ):
        return "live"


    # ----------------------------------------
    # EDUCATION
    # ----------------------------------------

    education_signals = [
        "learn",
        "teach",
        "explain",
        "solve",
        "calculate",
        "homework",
        "assignment",
        "school",
        "exam",
        "test",
        "revision",
        "quiz",
        "question",
        "waec",
        "jamb",
        "neco",
        "math",
        "mathematics",
        "physics",
        "chemistry",
        "biology",
        "economics",
        "government",
        "literature",
        "english",
        "science"
    ]

    if any(
        word in text
        for word in education_signals
    ):
        return "education"


    # ----------------------------------------
    # PROGRAMMING
    # ----------------------------------------

    programming_signals = [
        "python",
        "javascript",
        "html",
        "css",
        "programming",
        "coding",
        "code",
        "software",
        "website",
        "app",
        "bug",
        "error",
        "debug"
    ]

    if any(
        word in text
        for word in programming_signals
    ):
        return "programming"


    # ----------------------------------------
    # WRITING
    # ----------------------------------------

    writing_signals = [
        "write",
        "rewrite",
        "rephrase",
        "essay",
        "letter",
        "email",
        "caption",
        "story",
        "paragraph",
        "message"
    ]

    if any(
        word in text
        for word in writing_signals
    ):
        return "writing"


    # ----------------------------------------
    # GENERAL
    # ----------------------------------------

    return "general"


def route_request(user_input):

    intent = detect_intent(user_input)

    return {
        "intent": intent,

        # Gemini intentionally disabled.
        "use_gemini": False
    }
