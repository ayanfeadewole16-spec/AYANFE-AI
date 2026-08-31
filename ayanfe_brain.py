============================================
AYANFE AI V2 — INDEPENDENT CORE BRAIN
============================================
from datetime import datetime
from zoneinfo import ZoneInfo
import re
from master_router import route_request
from live_search import search_web
from youtube import get_best_youtube_video
============================================
AYANFE IDENTITY
============================================
AYANFE_SYSTEM_INSTRUCTION = """
You are AYANFE AI, a modern general-purpose
AI assistant and learning companion.
Your creator is Ayanfe.
You are designed to operate independently.
Do not unnecessarily depend on external AI services.
Do not automatically generate quizzes, practice
questions, or extra sections unless requested or
genuinely useful.
Understand normal conversation and conversational
follow-ups. Do not assume every user message must
contain a keyword.
"""
============================================
TEXT NORMALIZATION
============================================
def normalize(text):
if not text:
return ""
text = str(text).strip().lower()

# Normalize repeated spaces
text = re.sub(r"\s+", " ", text)

return text
============================================
CONVERSATION CONTEXT
============================================
def has_conversation(conversation_history):
return bool(
conversation_history
and len(conversation_history) > 0
)
def previous_message(conversation_history):
if not conversation_history:
    return ""

for message in reversed(conversation_history):
    content = message.get("content", "")

    if content:
        return str(content)

return ""
============================================
LOCAL AYANFE RESPONSES
============================================
def local_response(
user_message,
conversation_history=None
):
text = normalize(user_message)

if not text:
    return None


# ========================================
# IDENTITY
# ========================================

identity_patterns = [
    "who created you",
    "who made you",
    "who built you",
    "who is your creator",
"who's your creator"
]

if any(
    pattern in text
    for pattern in identity_patterns
):
    return "I was created by Ayanfe."


# ========================================
# GREETINGS
# ========================================

greeting_patterns = [
    "hi",
    "hello",
    "hey",
    "hiya",
    "good morning",
    "good afternoon",
    "good evening"
]

if text in greeting_patterns:

    return (
        "I'm doing great! 😊 "
        "I'm ready to help. What would you "
        "like to talk about today?"
    )


# ========================================
# NATURAL SHORT CONVERSATION
# ========================================
#
# Short conversational replies should not
# automatically be treated as unsupported
# technical requests.
#
# The important improvement is that this
# considers whether there is already a
# conversation.
# ========================================

if has_conversation(conversation_history):

    short_message = (
        len(text.split()) <= 8
    )

    conversational_punctuation = (
        "!" in text
        or "?" in text
    )

    if short_message or conversational_punctuation:

        conversational_signals = [
            "nice",
            "cool",
            "great",
            "good",
            "okay",
            "ok",
            "alright",
            "thanks",
            "thank you",
            "wow",
            "interesting",
            "really",
            "sure",
            "yes",
            "yeah",
            "yep",
            "no",
            "nah",
            "true",
            "exactly"
        ]

        if any(
            signal in text
            for signal in conversational_signals
        ):

            return (
                "😊 Glad to hear that. "
                "What would you like to talk about next?"
            )


# ========================================
# DATE
# ========================================

date_patterns = [
    "today date",
    "today's date",
    "todays date",
    "what date is it",
    "what is the date",
    "what is the date today",
    "what day is today",
    "which date is today",
    "what day are we on",
    "date today"
]

if any(
    pattern in text
    for pattern in date_patterns
):

    # Nigeria / West Africa local time.
    # This avoids restricting AYANFE to UTC.
    now = datetime.now(
        ZoneInfo("Africa/Lagos")
    )

    return (
        f"Today is "
        f"{now.strftime('%A, %B %d, %Y')}."
    )


# ========================================
# TIME
# ========================================

time_patterns = [
    "what time is it",
    "what is the time",
    "current time",
    "time right now",
    "tell me the time",
    "what's the time"
]

if any(
    pattern in text
    for pattern in time_patterns
):

    now = datetime.now(
        ZoneInfo("Africa/Lagos")
    )

    return (
        f"The current local time is "
        f"{now.strftime('%I:%M %p')}."
    )


