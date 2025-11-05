# core/question_types/knights_tour.py
from typing import List, Tuple, Dict
import random

def generate_question(board_size: int = 8, ask_type: str = "strategy", start_pos: Tuple[int, int] = (1, 1)) -> str:
    """
    Generează întrebarea pentru Turul Calului.
    board_size: dimensiunea tablei (NxN).
    ask_type: "strategy", "solvability", "complexity".
    """
    start_str = f"({start_pos[0]}, {start_pos[1]})"
    
    if ask_type == "strategy":
        return f"Pentru Turul Calului pe o tablă {board_size}x{board_size}, pornind de la {start_str}, care este cea mai eficientă euristică?"
    elif ask_type == "solvability":
        return f"Este posibil un Tur al Calului (închis) pe o tablă {board_size}x{board_size}?"
    elif ask_type == "complexity":
        return f"Care este complexitatea în timp (în termeni de O-mare) pentru algoritmul de forță brută (backtracking) care găsește un tur al calului pe o tablă NxN?"
    else:
        return f"Turul Calului pe o tablă {board_size}x{board_size}: Care este strategia recomandată?"

def generate_answer(board_size: int = 8, ask_type: str = "strategy", start_pos: Tuple[int, int] = (1, 1)) -> str:
    """
    Generează răspunsul corect.
    """
    if ask_type == "strategy":
        return "Cea mai eficientă euristică este Euristică lui Warnsdorff: Calul ar trebui să se mute întotdeauna în poziția din care va avea cele mai puține mutări posibile (minimum degree)."
    elif ask_type == "solvability":
        # Tur închis (se termină pe o poziție de unde poate reveni la start)
        if board_size % 2 != 0 and board_size > 1:
             return f"Un tur închis nu este posibil pe o tablă de dimensiune impară ({board_size}x{board_size}). Un tur deschis este posibil."
        elif board_size <= 4:
             return f"Un tur închis nu este posibil pe o tablă {board_size}x{board_size}. Turul este posibil doar pe table NxN unde N >= 5."
        else:
            return "Da, un Tur al Calului închis este posibil pe majoritatea tablelor de dimensiuni mari, inclusiv pe o tablă 8x8."
    elif ask_type == "complexity":
        return "Complexitatea în timp este $O(8^{N^2})$, dar este redusă semnificativ de euristici la $O(N^2)$."
            
    return "Strategia recomandată este Euristica lui Warnsdorff."