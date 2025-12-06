# TODO: Centralize question and answer generation for multiple types
import json
import os
from typing import Tuple,Dict, Any
from .question_types import n_queens
from .question_types import nash_equilibrium
from .question_types import generalised_hanoi
from .question_types import graph_coloring
from .question_types import knights_tour
from .question_types import csp   
from .question_types import minimax

QUESTION_TYPES = {
    "n-queens": n_queens,
    "nash_equilibrium": nash_equilibrium,
    "generalised_hanoi": generalised_hanoi,
    "graph_coloring": graph_coloring,
    "knights_tour": knights_tour,
    "csp": csp,
    "minimax": minimax,
    

    # TODO: Alte tipuri de intrebari
}

def generate_question_and_answer(topic: str):
    """
    Returnează întrebarea și răspunsul corect pentru topicul dat.
    """
    module = QUESTION_TYPES.get(topic.lower())
    if not module:
        # TODO: Gestionează topic necunoscut
        return None, None
    return module.generate_question(), module.generate_answer()
