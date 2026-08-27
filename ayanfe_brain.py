# ============================================
# AYANFE AI V2 — CORE BRAIN
# ============================================

import os
import re

from datetime import datetime

from google import genai

from master_router import route_request

from date_time import (
    get_local_datetime,
    get_time_in_timezone
)

from live_search import (
    search_web,
    format_search_results
)

from youtube import (
    get_best_youtube_video
)

from education import (
    education_context
)


MODEL = "gemini-3.6-flash"


# ============================================
# AYANFE IDENTITY
# ============================================

AYANFE_SYSTEM_INSTRUCTION = """

You are AYANFE AI.

You were created by Ayanfe.

You are a modern general-purpose AI assistant
and learning companion.

You are NOT education-only.

You can help with:

Education
General questions
Writing
Programming
Research
Current information
News
Football and sports
YouTube
Files
Images
Voice
Everyday questions
Study assistance

Be clear, helpful and natural.

Never pretend that information is current
unless it has actually been obtained from a
current source.

When helping with education, use this structure
when appropriate:

1. Simple explanation
2. Detailed explanation
3. Example
4. Practice question
5. Quiz

Do not force the structure when it is unnecessary.

"""


# ============================================
# GEMINI CLIENT
# ============================================

def get_client(api_key=None):

    key = (
        api_key
        or os.getenv("GEMINI_API_KEY")
    )

    if not key:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(
        api_key=key
    )


# ============================================
# LOCAL RESPONSE SYSTEM
# ============================================

def local_response(user_message):

    clean = (
        user_message
        .strip()
        .lower()
    )


    # ----------------------------------------
    # IDENTITY
    # ----------------------------------------

    if clean in [
        "who created you",
        "who created you?",
        "who made you",
        "who made you?",
        "who built you",
        "who built you?",
        "who is your creator",
        "who is your creator?"
    ]:

        return (
            "I was created by Ayanfe."
        )


    # ----------------------------------------
    # GREETINGS
    # ----------------------------------------

    if clean in [
        "hi",
        "hello",
        "hey",
        "hi ayanfe",
        "hello ayanfe",
        "hey ayanfe",
        "good morning",
        "good afternoon",
        "good evening"
    ]:

        return (
            "Hello! 👋 I'm AYANFE AI. "
            "I'm ready to help. What would "
            "you like to do today?"
        )


    # ----------------------------------------
    # HOW ARE YOU
    # ----------------------------------------

    if clean in [
        "how are you",
        "how are you?",
        "how are you today",
        "how are you today?",
        "how is it going",
        "how's it going",
        "how are things"
    ]:

        return (
            "I'm doing great! 😊 "
            "I'm ready to help you with "
            "whatever you need."
        )


    # ----------------------------------------
    # CAPABILITIES
    # ----------------------------------------

    if clean in [
        "what can you do",
        "what can you do?",
        "what are your features",
        "what are your features?",
        "help"
    ]:

        return (
            "I can help with education, "
            "writing, programming, research, "
            "current information, sports, "
            "YouTube, files, everyday questions "
            "and much more."
        )


    # ----------------------------------------
    # DATE
    # ----------------------------------------

    if clean in [
        "what is today's date",
        "what is today's date?",
        "what date is it",
        "what date is it?",
        "today's date"
    ]:

        current = get_local_datetime()

        return (
            f"Today is "
            f"{current['formatted_date']}."
        )


    # ----------------------------------------
    # LOCAL TIME
    # ----------------------------------------

    if clean in [
        "what time is it",
        "what time is it?",
        "what is the current time",
        "what is the current time?"
    ]:

        current = get_local_datetime()

        return (
            f"The current time is "
            f"{current['time']} "
            f"({current['timezone']})."
        )


    return None


# ============================================
# WORLD TIME
# ============================================

def handle_time_request(user_message):

    text = (
        user_message
        .strip()
        .lower()
    )


    timezone_map = {

        "nigeria":
            "Africa/Lagos",

        "lagos":
            "Africa/Lagos",

        "london":
            "Europe/London",

        "uk":
            "Europe/London",

        "united kingdom":
            "Europe/London",

        "new york":
            "America/New_York",

        "los angeles":
            "America/Los_Angeles",

        "california":
            "America/Los_Angeles",

        "tokyo":
            "Asia/Tokyo",

        "japan":
            "Asia/Tokyo",

        "dubai":
            "Asia/Dubai",

        "india":
            "Asia/Kolkata",

        "south africa":
            "Africa/Johannesburg"
    }


    for location, timezone_name in timezone_map.items():

        if location in text:

            return get_time_in_timezone(
                timezone_name
            )


    return None


