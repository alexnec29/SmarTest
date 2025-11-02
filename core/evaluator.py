# TODO: Evaluate user answers against the correct answer

def evaluate_answer(correct_answer: str, user_answer: str) -> int:
    """
    Evaluează răspunsul utilizatorului ca procent (0-100%)
    TODO: Înlocuiți logica simplă cu keyword matching sau fuzzy matching
    """
    keywords = correct_answer.lower().split()
    score = 0
    for kw in keywords:
        if kw in user_answer.lower():
            score += 100 / len(keywords)
    return min(int(score), 100)
