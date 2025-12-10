# core/evaluator.py

from fuzzywuzzy import fuzz
from unidecode import unidecode 
import re
from typing import List, Optional

# Functie pentru a extrage primul array de numere dintr-un string (ex: solutie N-Queens)
def extract_array(text: str) -> str:
    # Cauta formatul [..., ..., ...]
    match = re.search(r'(\[.*?\])', text)
    return match.group(1).strip() if match else ""

# Functie pentru a extrage numerele din afara unui array
def is_primarily_numeric_answer(text: str) -> bool:
    """
    Determine if an answer is primarily numeric (the answer IS a number).
    
    Examples of numeric answers:
    - "There are 92 solutions"
    - "92"
    - "The answer is 42"
    
    Examples of NON-numeric answers (numbers appear incidentally):
    - "Backtracking is best for 8-Queens"
    - "Use 3 colors for the graph"
    
    Args:
        text: The answer text (normalized)
        
    Returns:
        True if the answer is primarily a numeric response
    """
    # Remove arrays first
    text_without_arrays = re.sub(r'\[.*?\]', '', text)
    
    # Extract number
    num_match = re.search(r'\b\d+\b', text_without_arrays)
    if not num_match:
        return False
    
    # Exclude common problem names with numbers (n-queens, 8-queens, etc.)
    problem_name_patterns = [
        r'\d+-queens?',
        r'\d+-colou?ring',
        r'\d+-knights?',
        r'n-queens?',
        r'k-colou?r',
    ]
    
    for pattern in problem_name_patterns:
        if re.search(pattern, text_without_arrays):
            # Check if there's ANOTHER number that's the actual answer
            temp_text = re.sub(pattern, '', text_without_arrays)
            if not re.search(r'\b\d+\b', temp_text):
                # Only number is in the problem name, not numeric answer
                return False
    
    # Get words around the number
    words = text_without_arrays.lower().split()
    
    # If the number is the ONLY significant content, it's numeric
    if len(words) <= 3 and any(char.isdigit() for word in words for char in word):
        return True
    
    # Check for numeric answer patterns
    numeric_patterns = [
        r'there\s+(are|is)\s+\d+',
        r'\d+\s+(solutions?|moves?|steps?|colors?|ways?)',
        r'answer\s+is\s+\d+',
        r'exactly\s+\d+',
        r'total\s+(of\s+)?\d+',
        r'num[ăa]r(ul)?(\s+de)?\s+.*\s+\d+',  # Romanian patterns
        r'minimum\s+(of\s+)?\d+',
        r'requires?\s+\d+',
    ]
    
    for pattern in numeric_patterns:
        if re.search(pattern, text_without_arrays):
            return True
    
    return False


def extract_standalone_number(text: str) -> str:
    # Extrage primul numar intreg standalone (ex: '92' din 'There are 92 solutions')
    # Ignoram numerele din interiorul listelor/array-urilor pentru a nu le confunda cu rezultatul final
    text_without_arrays = re.sub(r'\[.*?\]', '', text)
    match = re.search(r'\b\d+\b', text_without_arrays)
    return match.group(0) if match else ""


def extract_keywords_from_text(text: str, keywords: List[str]) -> List[str]:
    """
    Extract which keywords from the list are present in the text.
    Uses word boundary matching to avoid false positives.
    
    Args:
        text: The text to search (normalized)
        keywords: List of keywords to search for
        
    Returns:
        List of keywords found in text
    """
    found = []
    for keyword in keywords:
        # Normalize keyword
        norm_keyword = unidecode(keyword.lower().strip())
        # Use word boundary matching for exact word/phrase matches
        # Escape special regex characters in the keyword
        pattern = r'\b' + re.escape(norm_keyword) + r'\b'
        if re.search(pattern, text):
            found.append(norm_keyword)
    return found


# Scoring weights and penalties for keyword evaluation
KEYWORD_MATCH_WEIGHT = 0.6  # 60% weight for keyword matching in textual answers
TEXT_SIMILARITY_WEIGHT = 0.4  # 40% weight for text similarity in textual answers
KEYWORD_MISS_PENALTY_PERCENT = 30  # Penalty percentage for each missed keyword
KEYWORD_WRONG_PENALTY_EACH = 20  # Penalty for each wrong keyword present
KEYWORD_WRONG_PENALTY_MAX = 40  # Maximum penalty for wrong keywords


