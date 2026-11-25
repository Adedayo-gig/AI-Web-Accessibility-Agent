import speech_recognition as sr

recognizer = sr.Recognizer()

print("====================================")
print("VOICE RECOGNITION TEST")
print("====================================")

with sr.Microphone(device_index=1) as source:

    print("\nMicrophone is ready.")
    print("Please say this clearly:")
    print("Find a black shoe, size 45, below 15 thousand.")

    audio = recognizer.listen(
        source,
        timeout=10,
        phrase_time_limit=8
    )

print("\nRecording completed.")
print("Sending audio for recognition...")

try:
    text = recognizer.recognize_google(audio)

    print("\n===== SUCCESS =====")
    print("You said:")
    print(text)

except sr.UnknownValueError:
    print("\n===== RESULT =====")
    print("Audio was captured, but Google could not understand the speech.")

except sr.RequestError as error:
    print("\n===== INTERNET/SERVICE ERROR =====")
    print(error)