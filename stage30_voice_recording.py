import speech_recognition as sr

recognizer = sr.Recognizer()

print("====================================")
print("SHORT VOICE TEST")
print("====================================")

with sr.Microphone() as source:

    print("\nMicrophone is ready.")
    print("Say only:")
    print("Hello")

    audio = recognizer.listen(
        source,
        timeout=10,
        phrase_time_limit=5
    )

print("\nRecording completed.")
print("Testing speech recognition...")

try:
    text = recognizer.recognize_google(audio)

    print("\n===== SUCCESS =====")
    print("Google heard:")
    print(text)

except sr.UnknownValueError:
    print("\n===== RESULT =====")
    print("Google received the audio but could not understand it.")

except sr.RequestError as error:
    print("\n===== SERVICE ERROR =====")
    print(error)