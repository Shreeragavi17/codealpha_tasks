import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import pyperclip
import uuid

languages = {
    "Auto Detect": "auto",
    "Arabic": "ar",
    "Bengali": "bn",
    "Chinese (Simplified)": "zh-CN",
    "Dutch": "nl",
    "English": "en",
    "French": "fr",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Hindi": "hi",
    "Indonesian": "id",
    "Italian": "it",
    "Japanese": "ja",
    "Kannada": "kn",
    "Korean": "ko",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Russian": "ru",
    "Spanish": "es",
    "Swedish": "sv",
    "Tamil": "ta",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Vietnamese": "vi",
}

lang_names = list(languages.keys())

if "src_lang" not in st.session_state:
    st.session_state.src_lang = "Auto Detect"
if "tgt_lang" not in st.session_state:
    st.session_state.tgt_lang = "Tamil"

def translate_text(text, src_lang, tgt_lang):
    try:
        result = GoogleTranslator(source=src_lang, target=tgt_lang).translate(text)
        if src_lang == "auto":
            detected = GoogleTranslator(source="auto", target=tgt_lang).detect(text)
            st.info(f"🔍 Detected Language: **{detected}**")
        return result
    except Exception as e:
        st.error(f"Translation Error: {e}")
        return ""

def speak_text(text, lang_code):
    if not text or not text.strip():
        st.warning("No text to speak")
        return
    try:
        file_name = f"speech_{uuid.uuid4().hex}.mp3"
        tts = gTTS(text=text, lang=lang_code)
        tts.save(file_name)
        st.audio(file_name, autoplay=True)
    except Exception as e:
        st.error(f"TTS Error: {e}")

st.set_page_config(page_title="Translator Tool", page_icon="🌍")
st.title("🌍 Language Translation Tool")

col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("Source Language", lang_names, index=lang_names.index(st.session_state.src_lang))
with col2:
    tgt_lang = st.selectbox("Target Language", lang_names[1:], index=lang_names[1:].index(st.session_state.tgt_lang))

st.session_state.src_lang = src_lang
st.session_state.tgt_lang = tgt_lang

if st.button("🔁 Swap Languages"):
    if st.session_state.src_lang != "Auto Detect":
        temp = st.session_state.src_lang
        st.session_state.src_lang = st.session_state.tgt_lang
        st.session_state.tgt_lang = temp
    else:
        st.warning("Cannot swap when Auto Detect is selected!")
    st.rerun()

text = st.text_area("Enter text")

if st.button("Translate"):
    if not text.strip():
        st.warning("Please enter text first!")
    else:
        translated = translate_text(text, languages[src_lang], languages[tgt_lang])
        st.session_state["translated"] = translated
        st.session_state["tgt_lang_code"] = languages[tgt_lang]

if "translated" in st.session_state:
    st.success("Translation Done!")
    st.text_area("Translated Text", st.session_state["translated"], height=150)
    col3, col4 = st.columns(2)
    with col3:
        if st.button("📋 Copy"):
            pyperclip.copy(st.session_state["translated"])
            st.success("Copied to clipboard!")
    with col4:
        if st.button("🔊 Listen"):
            speak_text(st.session_state["translated"], st.session_state["tgt_lang_code"])
