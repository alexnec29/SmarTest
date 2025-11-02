"""
Factory pentru crearea întrebărilor.
Gestionează toate tipurile de întrebări disponibile.
"""
from typing import Dict, Type, Optional
from .question_types.base import QuestionBase
from .question_types.n_queens import NQueensQuestion


class QuestionFactory:
    """
    Factory class pentru crearea întrebărilor.
    Permite înregistrarea dinamică de noi tipuri de întrebări.
    """

    # Registry pentru toate tipurile de întrebări disponibile
    _registry: Dict[str, Type[QuestionBase]] = {}

    @classmethod
    def register(cls, name: str, question_class: Type[QuestionBase]):
        """
        Înregistrează un nou tip de întrebare.

        Args:
            name: Numele tipului (ex: "n-queens")
            question_class: Clasa care implementează QuestionBase
        """
        cls._registry[name.lower()] = question_class

    @classmethod
    def create(cls, question_type: str, difficulty: str = "medium") -> Optional[QuestionBase]:
        """
        Creează o instanță de întrebare a tipului specificat.

        Args:
            question_type: Tipul întrebării (ex: "n-queens")
            difficulty: Nivelul de dificultate ("easy", "medium", "hard")

        Returns:
            Instanță QuestionBase sau None dacă tipul nu există
        """
        question_class = cls._registry.get(question_type.lower())
        if not question_class:
            return None

        # Creează instanța și generează întrebarea completă
        question = question_class(difficulty)
        question.create()  # Această metodă generează tot: params, question, answer
        return question

    @classmethod
    def get_available_types(cls) -> list:
        """Returnează lista de tipuri de întrebări disponibile."""
        return list(cls._registry.keys())


# Înregistrează tipurile disponibile
QuestionFactory.register("n-queens", NQueensQuestion)


# TODO: Adăugați alte tipuri aici
# QuestionFactory.register("nash-equilibrium", NashEquilibriumQuestion)
# QuestionFactory.register("csp-backtracking", CSPBacktrackingQuestion)
# QuestionFactory.register("minimax-alphabeta", MinimaxAlphaBetaQuestion)


# Funcții helper pentru backwards compatibility
def generate_question_and_answer(topic: str, difficulty: str = "medium"):
    """
    Generează întrebare și răspuns (backwards compatible).

    Args:
        topic: Tipul întrebării
        difficulty: Nivelul de dificultate

    Returns:
        Tuple (question_text, correct_answer) sau (None, None)
    """
    question = QuestionFactory.create(topic, difficulty)
    if not question:
        return None, None

    return question.get_question(), question.get_answer()


def create_question(topic: str, difficulty: str = "medium") -> Optional[QuestionBase]:
    """
    Creează o întrebare completă (metoda recomandată).

    Args:
        topic: Tipul întrebării
        difficulty: Nivelul de dificultate

    Returns:
        Instanță QuestionBase

    Example:
        >>> q = create_question("n-queens", "hard")
        >>> print(q.get_question())
        >>> print(q.get_answer(detailed=True))
        >>> score = evaluate_answer(q.correct_answer, user_answer)
    """
    return QuestionFactory.create(topic, difficulty)