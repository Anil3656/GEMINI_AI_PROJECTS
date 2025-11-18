# app.py
import streamlit as st
import os
import time
from pathlib import Path

from config import GOOGLE_GENAI_API_KEY
from translator import translate_text_with_gemini
from tts import text_to_speech_gtts
from stt import speech_to_text

# --- Page Config ---
st.set_page_config(
    page_title="Multi-Language Voice Translator",
    layout="centered",
    page_icon="🌐"
)

# ---------------------- CUSTOM CLEAN UI CSS ----------------------

# -----------------------------------------------------------------

# --- Header ---
st.markdown("### Multi-Language Voice Translator")
st.markdown('<div class="app-sub">Translate text or speech across languages using Gemini + LangChain.</div>', unsafe_allow_html=True)

# --- Controls ---
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox(
        "Source language",
        ["English", "Telugu", "Hindi", "Tamil", "Kannada", "Malayalam", "French", "Spanish"]
    )
with col2:
    target_lang = st.selectbox(
        "Target language",
        ["Telugu", "English", "Hindi", "Tamil", "Kannada", "Malayalam", "French", "Spanish"]
    )

st.markdown("---")

# Text input area
text_input = st.text_area(
    "Type text to translate (or use Audio Upload below):",
    height=120,
    placeholder="Type or paste text here..."
)

# Audio upload for STT
st.markdown("### Speech Input")
audio_file = st.file_uploader(
    "Upload audio file (mp3 / wav)",
    type=["mp3", "wav", "m4a"]
)

# Buttons
colA, colB = st.columns(2)
with colA:
    translate_btn = st.button("✨ Translate Text")
with colB:
    stt_btn = st.button("🎙️ Transcribe Audio & Translate")

# API key validation
if not GOOGLE_GENAI_API_KEY or len(GOOGLE_GENAI_API_KEY) < 20:
    st.warning("⚠️ Invalid Google Gemini API key. Please set it in config.py")
    st.stop()

# --- Actions ---
translated_text = None
translated_audio_path = None

# TEXT → TRANSLATION
if translate_btn:
    if not text_input.strip():
        st.warning("Please provide text to translate.")
    else:
        with st.spinner("Translating..."):
            try:
                translated_text = translate_text_with_gemini(
                    text_input, source_lang, target_lang
                )
                st.success("✅ Translation complete")

                st.subheader("Translated text")
                st.text_area("Result", translated_text, height=200)

            except Exception as e:
                st.error(f"Translation error: {e}")

    # TTS option
    if translated_text:
        lang_code_map = {
            "English": "en", "Telugu": "te", "Hindi": "hi", "Tamil": "ta",
            "Kannada": "kn", "Malayalam": "ml", "French": "fr", "Spanish": "es"
        }

        tts_lang = lang_code_map.get(target_lang, "en")

        if st.checkbox("🔊 Generate audio (TTS) for translated text"):
            with st.spinner("Generating audio..."):
                translated_audio_path = text_to_speech_gtts(translated_text, tts_lang)
                st.audio(translated_audio_path)
                st.success("Audio ready 🎧")

# AUDIO → STT → TRANSLATE
if stt_btn:
    if not audio_file:
        st.warning("Please upload an audio file to transcribe.")
    else:
        temp_audio_path = Path(f"uploaded_{int(time.time())}_{audio_file.name}")
        with open(temp_audio_path, "wb") as f:
            f.write(audio_file.getbuffer())

        try:
            with st.spinner("Transcribing audio (Whisper)..."):
                transcribed = speech_to_text(str(temp_audio_path), engine="whisper")

            st.subheader("Transcribed Text:")
            st.write(transcribed)

            with st.spinner("Translating..."):
                translated_text = translate_text_with_gemini(transcribed, source_lang, target_lang)

            st.subheader("Translated Text:")
            st.text_area("Result", translated_text, height=200)

            # TTS option
            lang_code_map = {
                "English": "en", "Telugu": "te", "Hindi": "hi", "Tamil": "ta",
                "Kannada": "kn", "Malayalam": "ml", "French": "fr", "Spanish": "es"
            }

            tts_lang = lang_code_map.get(target_lang, "en")

            if st.checkbox("🔊 Generate audio (TTS) for translated text"):
                with st.spinner("Generating audio..."):
                    translated_audio_path = text_to_speech_gtts(translated_text, tts_lang)
                    st.audio(translated_audio_path)
                    st.success("Audio ready 🎧")

        except Exception as e:
            st.error(f"STT or translation error: {e}")
        finally:
            try:
                os.remove(temp_audio_path)
            except:
                pass

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#555;'>Built with ❤️ using Gemini + LangChain. "
    "Want auto-detect, chat mode, or camera input? Let's collaborate!</p>",
    unsafe_allow_html=True
)
