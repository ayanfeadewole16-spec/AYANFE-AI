# ============================================
# AYANFE AI V2 — MASTER ROUTER
# ============================================

def detect_intent(user_input):

    text = user_input.strip().lower()

    # ========================================
    # IDENTITY
    # ========================================

    if any(x in text for x in [
        "who created you",
        "who made you",
        "who built you",
        "who is your creator",
        "who developed you"
    ]):
        return "identity"


    # ========================================
    # GREETINGS
    # ========================================

    if text in [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
        "how are you",
        "how are you?",
        "how are you today",
        "how are you today?",
        "how is it going",
        "how's it going"
    ]:
        return "greeting"


    # ========================================
    # DATE / TIME
    # IMPORTANT:
    # This MUST come BEFORE live search.
    # ========================================

    if any(x in text for x in [
        "what is today's date",
        "what is today's date?",
        "what date is it",
        "what date is it?",
        "today's date",
        "todays date",
        "what day is today",
        "what day is it"
    ]):
        return "datetime"


    if any(x in text for x in [
        "what time is it",
        "what time is it?",
        "current time",
        "what is the current time",
        "what is the time"
    ]):
        return "datetime"


    # ========================================
    # YOUTUBE
    # ========================================

    if any(x in text for x in [
        "youtube",
        "youtube video",
        "video on youtube",
        "find me a video",
        "find a video"
    ]):
        return "youtube"


    # ========================================
    # LIVE INFORMATION
    # ========================================

    if any(x in text for x in [
        "latest news",
        "breaking news",
        "recent news",
        "current news",
        "latest update",
        "latest information",
        "current events",
        "right now",
        "currently",
        "live score",
        "live scores",
        "latest score",
        "match result",
        "match results",
        "football result",
        "football results",
        "league table",
        "football table",
        "standings",
        "fixtures"
    ]):
        return "live"


    # ========================================
    # EDUCATION
    # ========================================

    if any(x in text for x in [
        "explain",
        "solve",
        "teach me",
        "study",
        "homework",
        "assignment",
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
        "economics",
        "government",
        "literature",
        "computer science"
    ]):
        return "education"


    # ========================================
    # PROGRAMMING
    # ========================================

    if any(x in text for x in [
        "python",
        "javascript",
        "programming",
        "coding",
        "debug",
        "code"
    ]):
        return "programming"


    # ========================================
    # WRITING
    # ========================================

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


    # ========================================
    # GENERAL
    # ========================================

    return "general"


# ============================================
# ROUTE REQUEST
# ============================================

def route_request(user_input):

    intent = detect_intent(user_input)

    return {
        "intent": intent,
        "use_gemini": False
    }
