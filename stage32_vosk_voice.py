
import speech_recognition as sr
import wave

print("MICROPHONE RECORDING TEST")
print("=========================")

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Adjusting for background noise...")
    recognizer.adjust_for_ambient_noise(source, duration=2)

    print("Speak now: Hello, my name is Adedayo.")
    audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)

print("Recording finished.")
print("Audio bytes:", len(audio.frame_data))

with wave.open("microphone_test.wav", "wb") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(16000)
    wav.writeframes(
        audio.get_raw_data(convert_rate=16000, convert_width=2)
    )

print("Saved recording as microphone_test.wav")

