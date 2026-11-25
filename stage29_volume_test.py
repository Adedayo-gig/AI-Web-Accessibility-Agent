import speech_recognition as sr
import audioop

recognizer = sr.Recognizer()

print("====================================")
print("MICROPHONE VOLUME TEST")
print("====================================")

with sr.Microphone(device_index=1) as source:

    print("\nSpeak normally for about 5 seconds...")
    
    audio = recognizer.listen(
        source,
        timeout=10,
        phrase_time_limit=8
    )

raw_audio = audio.get_raw_data()

volume = audioop.rms(
    raw_audio,
    audio.sample_width
)

print("\n===== RESULT =====")
print("Recorded audio volume:", volume)

if volume < 500:
    print("Volume is VERY LOW.")
elif volume < 1500:
    print("Volume is LOW.")
elif volume < 5000:
    print("Volume is NORMAL.")
else:
    print("Volume is HIGH.")