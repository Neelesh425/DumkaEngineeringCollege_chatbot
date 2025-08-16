import sounddevice as sd
import soundfile as sf

def record_audio(filename="output.wav", duration=5, samplerate=44100):
    print("🎙️ Recording will begin...")
    try:
        audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
        print("⏺️ Recording in progress...")
        sd.wait()
        sf.write(filename, audio, samplerate)
        print(f"✅ Recording saved as {filename}")
    except Exception as e:
        print("❌ Error during recording:", e)

if __name__ == "__main__":
    record_audio()
