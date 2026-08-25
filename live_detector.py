
# ============================================
# AYANFE AI V2 — LIVE INFORMATION DETECTOR
# ============================================

import re


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
    "current information",
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
    "fixtures",
]


NEWS_TOPICS = [
    "news",
    "announcement",
    "announcements",
    "election",
    "government announcement",
]


def detect_live_requirement(user_message):
    """
    Determine whether a request requires current/live information.
    """

    text = user_message.lower().strip()

    if not text:
        return {
            "needs_live_search": False,
            "reason": "Empty request."
        }

    # Strong time-sensitive phrases
    for phrase in STRONG_LIVE_PHRASES:
        if phrase in text:
            return {
                "needs_live_search": True,
                "reason": f"Time-sensitive phrase detected: '{phrase}'."
            }

    # Sports-specific live requests
    for phrase in SPORTS_LIVE_PHRASES:
        if phrase in text:
            return {
                "needs_live_search": True,
                "reason": f"Sports/current-result phrase detected: '{phrase}'."
            }

    # News and announcement requests
    for topic in NEWS_TOPICS:
        if topic in text:
            return {
                "needs_live_search": True,
                "reason": f"Current-events topic detected: '{topic}'."
            }

    return {
        "needs_live_search": False,
        "reason": "No clear requirement for live information."
    }
