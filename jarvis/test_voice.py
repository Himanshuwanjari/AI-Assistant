from src.voice import VoiceInput, VoiceInputError

v = VoiceInput()
print("Speak now...")
try:
    text = v.listen()
    print(f"✓ Transcribed: {text}")
except VoiceInputError as e:
    print(f"✗ {e}")