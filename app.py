import streamlit as st
from transcribe import transcribe_audio
from match_verse import find_best_match
from quran_api import get_tafsir, get_translation
from PIL import Image
import sounddevice as sd
from scipy.io.wavfile import write
import base64

#removing hamburger 
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

logo = Image.open("photo.png")

# Convert image to base64 to embed with HTML
with open("photo.png", "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode()

# Use HTML to center the image
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{encoded}" width="300">
    </div>
    """,
    unsafe_allow_html=True
)

# Session state
if "recording" not in st.session_state:
    st.session_state["recording"] = False

# Title
st.markdown("<h1 style='text-align: center;'>🎙️ Surah Voice Detector</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Upload Section
st.subheader("📤 Upload Your Recitation (.wav)")
audio_file = st.file_uploader("", type=["wav"])
if audio_file:
    with open("temp.wav", "wb") as f:
        f.write(audio_file.read())

    with st.spinner("⏳ Transcribing your recitation..."):
        arabic_text = transcribe_audio("temp.wav")

    st.success("✅ Transcription complete!")
    st.markdown(f"**📝 Transcribed Text:** {arabic_text}")

    with st.spinner("🔍 Matching verse..."):
        match = find_best_match(arabic_text)

    if match:
        st.success(f"📌 Matched: **Surah {match['surah']} - Ayah {match['ayah']}**")
        st.markdown(f"**📖 Verse:** {match['text']}")

        surah_number = int(match['surah'].split("-")[0].strip())
        tafsir = get_tafsir(surah_number, match['ayah'])
        translation = get_translation(surah_number, match['ayah'])

        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📘 Translation")
            st.write(translation.get('data', {}).get('translation', '❌ Not found'))

        with col2:
            st.subheader("📗 Tafsir")
            st.write(tafsir.get('data', {}).get('tafsir', '❌ Tafsir not found'))

    else:
        st.error("❌ No matching verse found.")
        st.markdown(f"**📝 Transcribed:** {arabic_text}")

# Live Recording Section
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### 🎤 Or Record Using Microphone")

if not st.session_state["recording"]:
    if st.button("🎙️ Start Recording"):
        st.session_state["recording"] = True
else:
    if st.button("⏹️ Stop Recording"):
        st.info("🔴 Recording for 10 seconds...")
        fs = 16000
        duration = 10
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        write("live_input.wav", fs, recording)
        st.success("✅ Recording saved!")

        st.session_state["recording"] = False

        with st.spinner("⏳ Transcribing..."):
            arabic_text = transcribe_audio("live_input.wav")
        st.markdown(f"**📝 Transcribed:** {arabic_text}")

        with st.spinner("🔍 Matching verse..."):
            match = find_best_match(arabic_text)

        if match:
            st.success(f"📌 Matched: **Surah {match['surah']} - Ayah {match['ayah']}**")
            st.markdown(f"**📖 Verse:** {match['text']}")

            surah_number = int(match['surah'].split("-")[0].strip())
            tafsir = get_tafsir(surah_number, match['ayah'])
            translation = get_translation(surah_number, match['ayah'])

            st.markdown("---")
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📘 Translation")
                st.write(translation.get('data', {}).get('translation', '❌ Not found'))

            with col2:
                st.subheader("📗 Tafsir")
                st.write(tafsir.get('data', {}).get('tafsir', '❌ Tafsir not found'))

        else:
            st.error("❌ No matching verse found.")
            st.markdown(f"**📝 Transcribed:** {arabic_text}")
