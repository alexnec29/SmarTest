# core/evaluator.py

from fuzzywuzzy import fuzz
from unidecode import unidecode
import re
from typing import List, Optional


def extract_structured_data(text: str) -> str:
    """
    Extrage structuri de date precum liste [...] sau tupluri (...)
    Vital pentru N-Queens (liste) și Nash Equilibrium (tupluri).
    Prioritizes longer/more complete structures.
    """
    # Caută formatul [...] sau (...) - find all matches
    # Use non-greedy matching but allow nested content
    matches = re.findall(r'(\([^()]*(?:,\s*[^()]*)*\)|\[[^\[\]]*(?:,\s*[^\[\]]*)*\])', text)
    
    if not matches:
        return ""
    
    # Return the match with the most content (commas indicate multiple elements)
    # Prioritize structures with commas (actual tuples/lists with multiple elements)
    matches_with_commas = [m for m in matches if ',' in m]
    
    if matches_with_commas:
        return max(matches_with_commas, key=len).strip()
    
    # Fallback to longest match
    return max(matches, key=len).strip() if matches else ""


def is_primarily_numeric_answer(text: str) -> bool:
    """
    Determină dacă răspunsul este în principal numeric.
    """
    # Elimină structurile complexe mai întâi
    text_without_structs = re.sub(r'[\[\(].*?[\]\)]', '', text)

    # Caută numere (inclusiv negative și float)
    num_match = re.search(r'-?\d+(\.\d+)?', text_without_structs)
    if not num_match:
        return False

    # Exclude numele problemelor (n-queens, 8-queens etc.)
    problem_name_patterns = [
        r'\d+-queens?',
        r'\d+-colou?ring',
        r'\d+-knights?',
        r'n-queens?',
        r'k-colou?r',
    ]

    for pattern in problem_name_patterns:
        if re.search(pattern, text_without_structs):
            # Verifică dacă mai există ALT număr care să fie răspunsul
            temp_text = re.sub(pattern, '', text_without_structs)
            if not re.search(r'-?\d+', temp_text):
                return False

    # Dacă numărul este singurul conținut semnificativ
    words = text_without_structs.lower().split()
    if len(words) <= 3 and any(char.isdigit() for word in words for char in word):
        return True

    # Modele specifice pentru răspunsuri numerice
    numeric_patterns = [
        r'there\s+(are|is)\s+\d+',
        r'\d+\s+(solutions?|moves?|steps?|colors?|ways?)',
        r'answer\s+is\s+\d+',
        r'exactly\s+\d+',
        r'total\s+(of\s+)?\d+',
        r'num[ăa]r(ul)?(\s+de)?\s+.*\s+\d+',
        r'minimum\s+(of\s+)?\d+',
        r'requires?\s+\d+',
        r'valoare(a)?\s+.*\s+\d+',  # Specific Minimax
        r'noduri\s+.*\s+\d+',  # Specific Minimax
    ]

    for pattern in numeric_patterns:
        if re.search(pattern, text_without_structs):
            return True

    return False


def extract_standalone_number(text: str) -> str:
    """
    Extrage cel mai relevant număr din text.
    Suportă acum numere negative și zecimale.
    """
    # Ignorăm numerele din interiorul listelor/tuplurilor
    text_without_structs = re.sub(r'[\[\(].*?[\]\)]', '', text)

    # Modele prioritare
    priority_patterns = [
        r'(?:minim|minimum|necesit[aă]|require[sd]?|need[sd]?)\s+(-?\d+(?:\.\d+)?)',
        r'(?:exact|exactly|precisely)\s+(-?\d+(?:\.\d+)?)',
        r'(?:răspuns|answer|result|solu[tț]ie|valoare|value)[^\d]*(-?\d+(?:\.\d+)?)',
        r'(?:num[ăa]r|number|count)[^\d]*(-?\d+(?:\.\d+)?)',
        r'(?:este|is|are|:)\s+(-?\d+(?:\.\d+)?)',
    ]

    for pattern in priority_patterns:
        match = re.search(pattern, text_without_structs, re.IGNORECASE)
        if match:
            return match.group(1)

    # Fallback: primul număr găsit (inclusiv negativ)
    match = re.search(r'-?\d+(\.\d+)?', text_without_structs)
    return match.group(0) if match else ""


