# ============================================
# AYANFE AI V2 — VOICE SYSTEM
# ============================================

from pathlib import Path


SUPPORTED_AUDIO = {
    ".wav",
    ".mp3",
    ".m4a",
    ".ogg",
    ".webm"
}


def is_voice_supported_audio(filename):

    return Path(
        filename
    ).suffix.lower() in SUPPORTED_AUDIO


def transcribe_audio(file_path):

    """
    Convert recorded speech into text.

    Uses SpeechRecognition when available.
    """

    try:

        import speech_recognition as sr

        recognizer = sr.Recognizer()

        with sr.AudioFile(
            str(file_path)
        ) as source:

            audio = recognizer.record(
                source
            )

        text = recognizer.recognize_google(
            audio
        )

        return {
            "success": True,
            "text": text
        }

    except sr.UnknownValueError:

        return {
            "success": False,
            "error": "I couldn't understand the recording."
        }

    except sr.RequestError:

        return {
            "success": False,
            "error": "Voice recognition is temporarily unavailable."
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


def voice_context():

    return """
Voice input is part of AYANFE's main composer.

The intended flow is:

Microphone
→ speech recording
→ transcription
→ text
→ AYANFE

Voice should not create a separate large section.
"""
