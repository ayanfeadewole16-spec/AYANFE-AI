# ============================================
# AYANFE AI V2 — MASTER ROUTER
# ============================================

import re


# ============================================
# NORMALIZE USER REQUEST
# ============================================

def normalize(text):
    text = text.lower().strip()

    # Remove unnecessary punctuation
    text = re.sub(r"[!?.,]+", " ", text)

    # Remove repeated spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================
# INTENT DETECTION
# ============================================

def detect_intent(user_input):

    text = normalize(user_input)

    # ----------------------------------------
    # IDENTITY
    # ----------------------------------------

    identity_phrases = [
        "who created you",
        "who made you",
        "who built you",
        "who is your creator",
        "who developed you"
    ]

    if any(phrase in text for phrase in identity_phrases):
        return "identity"


    # ----------------------------------------
    # GREETINGS / CASUAL
    # ----------------------------------------

    greeting_words = [
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
    ]
    if any(
        text == word or text.startswith(word + " ")
        for word in greeting_words
    ):
        return "greeting"


    # ----------------------------------------
    # DATE / TIME
    # ----------------------------------------

    date_words = [
        "today date",
        "todays date",
        "what date is it",
        "date today",
        "what day is today",
        "which date is today"
    ]

    time_words = [
        "what time is it",
        "current time",
        "time right now",
        "what is the time",
        "tell me the time"
    ]

    if any(word in text for word in date_words):
        return "datetime"

    if any(word in text for word in time_words):
        return "datetime"


    # ----------------------------------------
    # YOUTUBE
    # ----------------------------------------

    youtube_words = [
        "youtube",
        "youtube video",
        "video on youtube",
        "find me a video",
        "find a video"
    ]

    if any(word in text for word in youtube_words):
        return "youtube"


    # ----------------------------------------
    # FOOTBALL / SPORTS
    # ----------------------------------------

    sports_words = [
        "football",
        "soccer",
        "premier league",
        "epl",
        "champions league",
        "europa league",
        "conference league",
        "la liga",
        "serie a",
        "bundesliga",
        "ligue 1",
        "arsenal",
        "chelsea",
        "liverpool",
        "manchester united",
        "man united",
        "manchester city",
        "tottenham",
        "newcastle",
        "real madrid",
        "barcelona",
        "bayern",
        "psg",
        "transfer",
        "transfers",
        "signed",
        "signing",
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
        "goals",
        "player"
    ]

    if any(word in text for word in sports_words):

        # Sports questions involving recent/current information
        live_sports_words = [
            "latest",
            "recent",
            "today",
            "currently",
            "current",
            "now",
            "latest transfer",
            "recent transfer",
            "new transfer",
            "latest signing",
            "recent signing",
            "who won",
            "who scored",
            "score",
            "scores",
            "result",
            "results",
            "transfer",
            "transfers",
            "transfer news",
            "transfer window",
            "latest football news"
        ]

        if any(word in text for word in live_sports_words):
            return "live"

        return "sports"


    # ----------------------------------------
    # GENERAL CURRENT INFORMATION / NEWS
    # ----------------------------------------

    live_words = [
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
    ]

    if any(word in text for word in live_words):
        return "live"


    # ----------------------------------------
    # EDUCATION
    # ----------------------------------------

    education_words = [
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
    ]

if any(word in text for word in education_words):
        return "education"


    # ----------------------------------------
    # PROGRAMMING
    # ----------------------------------------

    programming_words = [
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
    ]

    if any(word in text for word in programming_words):
        return "programming"


    # ----------------------------------------
    # WRITING
    # ----------------------------------------

    writing_words = [
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
    ]

    if any(word in text for word in writing_words):
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

    # ========================================
    # AYANFE'S INDEPENDENCE RULE
    # ========================================
    #
    # Built-in systems should handle:
    #
    # identity
    # greetings
    # date/time
    # sports routing
    # live information
    # YouTube
    # education
    # programming
    # writing
    #
    # Gemini should ONLY be used as a
    # last-resort general AI fallback.
    # ========================================

    return {
        "intent": intent,

        "use_gemini": intent == "general"
    }


