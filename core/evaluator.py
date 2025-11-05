# core/evaluator.py

from fuzzywuzzy import fuzz

def evaluate_answer(correct_answer: str, user_answer: str) -> int:
    """
    Evaluează răspunsul utilizatorului folosind fuzzy string matching.
    token_set_ratio este robust la ordinea cuvintelor și cuvinte extra.
    """
    
    # TODO: Logica poate fi rafinată și mai mult, de ex. pentru răspunsuri
    # care sunt liste (ca la n-queens) sau matrici (ca la Nash).
    
    # Eliminăm spațiile albe de la început/sfârșit și convertim la litere mici
    clean_correct = correct_answer.lower().strip()
    clean_user = user_answer.lower().strip()

    if not clean_user:
        return 0

    # Calculează un scor de similaritate între 0 și 100
    score = fuzz.token_set_ratio(clean_correct, clean_user)
    
    return score