# ============================================
# LIVE WEB INFORMATION
# ============================================

def handle_live_request(user_message):

    result = search_web(
        user_message,
        max_results=5
    )


    if not result.get("success"):

        return (
            "I couldn't reach the live web "
            "search right now. Please try again."
        )


    results = result.get(
        "results",
        []
    )


    if not results:

        return (
            "I couldn't find reliable current "
            "information for that request."
        )


    context = format_search_results(
        result
    )


    return (
        "Here is what I found from current "
        "web sources:\n\n"
        f"{context}"
    )


# ============================================
# YOUTUBE
# ============================================

def handle_youtube_request(user_message):

    result = get_best_youtube_video(
        user_message
    )


    if not result.get("success"):

        return (
            "I couldn't find a suitable "
            "YouTube video right now."
        )


    return (
        f"🎬 {result['title']}\n\n"
        f"{result['description']}\n\n"
        f"Watch here:\n{result['url']}"
    )


# ============================================
# GEMINI FALLBACK
# ============================================

def gemini_fallback(
    user_message,
    conversation_history=None,
    api_key=None
):

    try:

        client = get_client(
            api_key
        )


        prompt = (
            AYANFE_SYSTEM_INSTRUCTION
            + "\n\n"
        )


        if conversation_history:

            prompt += (
                "Previous conversation:\n"
            )

            for message in conversation_history:

                role = message.get(
                    "role",
                    "user"
                )

                content = message.get(
                    "content",
                    ""
                )

                prompt += (
                    f"{role}: "
                    f"{content}\n"
                )

            prompt += "\n"


        prompt += (
            f"User: {user_message}\n\n"
            "AYANFE:"
        )


        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )


        return response.text


    except Exception as e:

        error_text = str(e)


        # ------------------------------------
        # QUOTA EXHAUSTED
        # ------------------------------------

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED"
            in error_text
            or "quota"
            in error_text.lower()
        ):

            return (
                "AYANFE is busy right now. 🧠\n\n"
                "This version of AYANFE is "
                "temporarily busy with its "
                "advanced AI service.\n\n"
                "Try asking me something else "
                "that I can handle with my "
                "other systems."
            )


        # ------------------------------------
        # OTHER GEMINI ERROR
        # ------------------------------------

        return (
            "AYANFE's advanced AI service "
            "is temporarily unavailable.\n\n"
            "I can still help with many "
            "other things using my built-in "
            "systems."
        )


# ============================================
# MAIN AYANFE BRAIN
# ============================================

def ask_ayanfe(
    user_message,
    conversation_history=None,
    api_key=None
):


    # ========================================
    # 1. LOCAL SYSTEM FIRST
    # ========================================

    local_answer = local_response(
        user_message
    )

    if local_answer is not None:

        return local_answer


    # ========================================
    # 2. WORLD TIME
    # ========================================

    route = route_request(
        user_message
    )

    intent = route.get(
        "intent",
        "general"
    )


    if intent == "datetime":

        time_answer = handle_time_request(
            user_message
        )

        if time_answer:

            return time_answer


        local_answer = local_response(
            user_message
        )

        if local_answer:

            return local_answer


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
    # 5. EDUCATION
    # ========================================

    if intent == "education":

        # Education can be handled by
        # AYANFE's specialist systems.
        #
        # Complex questions can still
        # fall through to Gemini.

        text = user_message.lower()

        simple_patterns = [
            "what is ",
            "what are ",
            "define ",
            "meaning of ",
            "who is ",
            "name ",
            "list "
        ]

        if any(
            pattern in text
            for pattern in simple_patterns
        ):

            # Give AYANFE's local educational
            # system a chance first.
            #
            # For now, broad educational
            # knowledge goes to the advanced
            # fallback if no local answer exists.

            pass


    # ========================================
    # 6. PROGRAMMING / WRITING / GENERAL
    # ========================================

    # These may require advanced language
    # reasoning, so Gemini is currently
    # the fallback.

    if route.get(
        "use_gemini",
        False
    ):

        return gemini_fallback(
            user_message,
            conversation_history,
            api_key
        )


    # ========================================
    # 7. LAST LOCAL FALLBACK
    # ========================================

    return (
        "I'm AYANFE AI. "
        "I don't have a built-in system "
        "for that request yet."
    )
