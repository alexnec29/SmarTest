# core/question_types/nash_equilibrium.py

from typing import Dict, Any

# TODO: Implementa generare dinamică a matricilor de joc
# TODO: Implementa un solver care găsește echilibrul Nash

def generate_question(params: Dict[str, Any] = None) -> str:
    """
    Generează întrebarea pentru Echilibrul Nash.
    Momentan, folosește o întrebare statică.
    """
    # În viitor, am putea genera o matrice aleatorie aici
    
    return (
        "Pentru jocul dat în forma normală (matricea atașată), există echilibru Nash pur? Care este acesta?\n\n"
        "Matricea jocului (Jucătorul 1 alege rândul, Jucătorul 2 alege coloana):\n"
        "Format (Recompensă J1, Recompensă J2)\n\n"
        "        Jucătorul 2\n"
        "          Stânga   Dreapta\n"
        "Jucătorul 1\n"
        "    Sus     (1, 2)    (0, 1)\n"
        "    Jos     (2, 1)    (1, 0)"
    )

def generate_answer(params: Dict[str, Any] = None) -> str:
    """
    Generează răspunsul corect pentru Echilibrul Nash.
    """
    # Răspunsul corespunzător matricei de mai sus.
    # (Jos, Stânga) este echilibru deoarece:
    # - Dacă J1 alege 'Jos', J2 preferă 'Stânga' (primește 1 vs 0)
    # - Dacă J2 alege 'Stânga', J1 preferă 'Jos' (primește 2 vs 1)
    # Niciun jucător nu are un stimulent să devieze unilateral.
    
    return "Da, există un echilibru Nash pur. Acesta este (Jos, Stânga)."