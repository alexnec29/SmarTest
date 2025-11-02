"""
Package pentru tipurile de întrebări.
Fiecare tip de întrebare este un modul separat.
"""

from .base import QuestionBase
from .n_queens import NQueensQuestion

__all__ = [
    'QuestionBase',
    'NQueensQuestion',
]