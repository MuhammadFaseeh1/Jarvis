import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

try:
    response = client.models.generate_content(
        model="gemini-flash-latest", 
        contents="Say 'Hello, I am online.'"
    )
    print(f"RESPONSE: {response.text}")
except Exception as e:
    print(f"ERROR: {e}")
