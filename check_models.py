import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if "GOOGLE_API_KEY" in os.environ:
    del os.environ["GOOGLE_API_KEY"]

client = genai.Client(api_key=api_key)

try:
    print("Checking available models...")
    for model in client.models.list():
        print(f"Model: {model}")
except Exception as e:
    print(f"Error: {e}")