def evaluate_keyword_match(correct_answer: str, user_answer: str, keywords: List[str]) -> int:
    """
    Evaluate how well keywords match between correct and user answer.
    
    This gives heavy weight to correct keywords being present in user answer.
    Penalizes presence of wrong keywords (keywords in correct answer but not in user).
    
    Args:
        correct_answer: The correct answer text
        user_answer: The user's answer text
        keywords: List of important keywords for this topic
        
    Returns:
        Score from 0-100 based on keyword matching
    """
    if not keywords:
        return 0
    
    clean_correct = unidecode(correct_answer.lower().strip())
    clean_user = unidecode(user_answer.lower().strip())
    
    # Find which keywords appear in each answer
    correct_keywords = extract_keywords_from_text(clean_correct, keywords)
    user_keywords = extract_keywords_from_text(clean_user, keywords)
    
    if not correct_keywords:
        # No important keywords in correct answer, can't evaluate this way
        return 0
    
    # Calculate matches and misses
    matched_keywords = set(correct_keywords) & set(user_keywords)
    missed_keywords = set(correct_keywords) - set(user_keywords)
    wrong_keywords = set(user_keywords) - set(correct_keywords)
    
    # Score based on:
    # - Matched keywords: positive contribution
    # - Missed keywords: negative contribution
    # - Wrong keywords: penalty
    
    match_score = len(matched_keywords) / len(correct_keywords) * 100
    miss_penalty = len(missed_keywords) / len(correct_keywords) * KEYWORD_MISS_PENALTY_PERCENT
    wrong_penalty = min(len(wrong_keywords) * KEYWORD_WRONG_PENALTY_EACH, KEYWORD_WRONG_PENALTY_MAX)
    
    final_score = match_score - miss_penalty - wrong_penalty
    return max(0, min(100, int(final_score)))


def evaluate_answer(correct_answer: str, user_answer: str, keywords: Optional[List[str]] = None) -> int:
    """
    Evaluează răspunsul folosind o metodă ponderată avansată.
    
    Pondere:
    - Arrays/Lists: 70% match exact, 30% text
    - Numbers: 70% match exact, 30% text  
    - Text with keywords: 60% keywords, 40% text similarity
    - Text without keywords: 100% text similarity (fallback)
    
    Args:
        correct_answer: The correct answer
        user_answer: The user's answer
        keywords: Optional list of important keywords for this topic
        
    Returns:
        Score from 0-100
    """
    if not user_answer:
        return 0

    # 1. Normalizare
    clean_correct = unidecode(correct_answer.lower().strip())
    clean_user = unidecode(user_answer.lower().strip())
    
    # 2. Extragerea Elementelor Cheie
    correct_array = extract_array(clean_correct)
    user_array = extract_array(clean_user)
    
    correct_num = extract_standalone_number(clean_correct)
    user_num = extract_standalone_number(clean_user)
    
    # Determine if this is truly a numeric answer vs text with incidental numbers
    is_numeric_answer = is_primarily_numeric_answer(clean_correct)

    score_key_element = 0
    
    # --- Caz A: Răspunsul este o LISTĂ / ARRAY (ex: solutie N-Queens) ---
    if correct_array:
        # Folosim token_sort_ratio pentru a ne asigura ca elementele din lista sunt in aceeasi ordine
        score_key_element = fuzz.token_sort_ratio(correct_array, user_array)
        
    # --- Caz B: Răspunsul este un NUMĂR SINGUR (ex: nr. solutii N-Queens sau nr. mutari Hanoi) ---
    elif correct_num and is_numeric_answer:
        # Match exact pe număr sau WRatio pe număr (dacă ambele sunt extrase)
        if correct_num == user_num:
            score_key_element = 100
        elif user_num:
            # Dacă ambele conțin un număr, dar nu e perfect, dăm un scor parțial.
            score_key_element = fuzz.ratio(correct_num, user_num) 
        else:
            # Nu a gasit numarul cheie in raspunsul utilizatorului
            score_key_element = 0

    # --- Caz C: Răspunsul este predominant TEXTUAL (ex: Strategie Backtracking) ---
    else:
        # For textual answers, use keyword-aware evaluation if keywords are provided
        if keywords:
            # Use advanced keyword-based scoring
            score_keywords = evaluate_keyword_match(correct_answer, user_answer, keywords)
            score_text = fuzz.WRatio(clean_correct, clean_user)
            
            # Weight: keyword matching and text similarity
            # Using constants defined at module level
            final_score = int((score_keywords * KEYWORD_MATCH_WEIGHT) + (score_text * TEXT_SIMILARITY_WEIGHT))
            return min(final_score, 100)
        else:
            # Fallback: use only fuzzy text matching
            score_key_element = 100  # Setam elementul cheie la 100, dar ponderea va fi 100% text

    
    # 3. Scorul Textual (for Cases A and B, or C without keywords)
    # Folosim WRatio pentru formularea generală (textul)
    score_text = fuzz.WRatio(clean_correct, clean_user)
    
    # 4. Pondere Finală
    if correct_array or (correct_num and is_numeric_answer):
        # Daca exista un element cheie (array sau numar), il ponderam cu 70%
        final_score = int((score_key_element * 0.7) + (score_text * 0.3))
    else:
        # Daca e doar text (Caz C fara keywords), folosim doar WRatio (100% text)
        final_score = score_text

    # Ne asigurăm că scorul final nu depășește 100
    return min(final_score, 100)


def load_keywords_for_topic(topic: str) -> List[str]:
    """
    Load keywords for a specific topic from its template.
    
    Args:
        topic: The topic name (e.g., 'n-queens', 'minimax', 'csp')
               Can use hyphens or underscores (both will be normalized)
        
    Returns:
        List of keywords for this topic, or empty list if not found
    """
    import json
    import os
    
    # Normalize topic name: convert hyphens to underscores for file lookup
    topic_normalized = topic.lower().replace("-", "_")
    template_path = os.path.join(os.path.dirname(__file__), "..", "templates", f"{topic_normalized}.json")
    
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template = json.load(f)
            return template.get("keywords", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []