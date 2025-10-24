from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load a small, fast embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def find_best_match(user_question, qa_list, threshold=0.75):
    """
    Find the most semantically similar question.
    Returns (best_answer, similarity_score) or (None, 0)
    """
    questions = [item["question"] for item in qa_list]
    question_embeddings = model.encode(questions)
    user_embedding = model.encode([user_question])

    sims = cosine_similarity(user_embedding, question_embeddings)[0]
    best_idx = np.argmax(sims)
    best_score = sims[best_idx]

    if best_score >= threshold:
        return qa_list[best_idx]["answer"], float(best_score)
    else:
        return None, float(best_score)
