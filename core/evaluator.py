# core/evaluator.py

from fuzzywuzzy import fuzz
from unidecode import unidecode  # <-- Importă biblioteca

def evaluate_answer(correct_answer: str, user_answer: str) -> int:
    """
    Evaluează răspunsul utilizatorului folosind fuzzy string matching.
    Include normalizarea diacriticelor pentru robustețe.
    """
    
    if not user_answer:
        return 0

    # 1. Normalizează (elimină diacriticele) și convertește la litere mici
    clean_correct = unidecode(correct_answer.lower().strip())
    clean_user = unidecode(user_answer.lower().strip())
    
    # Acum "stânga" devine "stanga" în ambele șiruri

    # 2. Calculează un scor de similaritate între 0 și 100
    score = fuzz.token_set_ratio(clean_correct, clean_user)
    
    return score