def extract_yes_no_response(text: str) -> Optional[str]:
    """Extrage răspuns Da/Nu."""
    text_clean = text.lower().strip()

    no_patterns = [r'\bnu\b', r'\bno\b', r'\bnegativ', r'\bfalse\b']
    for pattern in no_patterns:
        if re.search(pattern, text_clean): return 'no'

    yes_patterns = [r'\bda\b', r'\byes\b', r'\bpozitiv', r'\btrue\b']
    for pattern in yes_patterns:
        if re.search(pattern, text_clean): return 'yes'

    return None


def extract_keywords_from_text(text: str, keywords: List[str]) -> List[str]:
    """Extrage keywords prezenți în text."""
    found = []
    for keyword in keywords:
        norm_keyword = unidecode(keyword.lower().strip())
        # Folosim word boundary (\b) pentru potrivire exactă, sau potrivire parțială relaxată
        # Dacă keyword-ul are mai multe cuvinte (ex: "alpha beta"), permitem spații flexibile
        pattern = re.escape(norm_keyword).replace(r'\ ', r'\s+')
        if re.search(pattern, text, re.IGNORECASE):
            found.append(norm_keyword)
    return found


# Ajustare ponderi pentru a fi mai puțin punitive
KEYWORD_MATCH_WEIGHT = 0.65
TEXT_SIMILARITY_WEIGHT = 0.35
KEYWORD_MISS_PENALTY_PERCENT = 25  # Redus de la 30
KEYWORD_WRONG_PENALTY_EACH = 10  # Redus de la 20 (pentru a nu depuncta drastic sinonimele)
KEYWORD_WRONG_PENALTY_MAX = 30  # Redus de la 40


def evaluate_keyword_match(correct_answer: str, user_answer: str, keywords: List[str]) -> int:
    if not keywords:
        return 0

    clean_correct = unidecode(correct_answer.lower().strip())
    clean_user = unidecode(user_answer.lower().strip())

    correct_keywords = extract_keywords_from_text(clean_correct, keywords)
    user_keywords = extract_keywords_from_text(clean_user, keywords)

    if not correct_keywords:
        return 0

    matched_keywords = set(correct_keywords) & set(user_keywords)
    missed_keywords = set(correct_keywords) - set(user_keywords)
    wrong_keywords = set(user_keywords) - set(correct_keywords)

    match_score = len(matched_keywords) / len(correct_keywords) * 100
    miss_penalty = len(missed_keywords) / len(correct_keywords) * KEYWORD_MISS_PENALTY_PERCENT
    # Penalizare mai mică pentru cuvinte greșite (posibil sinonime neidentificate)
    wrong_penalty = min(len(wrong_keywords) * KEYWORD_WRONG_PENALTY_EACH, KEYWORD_WRONG_PENALTY_MAX)

    final_score = match_score - miss_penalty - wrong_penalty
    return max(0, min(100, int(final_score)))


def normalize_nash_answer(text: str) -> str:
    """
    Normalize Nash equilibrium answers to handle Romanian terminology variations.
    Maps Sus/Jos/Stanga/Dreapta to U/D/L/R for consistent comparison.
    """
    # Create a normalized version for comparison
    normalized = text.lower()
    
    # Replace Romanian terms with standardized abbreviations
    replacements = [
        (r'\bsus\b', 'u'),
        (r'\bjos\b', 'd'),
        (r'\bstanga\b', 'l'),
        (r'\bstânga\b', 'l'),
        (r'\bdreapta\b', 'r'),
    ]
    
    for pattern, replacement in replacements:
        normalized = re.sub(pattern, replacement, normalized)
    
    return normalized


