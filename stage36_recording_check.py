import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

duration = 5
sample_rate = 44100
device = 9

print("Speak clearly for 5 seconds...")

recording = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=2,
    dtype="int16",
    device=device
)

sd.wait()

write("microphone_test.wav", sample_rate, recording)

peak = np.max(np.abs(recording))
average = np.sqrt(np.mean(recording.astype(float) ** 2))

print("Recording saved.")
print("Peak audio level:", peak)
print("Average audio level:", round(average, 2))