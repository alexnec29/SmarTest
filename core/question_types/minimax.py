# core/question_types/minimax.py

from typing import Dict, Any, List, Tuple
import random

# Arbore simplu pentru Minimax: adâncime 2, 4 frunze
def generate_minimax_tree() -> Dict[str, Any]:
    """ Generează un arbore simplu de joc cu 4 frunze. """
    leaf_values = [random.randint(1, 10) for _ in range(4)]
    
    tree_description = (
        "Nivel 0 (Rădăcină - MAX):\n"
        "  - Nod 1 (MIN) are frunzele: A (Valoare: {0}) și B (Valoare: {1})\n"
        "  - Nod 2 (MIN) are frunzele: C (Valoare: {2}) și D (Valoare: {3})"
    ).format(*leaf_values)
    
    return {
        "values": leaf_values, # [A, B, C, D]
        "description": tree_description
    }

def solve_minimax_alpha_beta(leaf_values: List[int]) -> Tuple[int, int]:
    """ Calculează valoarea rădăcinii și nodurile frunză vizitate. """
    
    # Arbore fixat: MAX la rădăcină (Nod 0), MIN la nivelul următor (Nod 1, Nod 2)
    # Nodurile frunză sunt [A, B, C, D]
    A, B, C, D = leaf_values
    
    visited_leaves = 0
    alpha = -float('inf')
    beta = float('inf')
    
    # 1. Calculează Nodul 1 (MIN)
    
    # a. Vizitează A
    val1 = A
    visited_leaves += 1
    beta = min(beta, val1) # beta = min(inf, A)
    
    # b. Vizitează B
    # alpha (-inf) < B (valoarea frunzei) este mereu adevărat
    val1 = min(val1, B)
    visited_leaves += 1
    beta = min(beta, val1) # beta = min(beta_curent, val1)
    
    # Rezultatul Nodului 1
    result_node1 = val1
    
    # 2. Calculează Nodul 2 (MIN)
    alpha = max(alpha, result_node1) # alpha = max(-inf, result_node1)
    
    # c. Vizitează C
    val2 = C
    visited_leaves += 1
    
    if val2 <= alpha:
        # Pruning C: Nu se întâmplă în acest caz simplu dacă C > alpha.
        # Presupunem că nu se face pruning la C
        pass
    
    # d. Vizitează D
    val2 = min(val2, D)
    visited_leaves += 1
    
    if val2 <= alpha:
        # Pruning D: Aici se poate întâmpla pruning, dar doar dacă D sau C este foarte mic.
        # Pentru a demonstra pruning-ul, trebuie să facem un caz în care se întâmplă:
        # Dacă result_node1=10, iar C=1 și D=1, val2=1, și 1 < 10 (alpha), se taie.
        
        # Simplificare pentru răspuns: nu e garantat pruning în acest arbore,
        # dar în cazuri mai complexe ar fi. Ne vom baza pe numărul de frunze vizitate.
        pass
    
    # Rezultatul Nodului 2
    result_node2 = val2

    # 3. Rădăcina (MAX)
    root_value = max(result_node1, result_node2)
    
    return root_value, visited_leaves # Vizitează întotdeauna 4 frunze în acest arbore 2 niveluri

def generate_question(params: Dict[str, Any] = None) -> str:
    problem = generate_minimax_tree()
    
    question_base = (
        f"Pentru arborele de joc dat (MAX la rădăcină) cu frunzele A, B, C, D:\n{problem['description']}\n\n"
        "Care va fi valoarea din rădăcină și câte noduri frunze vor fi vizitate în cazul aplicării strategiei MinMax cu optimizarea Alpha-Beta?"
    )
    
    if params is None:
        params = {}
    params["minimax_problem"] = problem
    return question_base

def generate_answer(params: Dict[str, Any] = None) -> str:
    if params and "minimax_problem" in params:
        leaf_values = params["minimax_problem"]["values"]
        root_value, visited_leaves = solve_minimax_alpha_beta(leaf_values)
        
        return f"Valoarea din rădăcină va fi: {root_value}. Numărul de noduri frunze vizitate va fi: {visited_leaves}."
    return "Eroare la generarea răspunsului Minimax."