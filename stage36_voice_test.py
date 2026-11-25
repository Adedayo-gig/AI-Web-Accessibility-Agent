import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import pyaudio
import json

MODEL_PATH = "vosk-model-small-en-us-0.15"

print("Loading Vosk model...")
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

audio = pyaudio.PyAudio()

microphone = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=8000
)

print("Speak now. Say: Hello, open the contact page.")

try:
    while True:
        data = microphone.read(4000, exception_on_overflow=False)

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")

            if text:
                print("You said:", text)
                break
finally:
    microphone.stop_stream()
    microphone.close()
    audio.terminate()