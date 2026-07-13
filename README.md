# J.A.R.V.I.S. (ADA) - Voice-Controlled AI Assistant

> **JUST A RATHER VERY INTELLIGENT SYSTEM** – An advanced voice-controlled AI assistant with desktop automation, powered by Google Gemini and local Ollama fallback.

![Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🎯 Overview

J.A.R.V.I.S. is a sophisticated voice-activated AI system that combines cloud-based intelligence with local privacy. It listens to your commands, processes them through advanced language models, and executes actions—from simple queries to complex desktop automation tasks.

### Key Capabilities
- **Voice-Based Interaction**: Speak naturally; the system converts your speech to actionable commands
- **Dual Intelligence Architecture**: Cloud (Gemini) for power, local Ollama for privacy
- **Desktop Automation**: Open apps, type text, save files, execute shell commands
- **System Monitoring**: Real-time CPU, RAM, and battery status
- **Beautiful UI**: Cyber-themed Tkinter interface with real-time audio visualization
- **Multi-threaded**: Smooth GUI responsiveness while processing commands

## 🚀 Features

### Machine Learning Pipeline
The system implements a complete ML pipeline:

1. **Data Acquisition** - Real-time audio capture via `sounddevice` and `SpeechRecognition`
2. **Preprocessing** - Audio normalization and noise thresholding with STT conversion
3. **Feature Engineering** - Natural language transformation into structured JSON intent schemas
4. **Model Building** - Supervised ML using LLMs as multi-class intent classifiers via prompt engineering
5. **Model Evaluation** - Continuous monitoring of Command Success Rate, Latency, and F1-score

### Core Features
- 🎤 Speech-to-Text recognition
- 🔊 Text-to-Speech voice output
- 🌐 Google Gemini integration (cloud-based)
- 🏠 Ollama local fallback (offline-capable, privacy-first)
- ⚙️ System command execution (PowerShell, app launching)
- 📝 File operations (create, write, save)
- 📊 Real-time system metrics (CPU, RAM, battery)
- 🎨 Cyber-themed GUI with audio level visualization

## 📋 Requirements

### System Requirements
- Windows OS (with audio input device)
- Python 3.8 or higher
- Active internet connection (for cloud mode)
- Ollama installed (optional, for offline/local mode)

### Python Dependencies

```txt
google-generativeai      # Google Gemini API client
SpeechRecognition       # Voice-to-text conversion
pyttsx3                 # Text-to-speech engine
pyautogui              # Desktop automation
psutil                 # System monitoring
python-dotenv          # Environment variable management
PyAudio               # Audio processing
sounddevice           # Real-time audio capture
numpy                 # Numerical operations
tkinter               # GUI framework (usually pre-installed)
requests              # HTTP requests (for Ollama)
```

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ada_v2.git
cd ada_v2-main
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the `ada_v2-main` directory:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

**Getting Your Gemini API Key:**
- Visit [Google AI Studio](https://aistudio.google.com/)
- Sign in with your Google account
- Create a new API key
- Copy and paste it into your `.env` file

### 5. (Optional) Install Ollama
For local/offline operation:
- Download [Ollama](https://ollama.ai/)
- Run: `ollama pull llama3.2:3b`

## 🚀 Quick Start

### Run the Main Application
```bash
python ada.py
```

The J.A.R.V.I.S. interface will launch with:
- Status display and audio visualization
- Continuous listening mode
- Voice command processing

### Test Components

#### Test Audio Input
```bash
python mic_tester.py
```

#### Test Speech Recognition
```bash
python test_voice.py
```

#### Test AI Models
```bash
python test_genai.py
```

#### Verify All Libraries
```bash
python test_libs.py
```

#### Check System Models
```bash
python check_models.py
```

#### Verify Ollama Status
```bash
python check_ollama.py
```

## 🎤 Usage

### Activation
1. Start the application: `python ada.py`
2. Speak the wake word: **"Jarvis"**
3. Provide your command

### Example Commands

**Information Queries**
- "What's the current time?"
- "Check my CPU and RAM usage"
- "Give me the weather"

**Desktop Automation**
- "Open Notepad"
- "Type 'Hello World'"
- "Save the file"
- "Execute a PowerShell command"

**Chat Interactions**
- "Tell me a joke"
- "Explain quantum computing"
- "What can you do?"

### Stop Listening
- Say: **"Stop"** or **"Exit"**
- Wait for timeout (configurable in settings)

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│         AUDIO INPUT (Microphone)                    │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │  Speech-to-Text     │
        │  (SpeechRecognition)│
        └─────────┬───────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │   JSON Intent       │
        │   Parsing Engine    │
        └─────────┬───────────┘
                  │
         ┌────────┴────────┐
         │                 │
         ▼                 ▼
    ┌─────────┐        ┌──────────┐
    │ Cloud   │        │  Local   │
    │ Gemini  │        │ Ollama   │
    └────┬────┘        └────┬─────┘
         │                  │
         └────────┬─────────┘
                  │
         ┌────────▼────────────┐
         │  Execution Engine   │
         │  - Open Apps        │
         │  - Type Text        │
         │  - Execute Commands │
         │  - Query System     │
         └────────┬────────────┘
                  │
                  ▼
        ┌──────────────────────┐
        │   Text-to-Speech     │
        │   (pyttsx3)          │
        └────────┬─────────────┘
                 │
                 ▼
        ┌──────────────────────┐
        │   Audio Output       │
        │   (Speaker)          │
        └──────────────────────┘
```

## 📊 Triple-Layer Hybrid Intelligence

### Primary Brain: Gemini Flash
- Cloud-based, ultra-fast responses
- Low latency for real-time interaction
- Advanced reasoning and knowledge

### Secondary Brain: Gemini Pro
- Cloud-based fallback
- Superior reasoning for complex queries
- Higher accuracy on specialized tasks

### Local Core: Ollama (llama3.2:3b)
- Completely offline execution
- Perfect privacy for sensitive commands
- Fast local response times
- No API keys or internet required

## 🎨 UI Features

- **Cyber-Themed Design**: Dark background with futuristic cyan accents
- **Real-Time Audio Visualization**: Animated rings showing activity status
- **Status Indicator**: Displays current system state (STANDBY, LISTENING, PROCESSING)
- **Event Log**: Rolling display of recent interactions
- **System Tray Integration**: Quick access and always-on-top window

## 📁 Project Structure

```
ada_v2-main/
├── ada.py                              # Main application entry point
├── ada_explanation.txt                 # Detailed system explanation
├── requirements.txt                    # Python dependencies
├── .env                               # Environment variables (API keys)
├── README.md                          # This file
│
├── SYSTEM_MANIFEST.md                 # Complete system architecture
├── Jarvis_ADA_Technical_Specification.txt  # Technical documentation
│
├── test_voice.py                      # Voice recognition tests
├── test_genai.py                      # AI model tests
├── test_libs.py                       # Library verification
├── check_models.py                    # Model availability checks
├── check_ollama.py                    # Ollama status verification
├── check_audio.py                     # Audio system diagnostics
└── mic_tester.py                      # Microphone configuration test
```

## 🔧 Configuration

### Adjustable Parameters (in `ada.py`)

```python
# TTS Engine Speed
engine.setProperty('rate', 200)  # Adjust speaking speed (100-300)

# Audio Sensitivity
NOISE_THRESHOLD = 0.02           # Adjust for ambient noise levels

# Session Duration
SESSION_TIMEOUT = 30             # Seconds before auto-exit
```

### Model Selection

The system automatically tries models in this order:
1. Gemini Flash (Primary)
2. Gemini Pro (Fallback)
3. Ollama Local (Offline)

## 📊 Performance Metrics

- **Voice Processing Latency**: ~100-300ms (cloud), ~50-150ms (local)
- **Command Execution**: 10-500ms depending on complexity
- **TTS Speed**: ~100-300ms per sentence
- **Memory Usage**: ~150-300MB (typical operation)

## 🛡️ Privacy & Security

- **Local Execution**: Desktop automation happens locally without cloud transmission
- **Environment Variables**: API keys stored in `.env` (never in code)
- **Offline Capable**: Works completely offline with Ollama
- **No Data Logging**: Conversations are not stored or analyzed
- **Thread-Safe**: Multi-threaded design prevents data races

## 🐛 Troubleshooting

### Audio Not Working
```bash
python check_audio.py
python mic_tester.py
```

### API Key Issues
- Verify `.env` file exists with correct key
- Ensure no extra whitespace around the key
- Test with `python test_genai.py`

### Speech Recognition Fails
- Check microphone connection
- Run `python mic_tester.py`
- Ensure no background noise interference

### Ollama Connection Issues
- Verify Ollama is running: `ollama serve`
- Check model is installed: `ollama list`
- Test with `python check_ollama.py`

## 📈 Future Enhancements

- [ ] Custom voice profiles and training
- [ ] Multi-language support
- [ ] Integration with smart home devices
- [ ] Advanced analytics dashboard
- [ ] Custom command macro recording
- [ ] Natural language fine-tuning
- [ ] Sentiment analysis and emotional responses

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation

## 🌟 Acknowledgments

Built with:
- [Google Generative AI](https://ai.google.dev/)
- [Ollama](https://ollama.ai/)
- [Python Speech Recognition](https://pypi.org/project/SpeechRecognition/)
- [pyttsx3](https://pypi.org/project/pyttsx3/)

---

**Ready to talk to JARVIS? Run `python ada.py` and say "Jarvis"!** 🎤
#
<img width="1311" height="598" alt="image" src="https://github.com/user-attachments/assets/56be3ae9-b3cb-47bd-bc81-f2374ad9c6ce" />

