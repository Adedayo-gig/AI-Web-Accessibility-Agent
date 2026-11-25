
import pyttsx3

def speak(message):
    print("AGENT:", message)

    engine = pyttsx3.init()
    engine.setProperty("rate", 165)
    engine.say(message)
    engine.runAndWait()