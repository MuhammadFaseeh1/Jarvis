import sounddevice as sd
import numpy as np
import time

def test_mics():
    print("--- JARVIS SENSOR DIAGNOSTICS ---")
    print("Please speak loudly or clap while this runs...")
    devices = sd.query_devices()
    input_devices = [i for i, d in enumerate(devices) if d['max_input_channels'] > 0]
    
    for _ in range(5): # 5 rounds of testing
        for i in input_devices:
            try:
                duration = 0.5  # 0.5 seconds per device
                recording = sd.rec(int(duration * 44100), samplerate=44100, channels=1, device=i, dtype='float32')
                sd.wait()
                volume = np.linalg.norm(recording) * 10
                if volume > 0.1: # Threshold for "hearing something"
                    print(f"[ACTIVE] Device {i} ({devices[i]['name']}): Volume Level {volume:.2f}")
            except:
                pass
        time.sleep(0.5)
    print("--- DIAGNOSTICS COMPLETE ---")

if __name__ == "__main__":
    test_mics()