def evaluate_answer(correct_answer: str, user_answer: str, keywords: Optional[List[str]] = None) -> int:
    if not user_answer:
        return 0

    clean_correct = unidecode(correct_answer.lower().strip())
    clean_user = unidecode(user_answer.lower().strip())

    # Special handling for Nash equilibrium answers with Romanian terminology
    # Normalize both answers to handle variations like "Sus" vs "U", "Stânga" vs "L", etc.
    norm_correct = normalize_nash_answer(clean_correct)
    norm_user = normalize_nash_answer(clean_user)

    # 1. Extragere structuri (Liste SAU Tupluri)
    correct_struct = extract_structured_data(norm_correct)
    user_struct = extract_structured_data(norm_user)

    # 2. Extragere Numere (suport extins)
    correct_num = extract_standalone_number(clean_correct)
    user_num = extract_standalone_number(clean_user)

    correct_yes_no = extract_yes_no_response(clean_correct)
    user_yes_no = extract_yes_no_response(clean_user)

    is_numeric_answer = is_primarily_numeric_answer(clean_correct)

    score_key_element = 0

    # --- Caz SPECIAL: Yes/No + Number (ex: "Nu. Necesită minim 4 culori") ---
    if correct_yes_no and correct_num:
        yes_no_score = 100 if correct_yes_no == user_yes_no else 0
        if correct_num == user_num:
            num_score = 100
        elif user_num:
            num_score = 50
        else:
            num_score = 0

        score_text = fuzz.WRatio(clean_correct, clean_user)
        final_score = int((yes_no_score * 0.5) + (num_score * 0.4) + (score_text * 0.1))
        return min(final_score, 100)

    # --- Caz A: Răspuns Structurat (LISTĂ sau TUPLU) ---
    if correct_struct:
        # Dacă e tuplu (paranteze rotunde), ordinea contează mai mult (Nash)
        if '(' in correct_struct:
            # For Nash equilibrium tuples, use exact matching for the content
            # Strip parentheses and spaces for comparison
            correct_content = correct_struct.strip('()').replace(' ', '').lower()
            user_content = user_struct.strip('()').replace(' ', '').lower()
            
            if correct_content == user_content:
                score_key_element = 100
            else:
                # Wrong Nash answer - give very low score
                score_key_element = 20
        else:
            # Dacă e listă (paranteze pătrate), ordinea contează mai puțin (N-Queens)
            score_key_element = fuzz.token_sort_ratio(correct_struct, user_struct)

    # --- Caz B: Răspuns NUMERIC ---
    elif correct_num and is_numeric_answer:
        if correct_num == user_num:
            score_key_element = 100
        elif user_num:
            # Număr greșit
            score_key_element = 0
        else:
            score_key_element = 0

    # --- Caz C: Răspuns TEXTUAL ---
    else:
        if keywords:
            score_keywords = evaluate_keyword_match(correct_answer, user_answer, keywords)
            score_text = fuzz.WRatio(clean_correct, clean_user)
            final_score = int((score_keywords * KEYWORD_MATCH_WEIGHT) + (score_text * TEXT_SIMILARITY_WEIGHT))
            return min(final_score, 100)
        else:
            score_key_element = 100

    # Calcul final pentru cazurile A și B
    score_text = fuzz.WRatio(norm_correct, norm_user)

    if correct_struct or (correct_num and is_numeric_answer):
        # Structura/Numărul contează 80% (crescut de la 70%)
        final_score = int((score_key_element * 0.8) + (score_text * 0.2))
    else:
        final_score = score_text

    return min(final_score, 100)


def load_keywords_for_topic(topic: str) -> List[str]:
    import json
    import os

    topic_normalized = topic.lower().replace("-", "_")
    # Ajustare cale pentru a funcționa indiferent de unde e apelat
    current_dir = os.path.dirname(__file__)
    # Încearcă mai multe căi relative posibile
    possible_paths = [
        os.path.join(current_dir, "..", "templates", f"{topic_normalized}.json"),
        os.path.join(current_dir, "templates", f"{topic_normalized}.json"),
    ]

    template_path = None
    for path in possible_paths:
        if os.path.exists(path):
            template_path = path
            break

    if not template_path:
        return []

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template = json.load(f)
            return template.get("keywords", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []