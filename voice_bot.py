from livekit import Room
import pyttsx3
from main import get_bot_response
import sounddevice as sd
from scipy.io.wavfile import write
from openai import OpenAI
import numpy as np
import json
import time
url = "ws://localhost:7883"
api_key = "devkey"
api_secret = "secret"
room = Room(url=url, api_key=api_key, api_secret=api_secret)
room.connect("test_room")
client = OpenAI(api_key="YOUR_API_KEY")
def record_audio(filename="input.wav", fs=16000, silence_limit=1.5, threshold=0.01):
    print("Listening... (Speak now)")
    chunk_size = int(0.1 * fs)
    frames = []
    silent_chunks = 0
    max_silent_chunks = int(silence_limit / 0.1)
    has_started_speaking = False
    with sd.InputStream(samplerate=fs, channels=1, dtype='float32') as stream:
        while True:
            chunk, overflowed = stream.read(chunk_size)
            if has_started_speaking:
                frames.append(chunk)
            rms = np.sqrt(np.mean(chunk**2))
            if not has_started_speaking:
                if rms > threshold:
                    print("Recording started...")
                    has_started_speaking = True
                continue 
            if rms < threshold:
                silent_chunks += 1
            else:
                silent_chunks = 0
            if silent_chunks > max_silent_chunks:
                print("Silence detected. Stopping.")
                break
    audio_data = np.concatenate(frames, axis=0)
    audio_int16 = (audio_data * 32767).astype(np.int16)
    write(filename, fs, audio_int16)

def speech_to_text():
    try:
        record_audio()
        with open("input.wav", "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-transcribe",
                file=f
            )

        return transcript.text
    except Exception as e:
        print(f"Error during transcription: {e}")
        return ""
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()
while True:
    user_input = speech_to_text()
    print("You said:", user_input)
    if user_input.lower() in ["exit", "quit"]:
        break
    response = get_bot_response(user_input)
    print("Bot:", response)
    speak(response)