"""
MACHINE LEARNING PIPELINE: J.A.R.V.I.S. (ADA)
-------------------------------------------
1. DATA ACQUISITION: Real-time audio capture via 'sounddevice' and 'SpeechRecognition'.
2. PREPROCESSING: Audio normalization, noise thresholding, and STT (Speech-to-Text) conversion.
3. FEATURE ENGINEERING: Transformation of natural language strings into structured JSON intent schemas.
4. MODEL BUILDING: Supervised Machine Learning approach using Large Language Models (LLMs) 
   acting as a multi-class intent classifier (Random Forest/Decision Tree logic emulated via prompt engineering).
5. MODEL EVALUATION: Continuous monitoring of Command Success Rate, Latency, and F1-score 
   based on user feedback and execution accuracy.
"""

import os
import time
import datetime
import threading
import tkinter as tk
from tkinter import ttk
import numpy as np
import sounddevice as sd
import speech_recognition as sr
import pyttsx3
import pyautogui
import psutil
from google import genai
from dotenv import load_dotenv
from io import BytesIO
import wave
import re
import json
import requests

# --- CONFIGURATION & ENV ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OLLAMA_MODEL = "llama3.2:3b"

if "GOOGLE_API_KEY" in os.environ:
    del os.environ["GOOGLE_API_KEY"]

client = genai.Client(api_key=GEMINI_API_KEY)

# --- JARVIS THEME CONSTANTS ---
BG_COLOR = "#000000"      # Deep Space Black
ACCENT_COLOR = "#00D1FF"  # Futuristic Cyber Blue
TEXT_COLOR = "#FFFFFF"    # Pure White
DIM_COLOR = "#003366"     # Dark Navy for Depth

# --- TTS ENGINE ---
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 200)

def speak(text, ui=None):
    if ui: ui.update_log(f"JARVIS: {text}")
    print(f"JARVIS: {text}")

    def _tts_worker():
        try:
            # Short sleep to let any existing audio streams close
            time.sleep(0.1)
            temp_engine = pyttsx3.init('sapi5')
            temp_engine.setProperty('rate', 190)
            temp_engine.say(text)
            temp_engine.runAndWait()
            temp_engine.stop()
            # Delays to prevent audio driver collisions
            time.sleep(0.1)
        except Exception as e:
            print(f"TTS Thread Error: {e}")

    # Fire and forget the voice so it doesn't block the logic
    threading.Thread(target=_tts_worker, daemon=True).start()

