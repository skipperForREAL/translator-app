import streamlit as st
from deep_translator import GoogleTranslator

# Set page config
st.set_page_config(
    page_title="🌍 Universal Language Translator",
    layout="centered",
    page_icon=""
)

# Custom CSS to ensure text visibility
st.markdown("""
    <style>
        .translated-text {
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            font-size: 18px;
            color: #333333 !important;  /* Explicit dark color */
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

# Title and description
st.markdown("""
    <h1 style='text-align:center; color:#4CAF50;'>
        🌍 Universal Language Translator
    </h1>
    <p style='text-align:center; font-size:16px;'>
        Translate text between any languages easily
    </p>
""", unsafe_allow_html=True)

# Supported languages
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

# Language selection
col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox(
        "Select source language",
        ["Auto Detect"] + list(LANGUAGES.values())
    )

with col2:
    target_lang = st.selectbox(
        "Select target language",
        list(LANGUAGES.values()),
        index=0
    )

# Text input
text_to_translate = st.text_area(
    "Enter text to translate",
    height=150,
    placeholder="Type or paste text here...",
    max_chars=5000
)

# Debugging section
debug_mode = st.checkbox("Show debug information")

if st.button("Translate 🔄", type="primary"):
    if not text_to_translate.strip():
        st.warning("Please enter some text to translate.")
    else:
        with st.spinner("Translating..."):
            try:
                # Get language codes
                src_code = "auto" if source_lang == "Auto Detect" else \
                    [k for k, v in LANGUAGES.items() if v == source_lang][0]
                dest_code = [k for k, v in LANGUAGES.items() if v == target_lang][0]

                if debug_mode:
                    st.write(f"Debug: Translating from {src_code} to {dest_code}")
                    st.write(f"Original text: {text_to_translate}")

                # Perform translation
                translated = GoogleTranslator(
                    source=src_code,
                    target=dest_code
                ).translate(text_to_translate)

                if debug_mode:
                    st.write(f"Raw translation result: {translated}")

                # Display result with multiple fallback methods
                st.markdown('<div class="language-label">Translated Text:</div>', unsafe_allow_html=True)

                # # Method 1: Using custom CSS class
                # st.markdown(f'<div class="translated-text">{translated}</div>', unsafe_allow_html=True)

                # Method 2: Plain text as fallback
                st.text_area("", value=translated, height=150, disabled=True)

                # Method 3: Using success message
                st.success("Translation successful!")

                if debug_mode:
                    st.json({
                        "source": src_code,
                        "target": dest_code,
                        "original_length": len(text_to_translate),
                        "translated_length": len(translated)
                    })

            except Exception as e:
                st.error(f"⚠️ Translation failed: {str(e)}")
                st.info("""
                    Troubleshooting steps:
                    1. Try shorter text (under 500 characters)
                    2. Check your internet connection
                    3. Try a different language pair
                    4. Enable debug mode for more information
                """)