import pyttsx3
try:
    print("Initializing TTS engine...")
    engine = pyttsx3.init()
    print("Speaking...")
    engine.say("Hello Sir, this is a test of the voice system.")
    engine.runAndWait()
    print("Test complete.")
except Exception as e:
    print(f"Error: {e}")
