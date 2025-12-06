import random
from typing import Dict, Any, Tuple, List

# Numele strategiilor
STRATEGIES_J1 = ["Sus", "Jos"]
STRATEGIES_J2 = ["Stânga", "Dreapta"]

def generate_game_matrix() -> Tuple[Dict[str, Tuple[int, int]], str]:
    """
    Generează o matrice 2x2 cu recompense aleatorii (între 0 și 3) și calculează Echilibrul Nash Pur.
    Returnează: (matricea, răspunsul corect)
    """
    matrix = {}
    
    # Generează recompense aleatorii pentru cele 4 celule
    for s1 in STRATEGIES_J1:
        for s2 in STRATEGIES_J2:
            payoff_j1 = random.randint(0, 3)
            payoff_j2 = random.randint(0, 3)
            matrix[f"{s1}-{s2}"] = (payoff_j1, payoff_j2)

    # Caută Echilibrul Nash Pur
    nash_equilibria: List[Tuple[str, str]] = []

    for s1 in STRATEGIES_J1:
        for s2 in STRATEGIES_J2:
            is_nash = True
            
            # 1. Testează Jucătorul 1 (Rândul): Are J1 un stimulent să schimbe?
            # Află ce se întâmplă dacă J1 schimbă strategia (de la s1 la alt rând)
            other_s1 = [r for r in STRATEGIES_J1 if r != s1][0]
            
            # Recompensa lui J1 în echilibrul potențial:
            payoff_j1_current = matrix[f"{s1}-{s2}"][0]
            # Recompensa lui J1 dacă schimbă la other_s1, dar J2 rămâne la s2:
            payoff_j1_change = matrix[f"{other_s1}-{s2}"][0]

            if payoff_j1_change > payoff_j1_current:
                # J1 ar avea stimulent să schimbe. Nu este echilibru.
                is_nash = False

            # 2. Testează Jucătorul 2 (Coloana): Are J2 un stimulent să schimbe?
            if is_nash:
                # Află ce se întâmplă dacă J2 schimbă strategia (de la s2 la altă coloană)
                other_s2 = [c for c in STRATEGIES_J2 if c != s2][0]

                # Recompensa lui J2 în echilibrul potențial:
                payoff_j2_current = matrix[f"{s1}-{s2}"][1]
                # Recompensa lui J2 dacă schimbă la other_s2, dar J1 rămâne la s1:
                payoff_j2_change = matrix[f"{s1}-{other_s2}"][1]

                if payoff_j2_change > payoff_j2_current:
                    # J2 ar avea stimulent să schimbe. Nu este echilibru.
                    is_nash = False
            
            if is_nash:
                nash_equilibria.append((s1, s2))

    # Construiește răspunsul corect
    if nash_equilibria:
        # Formatul [('Rând', 'Coloană'), ...]
        nash_str = ", ".join([f"({s1}, {s2})" for s1, s2 in nash_equilibria])
        answer_str = f"Da, există echilibru Nash pur. Acesta este {nash_str}."
    else:
        answer_str = "Nu, nu există un echilibru Nash pur (sau există doar în strategii mixte)."

    return matrix, answer_str


def generate_question(params: Dict[str, Any] = None) -> str:
    """
    Generează întrebarea pentru Echilibrul Nash, incluzând matricea generată dinamic.
    """
    # Folosim o matrice pre-generată sau generăm una nouă
    matrix, _ = generate_game_matrix()
    
    # Construiește vizualizarea matricei
    payoff_sus_stanga = f"({matrix['Sus-Stânga'][0]}, {matrix['Sus-Stânga'][1]})"
    payoff_sus_dreapta = f"({matrix['Sus-Dreapta'][0]}, {matrix['Sus-Dreapta'][1]})"
    payoff_jos_stanga = f"({matrix['Jos-Stânga'][0]}, {matrix['Jos-Stânga'][1]})"
    payoff_jos_dreapta = f"({matrix['Jos-Dreapta'][0]}, {matrix['Jos-Dreapta'][1]})"

    matrix_str = (
        "Matricea jocului (Jucătorul 1 alege rândul, Jucătorul 2 alege coloana):\n"
        "Format (Recompensă J1, Recompensă J2)\n\n"
        "        Jucătorul 2\n"
        "          Stânga   Dreapta\n"
        "Jucătorul 1\n"
        f"    Sus     {payoff_sus_stanga}    {payoff_sus_dreapta}\n"
        f"    Jos     {payoff_jos_stanga}    {payoff_jos_dreapta}"
    )
    
    return f"Pentru jocul dat în forma normală (matricea atașată), există echilibru Nash pur? Care este acesta?\n\n{matrix_str}"

def generate_answer(params: Dict[str, Any] = None) -> str:
    """
    Generează răspunsul corect pentru Echilibrul Nash, folosind solver-ul.
    """
    _, answer_str = generate_game_matrix()
    return answer_str