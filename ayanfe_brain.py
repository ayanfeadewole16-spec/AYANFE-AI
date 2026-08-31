# ============================================
# AYANFE AI V2 — INDEPENDENT CORE BRAIN
# ============================================

from datetime import datetime

from master_router import route_request
from live_search import search_web
from youtube import get_best_youtube_video


# ============================================
# AYANFE IDENTITY
# ============================================

AYANFE_SYSTEM_INSTRUCTION = """
You are AYANFE AI, a modern general-purpose
AI assistant and learning companion.

Your creator is Ayanfe.

You are designed to operate independently
using AYANFE's own built-in systems.

Do not unnecessarily use external AI services.

Do not automatically generate quizzes,
practice questions or extra sections unless
the user asks for them or they are genuinely
useful to the request.
"""


# ============================================
# LOCAL RESPONSES
# ============================================

def local_response(user_message):

    text = user_message.strip().lower()

    # ----------------------------------------
    # IDENTITY
    # ----------------------------------------

    if any(x in text for x in [
        "who created you",
        "who made you",
        "who built you",
        "who is your creator"
    ]):
        return "I was created by Ayanfe."


    # ----------------------------------------
    # GREETINGS
    # ----------------------------------------

    if text in [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]:
        return (
            "I'm doing great! 😊 "
            "I'm ready to help. What would you like "
            "to do today?"
        )


    # ----------------------------------------
    # DATE
    # ----------------------------------------

    if any(x in text for x in [
        "today date",
        "today's date",
        "what date is it",
        "what is the date today",
        "what day is today",
        "which date is today"
    ]):
        now = datetime.now()

        return (
            f"Today is {now.strftime('%A, %B %d, %Y')}."
        )


    # ----------------------------------------
    # TIME
    # ----------------------------------------

    if any(x in text for x in [
        "what time is it",
        "what is the time",
        "current time",
        "time right now",
        "tell me the time"
    ]):
        now = datetime.now()

        return (
            f"The current time is "
            f"{now.strftime('%I:%M %p')}."
        )


    # ----------------------------------------
    # CAPABILITIES
    # ----------------------------------------

    if any(x in text for x in [
        "what can you do",
        "what are your features",
        "help me",
        "what do you do"
    ]):
        return (
            "I can help with education, general questions, "
            "current information, football and sports, "
            "programming, writing, research, YouTube, "
            "files and everyday questions."
        )


    return None


# ============================================
# LIVE INFORMATION
# ============================================

def handle_live_request(user_message):

    result = search_web(
        user_message,
        max_results=5
    )

    if not result.get("success"):
        return (
            "I couldn't reach the web search service "
            "right now. Please try again shortly."
        )

    results = result.get("results", [])

    if not results:
        return (
            "I couldn't find reliable current information "
            "for that request."
        )

    answer = "Here is what I found from current web sources:\n\n"

    for item in results[:5]:

        title = item.get("title", "")
        url = item.get("url", "")
        snippet = item.get("snippet", "")

        answer += f"**{title}**\n"

        if snippet:
            answer += f"{snippet}\n"

        if url:
            answer += f"Source: {url}\n"

        answer += "\n"

    return answer.strip()


# ============================================
# YOUTUBE
# ============================================

def handle_youtube_request(user_message):

    result = get_best_youtube_video(
        user_message
    )

    if not result.get("success"):
        return (
            "I couldn't find a suitable YouTube video "
            "for that request."
        )

    title = result.get("title", "")
    url = result.get("url", "")
    description = result.get("description", "")

    answer = f"**{title}**\n\n"

    if description:
        answer += f"{description}\n\n"

    answer += f"Watch on YouTube: {url}"

    return answer


# ============================================
# MAIN AYANFE BRAIN
# ============================================

def ask_ayanfe(
    user_message,
    conversation_history=None,
    api_key=None
):

    # ========================================
    # 1. LOCAL AYANFE SYSTEMS
    # ========================================

    answer = local_response(user_message)

    if answer is not None:
        return answer


    # ========================================
    # 2. ROUTER
    # ========================================

    route = route_request(user_message)

    intent = route.get(
        "intent",
        "general"
    )


    # ========================================
    # 3. LIVE INFORMATION
    # ========================================

    if intent == "live":

        return handle_live_request(
            user_message
        )


    # ========================================
    # 4. YOUTUBE
    # ========================================

    if intent == "youtube":

        return handle_youtube_request(
            user_message
        )


    # ========================================
    # 5. SPORTS
    # ========================================

    if intent == "sports":

        return handle_live_request(
            user_message
        )


    # ========================================
    # 6. EDUCATION
    # ========================================

    if intent == "education":

        return (
            "I can handle this as an education request. "
            "Tell me the exact question or topic and "
            "I'll work through it with you."
        )


    # ========================================
    # 7. PROGRAMMING
    # ========================================

    if intent == "programming":

        return (
            "I can help with the programming problem. "
            "Send me the code or describe what you "
            "want the program to do."
        )


    # ========================================
    # 8. WRITING
    # ========================================

    if intent == "writing":

        return (
            "Yes, I can help with that. "
            "Send me the text or tell me what you "
            "want to write."
        )


    # ========================================
    # 9. GENERAL — NO GEMINI
    # ========================================

    return (
        "I'm AYANFE AI. I can handle many requests "
        "using my built-in systems, but I don't yet "
        "have a built-in system for that particular "
        "request."
    )

