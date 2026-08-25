
# ============================================
# AYANFE AI V2 — CORE BRAIN
# ============================================

import os
from google import genai


MODEL = "gemini-3.6-flash"

AYANFE_SYSTEM_INSTRUCTION = """
You are AYANFE AI, a modern general-purpose AI assistant
and learning companion.

Your creator is Ayanfe.

If asked "Who created you?", answer:
"I was created by Ayanfe."

You are NOT an education-only assistant.

You can help with education, general questions, current
information, football and sports, programming, writing,
research, social-life questions, files, images, YouTube,
voice and everyday questions.

For educational questions, when appropriate use:
1. Simple explanation
2. Detailed explanation
3. Example
4. Practice question
5. Quiz

Do not claim information is current unless it has actually
been obtained from a current source.

Be helpful, accurate and clear.
"""


def get_client(api_key=None):
    """
    Create a Gemini client.

    On Streamlit Cloud, the API key will come from
    Streamlit Secrets.

    During local development it can come from an
    environment variable.
    """

    key = api_key or os.getenv("GEMINI_API_KEY")

    if not key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(api_key=key)


def ask_ayanfe(
    user_message,
    conversation_history=None,
    api_key=None
):
    """
    Send a message to AYANFE.
    """

    client = get_client(api_key)

    prompt = AYANFE_SYSTEM_INSTRUCTION + "\n\n"

    if conversation_history:
        prompt += "Previous conversation:\n"

        for message in conversation_history:
            role = message.get("role", "user")
            content = message.get("content", "")

            prompt += f"{role}: {content}\n"

        prompt += "\n"

    prompt += f"User: {user_message}\n\nAYANFE:"

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text
