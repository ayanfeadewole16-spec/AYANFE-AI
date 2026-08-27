# ============================================
# AYANFE AI V2 — INDEPENDENT CORE BRAIN
# ============================================

from datetime import datetime
from zoneinfo import ZoneInfo

from master_router import route_request


# ============================================
# AYANFE IDENTITY
# ============================================

AYANFE_NAME = "AYANFE AI"
AYANFE_CREATOR = "Ayanfe"


# ============================================
# LOCAL RESPONSE SYSTEM
# ============================================

def local_response(user_message):

    text = user_message.strip().lower()

    # ----------------------------------------
    # IDENTITY
    # ----------------------------------------

    if any(phrase in text for phrase in [
        "who created you",
        "who made you",
        "who built you",
        "who is your creator",
        "who developed you"
    ]):

        return (
            "I was created by Ayanfe."
        )


    # ----------------------------------------
    # GREETINGS
    # ----------------------------------------

    if text in [
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
            "How can I help you today?"
        )


    # ----------------------------------------
    # CASUAL CONVERSATION
    # ----------------------------------------

    if text in [
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
            "I'm ready to help. What would you "
            "like to do today?"
        )


    # ----------------------------------------
    # CAPABILITIES
    # ----------------------------------------

    if text in [
        "what can you do",
        "what can you do?",
        "what are your features",
        "what are your features?",
        "help"
    ]:

        return (
            "I can help with education, programming, "
            "writing, research, everyday questions, "
            "current information, sports, YouTube, "
            "files, images, voice and more."
        )


# ----------------------------------------
# DATE
# ----------------------------------------

if (
    "today's date" in text
    or "todays date" in text
    or "what is today's date" in text
    or "what is the date today" in text
    or "what date is it" in text
    or "what day is today" in text
):

    try:
        now = datetime.now(
            ZoneInfo("Africa/Lagos")
        )

        return (
            f"Today is {now.strftime('%A, %B %d, %Y')}."
        )

    except Exception:
        now = datetime.now()

        return (
            f"Today is {now.strftime('%A, %B %d, %Y')}."
        )
        
        


    # ----------------------------------------
    # TIME — NIGERIA
    # ----------------------------------------

    if any(phrase in text for phrase in [
        "what time is it",
        "what time is it?",
        "current time",
        "current time?",
        "what is the time",
        "what is the time?"
    ]):

        try:

            now = datetime.now(
                ZoneInfo("Africa/Lagos")
            )

            return (
                "The current time in Nigeria is "
                f"{now.strftime('%I:%M %p')}."
            )

        except Exception:

            now = datetime.now()

            return (
                f"The current time is "
                f"{now.strftime('%I:%M %p')}."
            )


    # ----------------------------------------
    # SIMPLE THANKS
    # ----------------------------------------

    if text in [
        "thanks",
        "thank you",
        "thanks ayanfe",
        "thank you ayanfe"
    ]:

        return (
            "You're welcome! 😊"
        )


    # ----------------------------------------
    # SIMPLE GOODBYE
    # ----------------------------------------

    if text in [
        "bye",
        "goodbye",
        "see you",
        "see you later"
    ]:

        return (
            "Goodbye! 👋 I'll be here whenever "
            "you need me."
        )


    return None


# ============================================
# SPECIALIST SYSTEMS
# ============================================

def specialist_response(
    user_message,
    conversation_history=None
):

    route = route_request(
        user_message
    )

    intent = route.get(
        "intent",
        "general"
    )


    # ----------------------------------------
    # LOCAL / BUILT-IN
    # ----------------------------------------

    local_answer = local_response(
        user_message
    )

    if local_answer is not None:

        return local_answer


    # ----------------------------------------
    # DATE / TIME
    # ----------------------------------------

    if intent == "datetime":

        return local_response(
            user_message
        )


    # ----------------------------------------
    # LIVE INFORMATION
    # ----------------------------------------

    if intent == "live":

        try:

            from live_search import search_web

            result = search_web(
                user_message,
                max_results=5
            )

            if result.get("success"):

                results = result.get(
                    "results",
                    []
                )

                if results:

                    answer = (
                        "Here are the latest results "
                        "I found:\n\n"
                    )

                    for item in results[:5]:

                        title = item.get(
                            "title",
                            "Untitled"
                        )

                        snippet = item.get(
                            "snippet",
                            ""
                        )

                        url = item.get(
                            "url",
                            ""
                        )

                        answer += (
                            f"**{title}**\n"
                            f"{snippet}\n"
                            f"{url}\n\n"
                        )

                    return answer

        except Exception:

            pass

        return (
            "I couldn't reach the live information "
            "service right now. Please try again shortly."
        )


    # ----------------------------------------
    # YOUTUBE
    # ----------------------------------------

    if intent == "youtube":

        try:

            from youtube import (
                get_best_youtube_video
            )

            result = get_best_youtube_video(
                user_message
            )

            if result.get("success"):

                return (
                    f"🎥 **{result['title']}**\n\n"
                    f"{result['description']}\n\n"
                    f"▶️ {result['url']}"
                )

        except Exception:

            pass

        return (
            "I couldn't find a suitable YouTube "
            "video right now. Please try again."
        )


    # ----------------------------------------
    # EDUCATION
    # ----------------------------------------

    if intent == "education":

        try:

            from education import (
                education_context
            )

            return (
                "I can handle this as an educational "
                "request.\n\n"
                "Please give me the exact question or "
                "topic you want help with."
            )

        except Exception:

            return (
                "Please send me the exact educational "
                "question and I'll help you work through it."
            )


    # ----------------------------------------
    # GENERAL BUILT-IN ANSWERS
    # ----------------------------------------

    if intent == "general":

        return general_response(
            user_message
        )


    return None


# ============================================
# GENERAL AYANFE RESPONSE SYSTEM
# ============================================

def general_response(user_message):

    text = user_message.strip()

    lower = text.lower()


    # ----------------------------------------
    # SIMPLE EVERYDAY QUESTIONS
    # ----------------------------------------

    if "what is your name" in lower:

        return (
            "My name is AYANFE AI."
        )


    if "what do you do" in lower:

        return (
            "I'm AYANFE AI, a general-purpose "
            "AI assistant and learning companion. "
            "I can help with questions, learning, "
            "writing, programming, research and "
            "everyday tasks."
        )


    # ----------------------------------------
    # BASIC HEALTH INFORMATION
    # ----------------------------------------

    health_words = [
        "leg pain",
        "my leg is paining",
        "my leg hurts",
        "headache",
        "stomach pain",
        "back pain",
        "fever",
        "cough"
    ]

    if any(word in lower for word in health_words):

        return (
            "There can be many possible reasons for "
            "pain or another symptom, and I can't "
            "diagnose the cause from a message alone.\n\n"
            "For something like leg pain, it can be "
            "related to things such as a minor injury, "
            "muscle strain, or another health issue. "
            "Tell a parent, guardian, school nurse, "
            "or healthcare professional if the pain "
            "is persistent, severe, getting worse, or "
            "worrying you.\n\n"
            "If you have severe symptoms or feel that "
            "something is seriously wrong, get medical "
            "help promptly."
        )


    # ----------------------------------------
    # UNKNOWN REQUEST
    # ----------------------------------------

    return (
        "I'm AYANFE AI. I can work on this using my "
        "built-in systems. Tell me a little more about "
        "what you need, and I'll do my best to help."
    )


# ============================================
# MAIN AYANFE FUNCTION
# ============================================

def ask_ayanfe(
    user_message,
    conversation_history=None,
    api_key=None
):

    # ----------------------------------------
    # 1. AYANFE'S OWN SYSTEMS FIRST
    # ----------------------------------------

    answer = specialist_response(
        user_message,
        conversation_history
    )

    if answer is not None:

        return answer


    # ----------------------------------------
    # 2. FINAL INDEPENDENT RESPONSE
    # ----------------------------------------

    return general_response(
        user_message
    )
