
# Automatic Speech Recognition

This project is an Automatic Speech Recognition (ASR) application built using Python, Streamlit, and OpenAI Whisper.

The application allows users to upload an audio file and convert the speech into text. It also shows timestamps and provides options to download the transcription and subtitles.

## Features

* Upload audio files
* Convert speech into text
* Supports English, Hindi, Telugu, Tamil and Kannada
* Automatic language detection
* Shows audio duration and word count
* Displays timestamps for each speech segment
* Download transcription as TXT
* Download subtitles as SRT

## Technologies Used

* Python
* Streamlit
* OpenAI Whisper
* PyTorch
* FFmpeg

## Project Structure

```text
automatic-speech-recognition/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── Recording.m4a.m4a
```

## How to Run

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

The application will open in the browser at:

```text
http://localhost:8501
```

## How It Works

1. Upload an audio file.
2. Select a language or use Auto Detect.
3. Click the Transcribe Audio button.
4. Whisper processes the audio.
5. The generated text and timestamps are displayed.
6. Download the transcript or SRT subtitles.

## Author

Nanda Kumar
