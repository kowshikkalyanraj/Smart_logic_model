import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load the API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash"

def get_gemini_answer(question):
    """
    Fetch answer from Gemini model.
    """
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=question,
            config=types.GenerateContentConfig(temperature=0)
        )
        return response.text.strip()
    except Exception as e:
        return f"Gemini API error: {e}"
