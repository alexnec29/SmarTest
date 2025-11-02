"""
Clasa de bază abstractă pentru toate tipurile de întrebări.
Fiecare tip de întrebare va moșteni din această clasă.
"""
from abc import ABC, abstractmethod
from typing import Dict, List
import random


class QuestionBase(ABC):
    """
    Clasă abstractă pentru toate tipurile de întrebări.
    Asigură că fiecare întrebare are parametri proprii și răspunsul corect asociat.
    """

    def __init__(self, difficulty: str = "medium"):
        """
        Inițializează întrebarea cu dificultatea specificată.

        Args:
            difficulty: Nivelul de dificultate ("easy", "medium", "hard")
        """
        self.difficulty = difficulty
        self.params = {}  # Parametrii specifici întrebării (n, matrice, etc.)
        self.correct_answer = None  # Răspunsul corect va fi generat
        self.question_text = None  # Textul întrebării

    @abstractmethod
    def generate_params(self) -> Dict:
        """
        Generează parametrii aleatori pentru întrebare (ex: n pentru n-queens).
        Trebuie implementat de fiecare subclasă.

        Returns:
            Dict cu parametrii generați
        """
        pass

    @abstractmethod
    def generate_question_text(self) -> str:
        """
        Generează textul întrebării pe baza parametrilor.
        Trebuie implementat de fiecare subclasă.

        Returns:
            String cu textul întrebării
        """
        pass

    @abstractmethod
    def generate_correct_answer(self) -> str:
        """
        Generează răspunsul corect pe baza parametrilor.
        Trebuie implementat de fiecare subclasă.

        Returns:
            String cu răspunsul corect
        """
        pass

    @abstractmethod
    def generate_detailed_answer(self) -> str:
        """
        Generează răspuns detaliat cu explicații și calcule.
        Trebuie implementat de fiecare subclasă.

        Returns:
            String cu răspunsul detaliat
        """
        pass

    @abstractmethod
    def get_keywords(self) -> List[str]:
        """
        Returnează keywords pentru evaluarea răspunsului.
        Trebuie implementat de fiecare subclasă.

        Returns:
            Lista de keywords
        """
        pass

    def create(self):
        """
        Creează întrebarea completă: generează parametri, întrebare și răspuns.
        Aceasta este metoda principală care leagă totul împreună!
        """
        self.params = self.generate_params()
        self.question_text = self.generate_question_text()
        self.correct_answer = self.generate_correct_answer()

    def get_question(self) -> str:
        """Returnează textul întrebării."""
        if not self.question_text:
            self.create()
        return self.question_text

    def get_answer(self, detailed: bool = False) -> str:
        """
        Returnează răspunsul (punctual sau detaliat).

        Args:
            detailed: Dacă True, returnează explicații detaliate

        Returns:
            Răspunsul corect
        """
        if not self.correct_answer:
            self.create()
        return self.generate_detailed_answer() if detailed else self.correct_answer

    def to_dict(self) -> Dict:
        """
        Exportă întrebarea ca dicționar (util pentru salvare în JSON/PDF).

        Returns:
            Dict cu toate informațiile întrebării
        """
        if not self.question_text:
            self.create()

        return {
            "type": self.__class__.__name__,
            "difficulty": self.difficulty,
            "params": self.params,
            "question": self.question_text,
            "answer": self.correct_answer,
            "detailed_answer": self.generate_detailed_answer(),
            "keywords": self.get_keywords()
        }