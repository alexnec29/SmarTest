# core/question_factory.py

import json
import os
from typing import Tuple,Dict, Any
from .question_types import n_queens
from .question_types import nash_equilibrium  # <--- 1. IMPORTĂ MODULUL NOU
from .question_types import generalised_hanoi
from .question_types import graph_coloring
from .question_types import knights_tour

QUESTION_TYPES = {
    "n-queens": n_queens,
    "nash-equilibrium": nash_equilibrium,     # <--- 2. ADAUGĂ-L ÎN DICȚIONAR\
    "generalised-hanoi": generalised_hanoi,
    "graph-coloring": graph_coloring,
    "knights-tour": knights_tour
    # TODO: Alte tipuri de intrebari
}

TEMPLATES_PATH = os.path.join(os.path.dirname(__file__),"..", "templates")   

def load_template(topic: str) -> Dict[str, Any]:
    """
    Încarcă un șablon JSON pentru un topic dat.
    """
    path = os.path.join(TEMPLATES_PATH, f"{topic.replace('-', '_')}.json")
    try:
        with open(path,"r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def generate_question_and_answer(topic: str, params: Dict[str, Any] = None) -> Tuple[Any, Any]:
    """
    Returnează întrebarea și răspunsul corect pentru topicul dat.
    params poate conține parametri dinamici (ex: {'n':8, 'ask_type':'strategy'}).
    """
    params = params or {}
    template = load_template(topic)

    #Completeaza valorile implicite din template daca exista

    if "params" in template:
        for k, meta in template["params"].items():
            params.setdefault(k, meta.get("default"))

    module = QUESTION_TYPES.get(topic.lower())
    if not module:
        #topic necunoscut folosim template-ul daca exista
        q= template.get("question")
        a = template.get("answer")
        if q:
            try:
                q = q.format(**params)
            except Exception:
                pass
        return q, a
    
    #daca modulul are functii, le apelam cu parametrii
    q = module.generate_question(**params) if hasattr(module, "generate_question") else template.get("question","").format(**params)
    a = module.generate_answer(**params) if hasattr(module, "generate_answer") else template.get("answer","").format(**params)
    return q, a