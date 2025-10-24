import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not set. Check your .env file.")

genai.configure(api_key=API_KEY)

KNOWLEDGE_DB_PATH = "knowledge_db.json"
MEMORY_DB_PATH = "memory_db.json"

def load_db(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_db(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def search_knowledge_db(question):
    db = load_db(KNOWLEDGE_DB_PATH)
    return db.get(question.lower(), None)

def get_answer_from_gemini(question):
    try:
        # Use a model your API key has access to
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(question)
        return response.text.strip()
    except Exception as e:
        print("❌ Gemini API Error:", e)
        return "Sorry, I couldn't reach Gemini right now."

def process_question(question):
    """Check knowledge DB first, otherwise query Gemini."""
    question_clean = question.strip().lower()

    # 1. Check knowledge_db.json
    answer = search_knowledge_db(question_clean)
    if answer:
        print("✅ Found in knowledge_db.json")
        return answer

    # 2. Fetch from Gemini
    print("🤖 Fetching from Gemini...")
    answer = get_answer_from_gemini(question)

    # 3. Save to memory_db.json
    memory_db = load_db(MEMORY_DB_PATH)
    memory_db[question_clean] = answer
    save_db(MEMORY_DB_PATH, memory_db)
    print("💾 Saved to memory_db.json")

    return answer
