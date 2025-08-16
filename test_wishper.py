import whisper

print("🟡 Starting Whisper Test...")

model = whisper.load_model("base")
result = model.transcribe("output.wav")

print("📜 Transcription:")
print(result["text"])
