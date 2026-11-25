import speech_recognition as sr

recognizer = sr.Recognizer()

print("====================================")
print("AI WEB ACCESSIBILITY AGENT")
print("OFFLINE VOICE TEST")
print("====================================")

with sr.Microphone() as source:

    print("\nMicrophone is ready.")
    print("Say:")
    print("Find a black shoe, size 45, below 15 thousand.")

    audio = recognizer.listen(
        source,
        phrase_time_limit=8
    )

print("\nRecording completed.")
print("Processing speech OFFLINE...")

try:
    text = recognizer.recognize_sphinx(audio)

    print("\n===== VOICE RESULT =====")
    print(text)

except sr.UnknownValueError:
    print("\nPocketSphinx could not understand the speech.")

except Exception as error:
    print("\nERROR:")
    print(error) 