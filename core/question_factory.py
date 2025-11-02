# TODO: Centralize question and answer generation for multiple types

from .question_types import n_queens

QUESTION_TYPES = {
    "n-queens": n_queens
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
