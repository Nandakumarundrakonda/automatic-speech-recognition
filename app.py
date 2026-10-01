import streamlit as st
import whisper
import tempfile
import os

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Speech to Text",
    page_icon="🎙️",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 35px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 600;
        margin-top: 20px;
    }

    .transcript-box {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd;
        font-size: 18px;
        line-height: 1.7;
    }

    .timestamp-box {
        padding: 12px;
        margin: 8px 0;
        border-radius: 8px;
        border: 1px solid #ddd;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="main-title">🎙️ AI Speech to Text</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Automatic Speech Recognition powered by OpenAI Whisper'
    '</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Load Whisper Model
# -----------------------------
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("small")


model = load_whisper_model()

# -----------------------------
# Upload Section
# -----------------------------
st.markdown(
    '<div class="section-title">📤 Upload Audio</div>',
    unsafe_allow_html=True
)

language = st.selectbox(
    "🌐 Select Language",
    [
        "Auto Detect",
        "English",
        "Hindi",
        "Telugu",
        "Tamil",
        "Kannada"
    ]
)

uploaded_file = st.file_uploader(
    "Choose an audio file",
    type=["wav", "mp3", "m4a", "mpeg", "mpga", "webm"]
)

# -----------------------------
# Audio Processing
# -----------------------------
if uploaded_file is not None:

    st.audio(uploaded_file)

    st.write(
        f"**File:** {uploaded_file.name}  \n"
        f"**Size:** {uploaded_file.size / 1024:.2f} KB"
    )

    if st.button("🚀 Transcribe Audio", use_container_width=True):

        with st.spinner("🤖 AI is transcribing your audio..."):

            file_extension = os.path.splitext(
                uploaded_file.name
            )[1]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=file_extension
            ) as temp_audio:

                temp_audio.write(uploaded_file.read())
                temp_audio_path = temp_audio.name

            try:

                # -----------------------------
                # Language Selection
                # -----------------------------
                if language == "Auto Detect":

                    result = model.transcribe(
                        temp_audio_path
                    )

                else:

                    language_codes = {
                        "English": "en",
                        "Hindi": "hi",
                        "Telugu": "te",
                        "Tamil": "ta",
                        "Kannada": "kn"
                    }

                    result = model.transcribe(
                        temp_audio_path,
                        language=language_codes[language]
                    )

                # -----------------------------
                # Get Segments
                # -----------------------------
                segments = result.get("segments", [])

                segment_texts = []

                for segment in segments:

                    text = segment.get("text", "").strip()

                    if text:
                        segment_texts.append(text)

                # Create final transcription
                transcription = " ".join(segment_texts).strip()

                # -----------------------------
                # Audio Statistics
                # -----------------------------
                word_count = len(transcription.split())

                character_count = len(transcription)

                segment_count = len(segments)

                if segments:
                    duration = segments[-1]["end"]
                else:
                    duration = 0

                # -----------------------------
                # Success Message
                # -----------------------------
                st.success(
                    "✅ Transcription completed successfully!"
                )

                # -----------------------------
                # Audio Statistics
                # -----------------------------
                st.markdown(
                    '<div class="section-title">📊 Audio Statistics</div>',
                    unsafe_allow_html=True
                )

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "⏱️ Duration",
                        f"{duration:.2f} sec"
                    )

                with col2:
                    st.metric(
                        "🔤 Words",
                        word_count
                    )

                with col3:
                    st.metric(
                        "🔢 Characters",
                        character_count
                    )

                with col4:
                    st.metric(
                        "🧩 Segments",
                        segment_count
                    )

                # -----------------------------
                # Transcript
                # -----------------------------
                st.markdown(
                    '<div class="section-title">📝 Transcription</div>',
                    unsafe_allow_html=True
                )

                if transcription:

                    st.markdown(
                        f'<div class="transcript-box">{transcription}</div>',
                        unsafe_allow_html=True
                    )

                else:

                    st.warning(
                        "⚠️ No speech could be detected in this audio."
                    )

                # -----------------------------
                # Timestamps
                # -----------------------------
                st.markdown(
                    '<div class="section-title">⏱️ Timestamps</div>',
                    unsafe_allow_html=True
                )

                for segment in segments:

                    start = segment["start"]
                    end = segment["end"]
                    text = segment.get("text", "").strip()

                    if text:

                        st.markdown(
                            f"""
                            <div class="timestamp-box">
                                <strong>
                                    [{start:.2f}s - {end:.2f}s]
                                </strong>
                                {text}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                # -----------------------------
                # Downloads
                # -----------------------------
                if transcription:

                    # Download TXT
                    st.download_button(
                        label="⬇️ Download Transcript",
                        data=transcription,
                        file_name="transcription.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                    # -----------------------------
                    # Create SRT Subtitle File
                    # -----------------------------
                    def format_srt_time(seconds):

                        hours = int(seconds // 3600)

                        minutes = int(
                            (seconds % 3600) // 60
                        )

                        secs = int(seconds % 60)

                        milliseconds = int(
                            (seconds - int(seconds)) * 1000
                        )

                        return (
                            f"{hours:02d}:"
                            f"{minutes:02d}:"
                            f"{secs:02d},"
                            f"{milliseconds:03d}"
                        )

                    srt_content = ""

                    for index, segment in enumerate(
                        segments,
                        start=1
                    ):

                        start = format_srt_time(
                            segment["start"]
                        )

                        end = format_srt_time(
                            segment["end"]
                        )

                        text = segment.get(
                            "text",
                            ""
                        ).strip()

                        if text:

                            srt_content += (
                                f"{index}\n"
                            )

                            srt_content += (
                                f"{start} --> {end}\n"
                            )

                            srt_content += (
                                f"{text}\n\n"
                            )

                    # Download SRT
                    st.download_button(
                        label="🎬 Download Subtitles (SRT)",
                        data=srt_content,
                        file_name="transcription.srt",
                        mime="text/plain",
                        use_container_width=True
                    )

            finally:

                if os.path.exists(temp_audio_path):
                    os.remove(temp_audio_path)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")

st.markdown(
    "<center>Built with Python • Streamlit • OpenAI Whisper</center>",
    unsafe_allow_html=True
)