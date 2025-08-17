import io
import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS

# ---------- Page config ----------
st.set_page_config(page_title="Universal Language Translator", layout="centered", page_icon="🌍")

# ---------- Session State ----------
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "translated_lang" not in st.session_state:
    st.session_state.translated_lang = "en"
if "tts_bytes" not in st.session_state:
    st.session_state.tts_bytes = None

# ---------- Styles ----------
st.markdown("""
    <style>
        .translated-text {
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            font-size: 18px;
            color: #333333 !important;
            border: 1px solid #dddddd;
            margin-top: 10px;
        }
        .language-label {
            color: #2196F3;
            font-weight: bold;
            margin-bottom: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.markdown("""
    <h1 style='text-align:center; color:#4CAF50;'>🌍 Universal Language Translator</h1>
    <p style='text-align:center; font-size:16px;'>Translate text between any languages easily</p>
""", unsafe_allow_html=True)

# ---------- Supported languages ----------
LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ar': 'Arabic',
    'hi': 'Hindi'
}

# gTTS language code mapping (adjust as needed)
GTTS_LANG_MAP = {
    'en': 'en',
    'es': 'es',
    'fr': 'fr',
    'de': 'de',
    'it': 'it',
    'pt': 'pt',
    'ru': 'ru',
    'zh': 'zh-CN',   # gTTS expects zh-CN or zh-TW
    'ja': 'ja',
    'ko': 'ko',
    'ar': 'ar',
    'hi': 'hi'
}


def to_code(name: str) -> str:
    """Get ISO code from human name."""
    return [k for k, v in LANGUAGES.items() if v == name][0]


# Cache TTS so repeated clicks don’t re-generate
@st.cache_data(show_spinner=False)
def synthesize_speech(text: str, lang_code: str) -> bytes:
    buf = io.BytesIO()
    tts = gTTS(text=text, lang=lang_code)
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()


# ---------- UI Controls ----------
col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox("Select source language", ["Auto Detect"] + list(LANGUAGES.values()))

with col2:
    target_lang = st.selectbox("Select target language", list(LANGUAGES.values()), index=0)

text_to_translate = st.text_area("Enter text to translate", height=150, placeholder="Type or paste text here...", max_chars=5000)
debug_mode = st.checkbox("Show debug information")

# ---------- Translate Button ----------
if st.button("Translate 🔄", type="primary"):
    if not text_to_translate.strip():
        st.warning("Please enter some text to translate.")
    else:
        with st.spinner("Translating..."):
            try:
                src_code = "auto" if source_lang == "Auto Detect" else to_code(source_lang)
                dest_code = to_code(target_lang)

                if debug_mode:
                    st.write(f"Debug: Translating from {src_code} to {dest_code}")
                    st.write(f"Original text length: {len(text_to_translate)}")

                translated = GoogleTranslator(source=src_code, target=dest_code).translate(text_to_translate)

                # Persist results across reruns
                st.session_state.translated_text = translated
                st.session_state.translated_lang = dest_code
                st.session_state.tts_bytes = None  # reset TTS cache for new text

                st.success("Translation successful!")

            except Exception as e:
                st.error(f"⚠️ Translation failed: {str(e)}")
                st.info(
                    "Troubleshooting:\n"
                    "1) Try shorter text (under 500 chars)\n"
                    "2) Check internet\n"
                    "3) Try a different language pair\n"
                    "4) Enable debug for details"
                )

# ---------- Show Result (if exists) ----------
if st.session_state.translated_text:
    st.markdown('<div class="language-label">Translated Text:</div>', unsafe_allow_html=True)
    st.text_area("", value=st.session_state.translated_text, height=150, disabled=True)

    # ---------- Read Aloud ----------
    read_col, dl_col = st.columns([1, 1])
    with read_col:
        if st.button("🔊 Read Aloud"):
            try:
                # Map/validate lang for gTTS
                gtts_lang = GTTS_LANG_MAP.get(st.session_state.translated_lang, None)
                if gtts_lang is None:
                    st.warning(f"Speech not supported for '{st.session_state.translated_lang}'. Falling back to English.")
                    gtts_lang = "en"

                with st.spinner("Generating speech..."):
                    audio_bytes = synthesize_speech(st.session_state.translated_text, gtts_lang)
                    st.session_state.tts_bytes = audio_bytes

            except Exception as e:
                st.error(f"⚠️ Speech synthesis failed: {str(e)}")

    # Play audio if ready (no autoplay due to browser policy; click play)
    if st.session_state.tts_bytes:
        st.audio(st.session_state.tts_bytes, format="audio/mp3")

    # ---------- Download MP3 ----------
    with dl_col:
        if st.session_state.tts_bytes:
            st.download_button(
                "⬇️ Download MP3",
                data=st.session_state.tts_bytes,
                file_name=f"translation_{st.session_state.translated_lang}.mp3",
                mime="audio/mpeg",
            )

    if debug_mode:
        st.json({
            "translated_lang": st.session_state.translated_lang,
            "translated_length": len(st.session_state.translated_text),
            "audio_ready": st.session_state.tts_bytes is not None
        })
