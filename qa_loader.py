from difflib import SequenceMatcher

def load_qa(file_path):
    """Load question-answer pairs from a text file."""
    qa_dict = {}
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if "|||" in line:
                question, answer = line.split("|||")
                qa_dict[question.strip().lower()] = answer.strip()
    return qa_dict


def find_best_match(user_question, qa_dict, threshold=0.7):
    """
    Finds the best-matching question using fuzzy similarity.
    Returns the answer if a match is above the threshold.
    """
    user_question = user_question.lower()
    best_match = None
    best_score = 0

    for question in qa_dict.keys():
        score = SequenceMatcher(None, user_question, question).ratio()
        if score > best_score:
            best_score = score
            best_match = question

    if best_score >= threshold:
        return qa_dict[best_match]
    return None
