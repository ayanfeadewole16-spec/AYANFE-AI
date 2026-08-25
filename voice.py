
# ============================================
# AYANFE AI V2 — VOICE SYSTEM
# ============================================

def is_voice_supported_audio(filename):
    """
    Check whether the uploaded audio format is supported.
    """

    supported = {
        ".wav",
        ".mp3",
        ".m4a",
        ".ogg",
        ".webm"
    }

    from pathlib import Path

    return Path(filename).suffix.lower() in supported


def transcribe_audio(file_path):
    """
    Convert speech audio into text.

    This function is kept separate from the UI so the
    Streamlit microphone can later connect to it.
    """

    import speech_recognition as sr

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(str(file_path)) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)

        return {
            "success": True,
            "text": text
        }

    except sr.UnknownValueError:
        return {
            "success": False,
            "error": "Speech could not be understood."
        }

    except sr.RequestError as e:
        return {
            "success": False,
            "error": f"Speech recognition service error: {e}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def voice_context():
    """
    Instructions for the future AYANFE voice interface.
    """

    return """
Voice input is integrated into the main AYANFE composer.

The interface should contain only one send button.

Desired composer:

[ + ] [ Ask AYANFE anything... ] [ microphone ] [ send ]

Do not create a large separate voice-recording section.
"""
