"""
Modul pentru evaluarea răspunsurilor utilizatorilor.
Suportă evaluare simplă și fuzzy matching pentru toleranță la greșeli.
"""
from typing import List, Dict
from difflib import SequenceMatcher


def normalize_text(text: str) -> str:
    """
    Normalizează textul pentru comparare.

    Args:
        text: Textul de normalizat

    Returns:
        Text normalizat (lowercase, fără spații extra)
    """
    return " ".join(text.lower().strip().split())


def calculate_similarity(str1: str, str2: str) -> float:
    """
    Calculează similaritatea între două stringuri (0.0 - 1.0).

    Args:
        str1: Primul string
        str2: Al doilea string

    Returns:
        Scor de similaritate (0 = diferit complet, 1 = identic)
    """
    return SequenceMatcher(None, str1, str2).ratio()


def evaluate_keywords(keywords: List[str], user_answer: str, threshold: float = 0.7) -> Dict:
    """
    Evaluează prezența keywords în răspunsul utilizatorului.

    Args:
        keywords: Lista de keywords esențiale
        user_answer: Răspunsul utilizatorului
        threshold: Pragul de similaritate pentru fuzzy matching

    Returns:
        Dict cu informații despre evaluare
    """
    normalized_answer = normalize_text(user_answer)
    found_keywords = []
    missing_keywords = []
    partial_matches = []

    for keyword in keywords:
        normalized_keyword = normalize_text(keyword)

        # Verifică match exact
        if normalized_keyword in normalized_answer:
            found_keywords.append(keyword)
            continue

        # Verifică fuzzy match pentru toleranță la greșeli de scriere
        best_similarity = 0.0
        words = normalized_answer.split()

        for word in words:
            similarity = calculate_similarity(normalized_keyword, word)
            if similarity > best_similarity:
                best_similarity = similarity

        # Pentru fraze multi-cuvânt, verifică și secvențe
        if " " in normalized_keyword:
            window_size = len(normalized_keyword.split())
            for i in range(len(words) - window_size + 1):
                phrase = " ".join(words[i:i + window_size])
                similarity = calculate_similarity(normalized_keyword, phrase)
                if similarity > best_similarity:
                    best_similarity = similarity

        if best_similarity >= threshold:
            found_keywords.append(keyword)
            partial_matches.append((keyword, best_similarity))
        else:
            missing_keywords.append(keyword)

    return {
        "found": found_keywords,
        "missing": missing_keywords,
        "partial": partial_matches
    }


def evaluate_answer(correct_answer: str, user_answer: str,
                    keywords: List[str] = None,
                    fuzzy: bool = True,
                    threshold: float = 0.8) -> Dict:
    """
    Evaluează răspunsul utilizatorului comparativ cu răspunsul corect.

    Args:
        correct_answer: Răspunsul corect complet
        user_answer: Răspunsul dat de utilizator
        keywords: Lista opțională de keywords pentru evaluare
        fuzzy: Dacă True, permite toleranță la greșeli mici
        threshold: Pragul de similaritate (0.0 - 1.0)

    Returns:
        Dict cu scor (0-100), feedback și detalii

    Example:
        >>> result = evaluate_answer(
        ...     "Backtracking cu Forward Checking",
        ...     "Backtraking with FC",
        ...     keywords=["backtracking", "forward checking", "fc"]
        ... )
        >>> print(result["score"])  # 85
    """
    if not user_answer or not user_answer.strip():
        return {
            "score": 0,
            "feedback": "Răspuns gol.",
            "details": {}
        }

    normalized_correct = normalize_text(correct_answer)
    normalized_user = normalize_text(user_answer)

    # Calculează similaritatea textuală generală
    overall_similarity = calculate_similarity(normalized_correct, normalized_user)

    # Dacă avem keywords, folosim evaluarea pe keywords
    if keywords:
        keyword_eval = evaluate_keywords(keywords, user_answer, threshold)

        # Calculează scorul pe baza keywords
        total_keywords = len(keywords)
        found_count = len(keyword_eval["found"])
        keyword_score = (found_count / total_keywords) * 100 if total_keywords > 0 else 0

        # Scorul final este media ponderată: 70% keywords, 30% similaritate text
        final_score = int(keyword_score * 0.7 + overall_similarity * 100 * 0.3)

        # Generează feedback
        feedback_parts = []
        if found_count == total_keywords:
            feedback_parts.append("Excelent! Toate conceptele cheie sunt prezente.")
        elif found_count >= total_keywords * 0.7:
            feedback_parts.append(f"Bine! {found_count}/{total_keywords} concepte cheie identificate.")
        elif found_count >= total_keywords * 0.4:
            feedback_parts.append(f"Parțial corect. {found_count}/{total_keywords} concepte cheie identificate.")
        else:
            feedback_parts.append(f"Insuficient. Doar {found_count}/{total_keywords} concepte cheie identificate.")

        if keyword_eval["missing"]:
            feedback_parts.append(f"Lipsesc: {', '.join(keyword_eval['missing'])}")

        if keyword_eval["partial"]:
            partial_info = [f"{kw} ({sim:.0%})" for kw, sim in keyword_eval["partial"]]
            feedback_parts.append(f"Potriviri parțiale: {', '.join(partial_info)}")

        return {
            "score": min(final_score, 100),
            "feedback": " ".join(feedback_parts),
            "details": {
                "keyword_score": keyword_score,
                "similarity_score": overall_similarity * 100,
                "found_keywords": keyword_eval["found"],
                "missing_keywords": keyword_eval["missing"],
                "partial_matches": keyword_eval["partial"]
            }
        }

    # Fallback: evaluare bazată doar pe similaritate textuală
    else:
        score = int(overall_similarity * 100)

        if score >= 90:
            feedback = "Excelent! Răspunsul este aproape identic cu răspunsul corect."
        elif score >= 70:
            feedback = "Bine! Răspunsul este similar cu răspunsul corect."
        elif score >= 50:
            feedback = "Parțial corect. Răspunsul conține unele elemente corecte."
        else:
            feedback = "Incorect. Răspunsul diferă semnificativ de răspunsul corect."

        return {
            "score": score,
            "feedback": feedback,
            "details": {
                "similarity_score": score
            }
        }


def evaluate_question(question_obj, user_answer: str, fuzzy: bool = True) -> Dict:
    """
    Evaluează răspunsul utilizând direct obiectul întrebării.
    Aceasta este metoda RECOMANDATĂ de utilizare!

    Args:
        question_obj: Instanță QuestionBase (ex: NQueensQuestion)
        user_answer: Răspunsul utilizatorului
        fuzzy: Dacă True, permite fuzzy matching

    Returns:
        Dict cu scor, feedback și răspunsul corect

    Example:
        >>> from core.question_factory import create_question
        >>> q = create_question("n-queens", "medium")
        >>> result = evaluate_question(q, "Backtracking cu FC")
        >>> print(f"Scor: {result['score']}%")
        >>> print(f"Răspuns corect: {result['correct_answer']}")
    """
    result = evaluate_answer(
        correct_answer=question_obj.correct_answer,
        user_answer=user_answer,
        keywords=question_obj.get_keywords(),
        fuzzy=fuzzy
    )

    # Adaugă răspunsul corect în rezultat
    result["correct_answer"] = question_obj.correct_answer
    result["detailed_answer"] = question_obj.generate_detailed_answer()

    return result