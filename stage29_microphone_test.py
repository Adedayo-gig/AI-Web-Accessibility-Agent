import speech_recognition as sr

recognizer = sr.Recognizer()

print("====================================")
print("AUDIO RECORDING TEST")
print("====================================")

with sr.Microphone(device_index=1) as source:

    print("\nMicrophone is ready.")
    print("Speak clearly for about 5 seconds...")

    audio = recognizer.listen(
        source,
        timeout=10,
        phrase_time_limit=8
    )

print("\nRecording completed.")

# Save the recorded audio
with open("voice_test.wav", "wb") as file:
    file.write(audio.get_wav_data())

print("Audio saved successfully.")
print("File: voice_test.wav")