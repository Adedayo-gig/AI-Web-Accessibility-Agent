import sounddevice as sd
from scipy.io.wavfile import read

sample_rate, audio = read("microphone_test.wav")

print("Playing your recording now...")
sd.play(audio, sample_rate)
sd.wait()
print("Playback finished.")