import requests
import json

def test_ollama():
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.2:3b",
        "prompt": "Say hello as JARVIS.",
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        print("Ollama Response:", result.get("response"))
    except Exception as e:
        print("Error connecting to Ollama:", e)

if __name__ == "__main__":
    test_ollama()
