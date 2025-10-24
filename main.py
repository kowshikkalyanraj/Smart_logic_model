from flask import Flask, render_template, request, jsonify
from qa_loader import load_qa, find_best_match
from database import load_json, save_json
from gemini_api import get_gemini_answer
import os

app = Flask(__name__)

# File paths
qa_file = os.path.join("data", "kowshik_daily_activities_final.txt")
knowledge_db = os.path.join("data", "knowledge_db.json")
memory_db = os.path.join("data", "memory_db.json")

# Load data
qa_data = load_qa(qa_file)
knowledge = load_json(knowledge_db)
memory = load_json(memory_db)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.form["question"].strip()
    normalized_q = user_question.lower()

    # 1️⃣ Check in text data
    answer = find_best_match(normalized_q, qa_data)
    if answer:
        knowledge[user_question] = answer
        save_json(knowledge_db, knowledge)
        return jsonify({"source": "Text Data", "answer": answer})

    # 2️⃣ Check in memory
    if user_question in memory:
        return jsonify({"source": "Memory", "answer": memory[user_question]})

    # 3️⃣ Get from Gemini
    answer = get_gemini_answer(user_question)
    memory[user_question] = answer
    save_json(memory_db, memory)
    return jsonify({"source": "Gemini", "answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
