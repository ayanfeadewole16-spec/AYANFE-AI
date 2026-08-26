# ============================================
# AYANFE AI V2 — CORE BRAIN
# ============================================

import os
from datetime import datetime

from google import genai

from master_router import route_request


MODEL = "gemini-3.6-flash"


# ============================================
# AYANFE IDENTITY
# ============================================

AYANFE_SYSTEM_INSTRUCTION = """
You are AYANFE AI, a modern general-purpose AI
assistant and learning companion.

Your creator is Ayanfe.

If asked who created you, answer:
"I was created by Ayanfe."

You are NOT an education-only assistant.

You can help with:
education, general questions, current information,
football and sports, programming, writing, research,
social-life questions, files, images, YouTube, voice,
and everyday questions.

For educational questions, when appropriate use:

1. Simple explanation
2. Detailed explanation
3. Example
4. Practice question
5. Quiz

Do not claim information is current unless it has
actually been obtained from a current source.

Be helpful, accurate and clear.
"""


# ============================================
# GEMINI CLIENT
# ============================================

def get_client(api_key=None):

    key = api_key or os.getenv("GEMINI_API_KEY")

    if not key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(api_key=key)


# ============================================
# LOCAL AYANFE RESPONSES
# ============================================

def local_response(user_message):

    clean = user_message.strip().lower()

    # ----------------------------------------
    # CREATOR
    # ----------------------------------------

    if clean in [
        "who created you?",
        "who created you",
        "who made you?",
        "who made you",
        "who built you?",
        "who built you",
        "who is your creator?"
    ]:

        return "I was created by Ayanfe."


   # ----------------------------------------
# GREETINGS / CASUAL CONVERSATION
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
    "good evening",
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
        "I'm ready to help. What would you like "
        "to do today?"
    )
    # ----------------------------------------
    # CAPABILITIES
    # ----------------------------------------

    if clean in [
        "what can you do?",
        "what can you do",
        "what are your features?",
        "help"
    ]:

        return (
            "I can help with education, writing, "
            "programming, research, current information, "
            "sports, YouTube, files, everyday questions "
            "and much more."
        )


    # ----------------------------------------
    # DATE
    # ----------------------------------------

    if clean in [
        "what is today's date?",
        "what is today's date",
        "what date is it?",
        "what date is it"
    ]:

        today = datetime.now().strftime("%A, %B %d, %Y")

        return f"Today is {today}."


    # ----------------------------------------
    # TIME
    # ----------------------------------------

    if clean in [
        "what time is it?",
        "what time is it",
        "what is the current time?",
        "what is the current time"
    ]:

        current_time = datetime.now().strftime("%I:%M %p")

        return f"The current time is {current_time}."


    return None


# ============================================
# GEMINI FALLBACK
# ============================================

def gemini_fallback(
    user_message,
    conversation_history=None,
    api_key=None
):

    client = get_client(api_key)

    prompt = AYANFE_SYSTEM_INSTRUCTION + "\n\n"

    if conversation_history:

        prompt += "Previous conversation:\n"

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
                f"{role}: {content}\n"
            )

        prompt += "\n"

    prompt += (
        f"User: {user_message}\n\n"
        "AYANFE:"
    )

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text

    except Exception as e:

        error_text = str(e)

        # NEVER expose Gemini technical errors
        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
        ):

            return (
                "AYANFE is busy right now. 🧠\n\n"
                "This version of AYANFE is temporarily "
                "busy with its AI service. Try asking me "
                "something else, or try again later."
            )

        return (
            "AYANFE is temporarily unavailable. "
            "Please try again shortly."
        )


# ============================================
# MAIN AYANFE BRAIN
# ============================================

def ask_ayanfe(
    user_message,
    conversation_history=None,
    api_key=None
):

    # ----------------------------------------
    # 1. TRY LOCAL AYANFE FIRST
    # ----------------------------------------

    local_answer = local_response(
        user_message
    )

    if local_answer is not None:
        return local_answer


    # ----------------------------------------
    # 2. ASK MASTER ROUTER
    # ----------------------------------------

    route = route_request(
        user_message
    )

    intent = route.get(
        "intent",
        "general"
    )

    use_gemini = route.get(
        "use_gemini",
        True
    )


    # ----------------------------------------
    # 3. CURRENT SPECIALIST SYSTEMS
    # ----------------------------------------
    #
    # These will be connected next:
    #
    # live_search
    # education
    # youtube
    # memory
    # files
    # voice
    #
    # For now, unsupported specialist
    # requests safely fall through.
    # ----------------------------------------


    # ----------------------------------------
    # 4. GEMINI LAST-RESORT FALLBACK
    # ----------------------------------------

    if use_gemini:

        return gemini_fallback(
            user_message,
            conversation_history,
            api_key
        )


    # ----------------------------------------
    # 5. SAFE FALLBACK
    # ----------------------------------------

    return (
        "I'm AYANFE AI. I couldn't handle that "
        "request with my current systems yet."
    )
