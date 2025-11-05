# core/question_types/graph_coloring.py
from typing import List, Dict, Tuple

# Exemplu de graf: noduri {1, 2, 3, 4, 5} și muchii.
# Graful din problema clasică a culorilor: K-4 (patru noduri complet conectate)
# Muchiile: (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)
def get_example_graph(graph_id: str) -> Dict[str, List[Tuple[int, int]]]:
    if graph_id == "k4":
        return {
            "nodes": [1, 2, 3, 4],
            "edges": [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)],
            "name": "Graful K4 (Complet, 4 noduri)"
        }
    elif graph_id == "wheel5":
         return {
            "nodes": [1, 2, 3, 4, 5],
            "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 3)], # Simplu
            "name": "Graful Roată W5"
        }
    return get_example_graph("k4") # Fallback

def generate_question(graph_id: str = "k4", ask_type: str = "chromatic_number", k_colors: int = 3) -> str:
    """
    Generează întrebarea pentru Colorarea Grafurilor.
    """
    graph = get_example_graph(graph_id)
    edges_str = ", ".join([f"({u},{v})" for u, v in graph["edges"]])
    
    question_base = f"Fie graful cu nodurile {graph['nodes']} și muchiile: {{{edges_str}}}. "

    if ask_type == "chromatic_number":
        return question_base + "Care este numărul cromatic (numărul minim de culori necesare)?"
    elif ask_type == "is_k_colorable":
        return question_base + f"Poate fi colorat graful cu maxim {k_colors} culori (excluzând nodul {graph['nodes'][0]})?"
    elif ask_type == "strategy":
        return question_base + "Care este cea mai potrivită strategie de rezolvare (algoritm)?"
    else:
        return question_base + "Care este numărul cromatic?"

def generate_answer(graph_id: str = "k4", ask_type: str = "chromatic_number", k_colors: int = 3) -> str:
    """
    Generează răspunsul corect.
    """
    graph = get_example_graph(graph_id)
    
    if ask_type == "strategy":
        return "Cea mai potrivită strategie este Backtracking-ul cu euristici (ex: MRV - Most Restricted Variable) sau algoritmi de forță brută optimizați."
        
    elif graph_id == "k4":
        if ask_type == "chromatic_number":
            return f"Graful K4 este un graf complet, deci numărul cromatic este egal cu numărul de noduri: 4."
        elif ask_type == "is_k_colorable":
            # K4 necesită 4 culori, deci răspunsul depinde de k_colors
            return "Da" if k_colors >= 4 else "Nu. Graful necesită minim 4 culori (numărul cromatic)."

    elif graph_id == "wheel5":
        if ask_type == "chromatic_number":
             return "Numărul cromatic este 3 (pentru că nu este un graf complet și nu conține un ciclu impar)."
        elif ask_type == "is_k_colorable":
            # W5 necesită 3 culori
            return "Da" if k_colors >= 3 else "Nu. Graful necesită minim 3 culori (numărul cromatic)."
            
    return "Răspuns necunoscut."