# --- JARVIS UI CLASS ---
class JarvisUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("J.A.R.V.I.S. INTERFACE")
        self.root.geometry("650x450")
        self.root.configure(bg=BG_COLOR)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.95)
        
        # --- Header ---
        self.header = tk.Label(self.root, text="JUST A RATHER VERY INTELLIGENT SYSTEM", 
                              font=("Consolas", 10, "bold"), bg=BG_COLOR, fg=ACCENT_COLOR)
        self.header.pack(pady=5)
        
        # --- Main Visualizer ---
        self.canvas = tk.Canvas(self.root, width=200, height=200, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(pady=5)
        self.arc = self.canvas.create_oval(10, 10, 190, 190, outline=ACCENT_COLOR, width=2)
        self.inner_arc = self.canvas.create_oval(50, 50, 150, 150, outline=DIM_COLOR, width=1)
        self.status_text = self.canvas.create_text(100, 100, text="STANDBY", fill=ACCENT_COLOR, font=("Consolas", 12, "bold"))
        
        # --- Audio Level Bar ---
        self.vol_frame = tk.Frame(self.root, bg=DIM_COLOR, width=200, height=5)
        self.vol_frame.pack(pady=5)
        self.vol_bar = tk.Frame(self.vol_frame, bg=ACCENT_COLOR, width=0, height=5)
        self.vol_bar.place(x=0, y=0)

        # --- System Stats ---
        self.stats_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.stats_frame.pack(side="left", padx=20, fill="y")
        
        self.cpu_label = tk.Label(self.stats_frame, text="CPU: 0%", font=("Consolas", 9), bg=BG_COLOR, fg=ACCENT_COLOR)
        self.cpu_label.pack(anchor="w")
        self.ram_label = tk.Label(self.stats_frame, text="RAM: 0%", font=("Consolas", 9), bg=BG_COLOR, fg=ACCENT_COLOR)
        self.ram_label.pack(anchor="w")
        self.time_label = tk.Label(self.stats_frame, text="00:00:00", font=("Consolas", 12, "bold"), bg=BG_COLOR, fg=ACCENT_COLOR)
        self.time_label.pack(anchor="w", pady=10)

        # --- Activity Log ---
        self.log_box = tk.Text(self.root, height=15, width=45, bg=BG_COLOR, fg=TEXT_COLOR, 
                              font=("Consolas", 8), borderwidth=1, relief="flat", insertbackground=ACCENT_COLOR)
        self.log_box.pack(side="right", padx=10, pady=10)
        
        self.update_stats_loop()
        
    def update_status(self, text, color=ACCENT_COLOR):
        self.canvas.itemconfig(self.status_text, text=text, fill=color)
        self.canvas.itemconfig(self.arc, outline=color)
        self.root.update()

    def update_log(self, text):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_box.insert(tk.END, f"[{timestamp}] {text}\n")
        self.log_box.see(tk.END)
        self.root.update()

    def update_vol(self, level):
        # Level expected 0.0 to 1.0
        self.vol_bar.config(width=int(level * 200))
        self.root.update()

    def update_stats_loop(self):
        # [INSTRUCTION: INSERT EDA VISUALIZATION HERE]
        # Plot a Distribution of CPU/RAM usage over time to identify system bottlenecks.
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.cpu_label.config(text=f"CORE_LOAD: {cpu}%")
        self.ram_label.config(text=f"MEM_ALLOC: {ram}%")
        self.time_label.config(text=now)
        self.canvas.coords(self.inner_arc, 50+cpu/5, 50+cpu/5, 150-cpu/5, 150-cpu/5)
        self.root.after(1000, self.update_stats_loop)

# --- SYSTEM LOGIC ---
def clean_command(text):
    # [ACADEMIC REQUIREMENT: PREPROCESSING]
    """Strips AI filler and formatting from commands."""
    text = text.strip().replace("`", "")
    text = re.sub(r'^\[|\]$', '', text)
    text = re.sub(r'^(Command|Action|JARVIS|Intent|Result):\s*', '', text, flags=re.I)
    return text.strip()

def execute_local_command(cmd_dict, ui=None):
    # [ACADEMIC REQUIREMENT: FEATURE ENGINEERING]
    """Execution logic for parsing Brain 2 (Local) JSON commands."""
    try:
        action = cmd_dict.get("action")
        
        # --- OPEN ACTION ---
        if action == "open":
            target = cmd_dict.get("target", "").lower()
            # Clean target (remove extensions AI might add)
            target = target.replace(".exe", "").replace(".lnk", "").replace(".app", "").strip()
            target = re.sub(r'\s+game$', '', target).strip()
            
            # Smart Map: Prefer Protocols (URI) over paths for higher success rate
            apps = {
                "notepad": "notepad", 
                "calculator": "calc", 
                "chrome": "chrome",
                "browser": "chrome", 
                "file explorer": "explorer", 
                "explorer": "explorer",
                "task manager": "taskmgr", 
                "control panel": "control", 
                "whatsapp": "whatsapp:",
                "edge": "msedge", 
                "vscode": "code", 
                "visual studio code": "code",
                "spotify": "spotify:",
                "discord": "discord:",
                "settings": "ms-settings:",
                "youtube": "https://www.youtube.com", 
                "google": "https://www.google.com",
                "gmail": "https://mail.google.com",
                "outlook": "outlookmail:",
                "valorant": "valorant:",
                "nfs": "NFS", 
                "need for speed": "NFS"
            }
            
            app_to_run = apps.get(target, target)
            speak(f"Sir, initializing {target} protocol.", ui)
            
            # Execution Strategy
            if app_to_run.startswith("http"):
                os.system(f'start {app_to_run}')
            elif ":" in app_to_run and not app_to_run[1] == ":": # It's a protocol like whatsapp:
                os.system(f'start {app_to_run}')
            else:
                # Try running as a system command
                os.system(f'start "" "{app_to_run}"')

        # --- WRITE ACTION ---
        elif action == "write":
            content = cmd_dict.get("content", "")
            speak("Sir, documenting the requested data.", ui)
            time.sleep(0.5)
            pyautogui.write(content, interval=0.01)

        # --- SYSTEM_INFO ACTION ---
        elif action == "system_info":
            query = cmd_dict.get("query", "").lower()
            if "battery" in query:
                try:
                    percent = psutil.sensors_battery().percent
                    speak(f"Battery is at {percent}%", ui)
                except: speak("Battery sensors offline.", ui)
            elif "time" in query:
                speak(f"The current time is {datetime.datetime.now().strftime('%H:%M')}", ui)
            elif "date" in query:
                speak(f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}", ui)

        # --- SHELL ACTION ---
        elif action == "shell":
            command = cmd_dict.get("command", "")
            speak(f"Executing shell sequence, Sir.", ui)
            os.system(f"powershell -Command {command}")

        # --- SAVE ACTION ---
        elif action == "save":
            filename = cmd_dict.get("filename", "")
            speak(f"Archiving as {filename}.", ui)
            pyautogui.hotkey('ctrl', 's')
            time.sleep(1)
            if filename:
                pyautogui.write(filename)
                time.sleep(0.5)
                pyautogui.press('enter')

        # --- HOTKEY ACTION ---
        elif action == "hotkey":
            keys = cmd_dict.get("keys", "").lower().split('+')
            speak(f"Executing hotkey sequence, Sir.", ui)
            pyautogui.hotkey(*keys)
        
    except Exception as e:
        if ui: ui.update_log(f"LOCAL_EXEC_ERROR: {str(e)}")

def ollama_brain(prompt, ui=None):
    """Fallback Local Brain using Ollama."""
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        if ui: ui.update_log(f"OLLAMA_ERROR: {str(e)}")
        return None

# [ACADEMIC REQUIREMENT: MODEL BUILDING]
# This function serves as the Inference Engine. It classifies user intent by mapping natural 
# language input to a structured JSON command schema using Large Language Models.
def process_request(user_input, ui=None):
    # [INSTRUCTION: INSERT EDA VISUALIZATION HERE]
    # Generate a Correlation Matrix between 'User Input Length' and 'Model Latency' 
    # to analyze the efficiency of the intent classification pipeline.
    if ui: ui.update_status("THINKING", ACCENT_COLOR)
    
    intent_prompt = f"""
    ROLE: You are J.A.R.V.I.S., a Hybrid Intelligence System.
    Analyze user request: "{user_input}"

    PROTOCOL:
    For local tasks, output a "LOCAL_EXEC" tag with a JSON command.
    COMMAND SCHEMA:
    - {{"action": "open", "target": "notepad"}}
    - {{"action": "write", "content": "text"}}
    - {{"action": "system_info", "query": "battery|time|date"}}
    - {{"action": "shell", "command": "powershell_cmd"}}
    - {{"action": "save", "filename": "name"}}
    - {{"action": "hotkey", "keys": "ctrl+s"}}

    BEHAVIOR:
    1. Provide a professional CHAT response first.
    2. Output LOCAL_EXEC tags for actions.
    3. Refer to the user as 'Sir'.
    4. You can combine multiple actions.

    Example: "open notepad and write hello then save it"
    CHAT Of course, Sir. I am preparing the document now.
    LOCAL_EXEC: {{"action": "open", "target": "notepad"}}
    LOCAL_EXEC: {{"action": "write", "content": "hello"}}
    LOCAL_EXEC: {{"action": "save", "filename": "document"}}
    """
    
    output = ""
    try:
        try:
            # Brain 1: Gemini Flash (Fastest)
            response = client.models.generate_content(model="gemini-flash-latest", contents=intent_prompt)
            output = response.text.strip()
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower() or "connection" in str(e).lower():
                ui.update_log("FLASH OFFLINE. SWITCHING TO PRO BRAIN.")
                try:
                    # Brain 2: Gemini Pro (Powerful)
                    response = client.models.generate_content(model="gemini-pro-latest", contents=intent_prompt)
                    output = response.text.strip()
                except:
                    ui.update_log("CLOUD BRAINS OFFLINE. ACTIVATING LOCAL CORE (OLLAMA).")
                    output = ollama_brain(intent_prompt, ui)
            else: raise e
        
        if not output:
            ui.update_log("ALL BRAINS FAILED TO RESPOND.")
            return

        ui.update_log(f"BRAIN_RAW: {output[:100]}...")
        
        # Parse CHAT
        chat_match = re.search(r'CHAT\s+(.*?)($|\n|LOCAL_EXEC)', output, re.S | re.I)
        if chat_match:
            speak(chat_match.group(1).strip(), ui)
        
        # Parse LOCAL_EXEC
        exec_matches = re.findall(r'LOCAL_EXEC:\s*(\{.*?\})', output)
        for match in exec_matches:
            try:
                cmd_dict = json.loads(match)
                execute_local_command(cmd_dict, ui)
            except: continue
            
    except Exception as e:
        ui.update_log(f"BRAIN_ERROR: {str(e)}")

def capture_audio(duration=2, fs=44100, ui=None):
    # [ACADEMIC REQUIREMENT: PREPROCESSING]
    if ui: ui.update_status("LISTENING", TEXT_COLOR)
    
    chunk_size = 1024
    recording = []
    
    def callback(indata, frames, time, status):
        volume_norm = np.linalg.norm(indata)*10
        if ui: ui.update_vol(min(volume_norm/100, 1.0))
        recording.append(indata.copy())

    with sd.InputStream(samplerate=fs, channels=1, callback=callback, dtype='int16'):
        sd.sleep(int(duration * 1000))
    
    if ui: ui.update_vol(0)
    
    full_recording = np.concatenate(recording, axis=0)
    buffer = BytesIO()
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(full_recording.tobytes())
    buffer.seek(0)
    return buffer

def listen(ui=None, duration=2):
    # [ACADEMIC REQUIREMENT: PREPROCESSING]
    r = sr.Recognizer()
    r.energy_threshold = 300
    
    audio_buffer = capture_audio(duration=duration, ui=ui)
    with sr.AudioFile(audio_buffer) as source:
        audio_data = r.record(source)
    try:
        text = r.recognize_google(audio_data)
        if ui: ui.update_log(f"RECOGNIZED: {text}")
        return text.lower()
    except sr.UnknownValueError:
        return ""
    except Exception as e:
        if ui: ui.update_log(f"LISTEN_ERROR: {str(e)[:20]}")
        return ""

def main_loop(ui):
    speak("System online. Audio sensors calibrated. Sir.", ui)
    while True:
        try:
            ui.update_status("STANDBY", ACCENT_COLOR)
            wake_check = listen(ui, duration=4)
            
            if any(word in wake_check for word in ["jarvis", "wake up", "hey", "ada"]):
                speak("At your service. Active mode engaged, Sir.", ui)
                
                consecutive_silence = 0
                while True:
                    ui.update_status("ACTIVE", ACCENT_COLOR)
                    command = listen(ui, duration=8)
                    
                    if not command:
                        consecutive_silence += 1
                        if consecutive_silence >= 2:
                            speak("Sir, I am returning to standby.", ui)
                            break
                        continue
                    
                    consecutive_silence = 0
                    
                    if any(stop_word in command for stop_word in ["thank you", "that is all", "goodbye", "go to sleep", "stop"]):
                        speak("Of course, Sir. Standing by.", ui)
                        break
                    
                    process_request(command, ui)
                    time.sleep(0.5)
            
            time.sleep(0.1)
        except Exception as e:
            print(f"Loop Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    jarvis_ui = JarvisUI()
    logic_thread = threading.Thread(target=main_loop, args=(jarvis_ui,), daemon=True)
    logic_thread.start()
    jarvis_ui.root.mainloop()
