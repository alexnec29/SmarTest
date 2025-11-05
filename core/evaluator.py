# core/evaluator.py

from fuzzywuzzy import fuzz
from unidecode import unidecode 
import re # <-- Adaugat pentru a extrage numere si liste

# Functie pentru a extrage primul array de numere dintr-un string (ex: solutie N-Queens)
def extract_array(text: str) -> str:
    # Cauta formatul [..., ..., ...]
    match = re.search(r'(\[.*?\])', text)
    return match.group(1).strip() if match else ""

# Functie pentru a extrage numerele din afara unui array
def extract_standalone_number(text: str) -> str:
    # Extrage primul numar intreg standalone (ex: '92' din 'There are 92 solutions')
    # Ignoram numerele din interiorul listelor/array-urilor pentru a nu le confunda cu rezultatul final
    text_without_arrays = re.sub(r'\[.*?\]', '', text)
    match = re.search(r'\b\d+\b', text_without_arrays)
    return match.group(0) if match else ""


def evaluate_answer(correct_answer: str, user_answer: str) -> int:
    """
    Evaluează răspunsul folosind o metodă ponderată: 70% pe elemente cheie (listă/număr) 
    și 30% pe formularea textuală.
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

    score_key_element = 0
    
    # --- Caz A: Răspunsul este o LISTĂ / ARRAY (ex: solutie N-Queens) ---
    if correct_array:
        # Folosim token_sort_ratio pentru a ne asigura ca elementele din lista sunt in aceeasi ordine
        score_key_element = fuzz.token_sort_ratio(correct_array, user_array)
        
    # --- Caz B: Răspunsul este un NUMĂR SINGUR (ex: nr. solutii N-Queens sau nr. mutari Hanoi) ---
    elif correct_num:
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
        # Fara element cheie, ne bazam pe WRatio pentru tot textul.
        score_key_element = 100 # Setam elementul cheie la 100, dar ponderea va fi 100% text

    
    # 3. Scorul Textual
    # Folosim WRatio pentru formularea generală (textul)
    score_text = fuzz.WRatio(clean_correct, clean_user)
    
    # 4. Pondere Finală
    if correct_array or correct_num:
        # Daca exista un element cheie (array sau numar), il ponderam cu 70%
        final_score = int((score_key_element * 0.7) + (score_text * 0.3))
    else:
        # Daca e doar text (Caz C), folosim doar WRatio (100% text)
        final_score = score_text

    # Ne asigurăm că scorul final nu depășește 100
    return min(final_score, 100)