# ========================================
# CAPABILITIES
# ========================================

capability_patterns = [
    "what can you do",
    "what are your features",
    "what do you do",
    "how can you help me",
    "what can you help with"
]

if any(
    pattern in text
    for pattern in capability_patterns
):

    return (
        "I can help with education, general "
        "questions, current information, "
        "football and sports, programming, "
        "writing, research, YouTube, files, "
        "and everyday questions."
    )


return None
============================================
LIVE INFORMATION
============================================
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

results = result.get(
    "results",
    []
)

if not results:

    return (
        "I couldn't find reliable current "
        "information for that request."
    )

answer = (
    "Here's what I found from current "
    "web sources:\n\n"
)

for item in results[:5]:

    title = item.get(
        "title",
        "Untitled source"
    )

    url = item.get(
        "url",
        ""
    )

    snippet = item.get(
        "snippet",
        ""
    )

    answer += f"**{title}**\n"

    if snippet:
        answer += f"{snippet}\n"

    if url:
        answer += f"Source: {url}\n"

    answer += "\n"

return answer.strip()
============================================
YOUTUBE
============================================
def handle_youtube_request(user_message):
result = get_best_youtube_video(
    user_message
)

if not result.get("success"):

    return (
        "I couldn't find a suitable YouTube "
        "video for that request."
    )

title = result.get(
    "title",
    ""
)

url = result.get(
    "url",
    ""
)

description = result.get(
    "description",
    ""
)

answer = f"**{title}**\n\n"

if description:
    answer += f"{description}\n\n"

if url:
    answer += (
        f"Watch on YouTube: {url}"
    )

return answer
============================================
GENERAL BUILT-IN FALLBACK
============================================
def general_fallback(
user_message,
conversation_history=None
):
text = normalize(user_message)

# If this is a continuation of an existing
# conversation, respond conversationally
# rather than claiming the request is
# unsupported.

if has_conversation(conversation_history):

    previous = normalize(
        previous_message(
            conversation_history
        )
    )

    if previous:

        return (
            "I understand you're continuing "
            "our conversation. Tell me a little "
            "more about what you mean and I'll "
            "work with you."
        )


# For an unfamiliar request, use web search
# as AYANFE's independent information fallback.
#
# This does NOT use Gemini.

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
            "I found some information that may "
            "help with that:\n\n"
        )

        for item in results[:3]:

            title = item.get(
                "title",
                ""
            )

            snippet = item.get(
                "snippet",
                ""
            )

            url = item.get(
                "url",
                ""
            )

            if title:
                answer += (
                    f"**{title}**\n"
                )

            if snippet:
                answer += (
                    f"{snippet}\n"
                )

            if url:
                answer += (
                    f"Source: {url}\n"
                )

            answer += "\n"

        return answer.strip()


return (
    "I'm AYANFE AI. I don't have enough "
    "information to answer that accurately "
    "yet. You can explain what you mean in "
    "another way and I'll try again."
)
============================================
MAIN AYANFE BRAIN
============================================
def ask_ayanfe(
user_message,
conversation_history=None,
api_key=None
):
# ========================================
# 1. LOCAL SYSTEMS FIRST
# ========================================

answer = local_response(
    user_message,
    conversation_history
)

if answer is not None:
    return answer


# ========================================
# 2. ROUTER
# ========================================

route = route_request(
    user_message
)

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
        "I can work with the education "
        "request. Send me the actual question "
        "or problem and I'll help you work "
        "through it."
    )


# ========================================
# 7. PROGRAMMING
# ========================================

if intent == "programming":

    return (
        "I can help with the programming "
        "request. Send the code, error, or "
        "describe what you want to build."
    )


# ========================================
# 8. WRITING
# ========================================

if intent == "writing":

    return (
        "I can help with the writing request. "
        "Send the text or describe what you "
        "want to write."
    )


# ========================================
# 9. GENERAL INDEPENDENT FALLBACK
# ========================================

return general_fallback(
    user_message,
    conversation_history
)

