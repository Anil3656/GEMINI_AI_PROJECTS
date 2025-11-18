# tts.py
"""
Text-To-Speech helper using gTTS (simple and free).
Saves mp3 to a temporary file and returns the path.
"""

import os
import uuid
from typing import Optional

def text_to_speech_gtts(text: str, lang: str = "te") -> str:
    """
    Create an MP3 file with gTTS and return the local filepath.
    lang: two-letter language code (e.g., 'en', 'te', 'hi', 'fr', 'es')
    """
    try:
        from gtts import gTTS
    except Exception as e:
        raise RuntimeError("gTTS not installed. Install with `pip install gTTS`.") from e

    if not text:
        raise ValueError("No text provided for TTS.")

    file_name = f"tts_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang=lang)
    tts.save(file_name)
    return file_name
