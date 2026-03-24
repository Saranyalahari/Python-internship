import pyttsx3

# Initialize engine globally
engine = pyttsx3.init()

def speak_text(text, rate=150, volume=1.0):
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

    engine.say(text)
    engine.runAndWait()

def stop_speech():
    engine.stop()


# MP3 conversion (gTTS)
from gtts import gTTS
import os

def save_audio(text, filename="audio_output/output.mp3"):
    os.makedirs("audio_output", exist_ok=True)

    tts = gTTS(text)
    tts.save(filename)

    return filename