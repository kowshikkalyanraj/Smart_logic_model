from flask import Flask, render_template, request, jsonify
from slm_core import process_question

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    if not question:
        return jsonify({'answer': 'No question received.'})

    # This is the key integration
    answer = process_question(question)

    return jsonify({'answer': answer})
