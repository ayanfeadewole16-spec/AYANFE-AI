# ============================================
# AYANFE AI V2 — MASTER ROUTER
# ============================================

import re


def normalize(text):
    text = text.lower().strip()
    text = re.sub(r"[!?.,]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def detect_intent(user_input):

    text = normalize(user_input)

    # Identity
    if any(x in text for x in [
        "who created you",
        "who made you",
        "who built you",
        "who is your creator",
        "who developed you"
    ]):
        return "identity"

    # Greetings
    if any(x in text for x in [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
        "how are you",
        "how are you today",
        "how is it going",
        "how are things"
    ]):
        return "greeting"

    # Date and time
    if any(x in text for x in [
        "today date",
        "todays date",
        "what date is it",
        "date today",
        "what day is today",
        "which date is today",
        "what time is it",
        "current time",
        "time right now",
        "what is the time"
    ]):
        return "datetime"

    # YouTube
    if any(x in text for x in [
        "youtube",
        "youtube video",
        "video on youtube",
        "find me a video",
        "find a video"
    ]):
        return "youtube"

    # Football and sports
    if any(x in text for x in [
        "football",
        "soccer",
        "premier league",
        "epl",
        "champions league",
        "europa league",
        "la liga",
        "serie a",
        "bundesliga",
        "ligue 1",
        "arsenal",
        "chelsea",
        "liverpool",
        "manchester united",
        "manchester city",
        "tottenham",
        "newcastle",
        "real madrid",
        "barcelona",
        "bayern",
        "psg",
        "transfer",
        "transfers",
        "transfer window",
        "fixture",
        "fixtures",
        "match",
        "matches",
        "score",
        "scores",
        "league table",
        "standings",
        "goal",
        "goals"
    ]):

        if any(x in text for x in [
            "latest",
            "recent",
            "today",
            "currently",
            "current",
            "now",
            "transfer",
            "transfers",
            "transfer news",
            "latest transfer",
            "recent transfer",
            "new signing",
            "latest signing",
            "who won",
            "who scored",
            "result",
            "results",
            "score",
            "scores"
        ]):
            return "live"

        return "sports"

    # Current information and news
    if any(x in text for x in [
        "latest",
        "recent",
        "currently",
        "right now",
        "today",
        "yesterday",
        "tomorrow",
        "this morning",
        "tonight",
        "this week",
        "this month",
        "breaking",
        "news",
        "current events",
        "latest news",
        "recent news",
        "latest update",
        "recent update",
        "current information",
        "what happened today",
        "what is happening"
    ]):
        return "live"
# Education
    if any(x in text for x in [
        "study",
        "learn",
        "lesson",
        "teach me",
        "explain",
        "homework",
        "assignment",
        "revision",
        "quiz",
        "practice",
        "exam",
        "question",
        "mathematics",
        "math",
        "physics",
        "chemistry",
        "biology",
        "english",
        "literature",
        "economics",
        "government",
        "geography",
        "computer science",
        "waec",
        "jamb",
        "neco",
        "sat"
    ]):
        return "education"

    # Programming
    if any(x in text for x in [
        "python",
        "javascript",
        "html",
        "css",
        "programming",
        "program",
        "coding",
        "code",
        "debug",
        "debugging",
        "software",
        "website",
        "app development"
    ]):
        return "programming"

    # Writing
    if any(x in text for x in [
        "write",
        "rewrite",
        "rephrase",
        "proofread",
        "essay",
        "letter",
        "caption",
        "story",
        "email",
        "message",
        "paragraph",
        "speech",
        "application"
    ]):
        return "writing"

    return "general"


def route_request(user_input):

    intent = detect_intent(user_input)

    return {
        "intent": intent,

        # AYANFE uses its own systems first.
        # Gemini is only the last-resort fallback
        # for requests that cannot be handled locally.
        "use_gemini": intent == "general"
    }

