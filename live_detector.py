# ============================================
# AYANFE AI V2 — LIVE INFORMATION DETECTOR
# ============================================

STRONG_LIVE_PHRASES = [
    "today",
    "yesterday",
    "tomorrow",
    "latest",
    "breaking news",
    "recent news",
    "recent",
    "currently",
    "right now",
    "this morning",
    "tonight",
    "this week",
    "this month",
    "current events",
    "latest news",
    "latest update",
    "recent update",
    "latest information",
    "current information"
]


SPORTS_LIVE_PHRASES = [
    "who won",
    "who scored",
    "match result",
    "match results",
    "football result",
    "football results",
    "game result",
    "game results",
    "live score",
    "live scores",
    "league table",
    "football table",
    "standings",
    "fixtures"
]


NEWS_TOPICS = [
    "news",
    "announcement",
    "announcements",
    "election",
    "government announcement"
]


def detect_live_requirement(user_message):

    text = user_message.lower().strip()

    if not text:

        return {
            "needs_live_search": False,
            "reason": "Empty request."
        }

    for phrase in STRONG_LIVE_PHRASES:

        if phrase in text:

            return {
                "needs_live_search": True,
                "reason": (
                    f"Time-sensitive phrase detected: "
                    f"'{phrase}'."
                )
            }

    for phrase in SPORTS_LIVE_PHRASES:

        if phrase in text:

            return {
                "needs_live_search": True,
                "reason": (
                    f"Sports/current-result phrase "
                    f"detected: '{phrase}'."
                )
            }

    for topic in NEWS_TOPICS:

        if topic in text:

            return {
                "needs_live_search": True,
                "reason": (
                    f"Current-events topic detected: "
                    f"'{topic}'."
                )
            }

    return {
        "needs_live_search": False,
        "reason": "No clear requirement for live information."
    }
