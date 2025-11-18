# stt.py
"""
Speech-To-Text helper.
Supports two strategies:
 - Whisper (local) if installed
 - Simple fallback: return empty or raise if not available

Usage:
    from stt import speech_to_text
    text = speech_to_text("path/to/audio.mp3")
"""

import os
from typing import Optional

def _transcribe_with_whisper(audio_path: str) -> str:
    try:
        import whisper
    except Exception as e:
        raise RuntimeError("Whisper not installed. Install openai-whisper or use a different STT.") from e

    model = whisper.load_model("base")  # choose model size: tiny, base, small, medium, large
    result = model.transcribe(audio_path)
    return result.get("text", "").strip()

def speech_to_text(audio_path: str, engine: str = "whisper") -> str:
    """
    Transcribe audio file at audio_path and return text.
    engine: "whisper" (default) or other future options.
    """
    if engine == "whisper":
        return _transcribe_with_whisper(audio_path)
    else:
        raise ValueError(f"Unknown STT engine: {engine}")
