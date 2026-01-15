# core/question_handlers/nash_equilibrium_handler.py

from typing import Dict, Any, Tuple
import random
from ..base_question_handler import BaseQuestionHandler

class NashEquilibriumHandler(BaseQuestionHandler):
    """Handler for Nash Equilibrium problem questions."""

    def generate_random_game(self) -> Dict[str, Any]:
        """Generate a random 2x2 normal-form game."""
        # Payoffs as (J1, J2)
        return {
            "U_L": (random.randint(0, 5), random.randint(0, 5)),
            "U_R": (random.randint(0, 5), random.randint(0, 5)),
            "D_L": (random.randint(0, 5), random.randint(0, 5)),
            "D_R": (random.randint(0, 5), random.randint(0, 5)),
        }

    def find_nash_pure(self, game: Dict[str, Tuple[int, int]]) -> list:
        """Return all pure strategy Nash equilibria."""
        equilibria = []

        # Best responses for J1
        # For each column (L, R), J1 compares U vs D
        # J1 wants to maximize first payoff element
        col_L = [("U", game["U_L"]), ("D", game["D_L"])]
        col_R = [("U", game["U_R"]), ("D", game["D_R"])]

        best_J1_L = max(col_L, key=lambda x: x[1][0])[0]
        best_J1_R = max(col_R, key=lambda x: x[1][0])[0]

        # Best responses for J2
        # For each row (U, D), J2 compares L vs R
        # J2 wants to maximize second payoff element
        row_U = [("L", game["U_L"]), ("R", game["U_R"])]
        row_D = [("L", game["D_L"]), ("R", game["D_R"])]

        best_J2_U = max(row_U, key=lambda x: x[1][1])[0]
        best_J2_D = max(row_D, key=lambda x: x[1][1])[0]

        # Check each profile
        profiles = {
            ("U", "L"): ("U" == best_J1_L and "L" == best_J2_U),
            ("U", "R"): ("U" == best_J1_R and "R" == best_J2_U),
            ("D", "L"): ("D" == best_J1_L and "L" == best_J2_D),
            ("D", "R"): ("D" == best_J1_R and "R" == best_J2_D),
        }

        return [p for p, ok in profiles.items() if ok]

    def format_game_matrix(self, g):
        """Format game matrix with Romanian terminology."""
        return (
            f"           Jucătorul 2\n"
            f"           Stânga     Dreapta\n"
            f"Jucătorul 1\n"
            f"  Sus      {g['U_L']}      {g['U_R']}\n"
            f"  Jos      {g['D_L']}      {g['D_R']}"
        )

    def generate_custom(self, variant: Dict[str, Any], params: Dict[str, Any]) -> Tuple[str, str]:

        question_id = variant.get("id", "")

        # --- Dynamic Nash equilibrium computation ---
        if question_id == "nash_equilibrium_dynamic":

            # 1. generate random game
            game = self.generate_random_game()

            # 2. compute Nash equilibria
            equilibria = self.find_nash_pure(game)

            # 3. build question text
            question = (
                    "Considerați următorul joc în formă normală:\n\n" +
                    self.format_game_matrix(game) +
                    "\n\nExistă echilibru Nash pur? Care este acesta?"
            )

            # 4. build answer text with Romanian terminology
            if equilibria:
                # Map U->Sus, D->Jos, L->Stânga, R->Dreapta
                translation_map = {
                    'U': 'Sus', 'D': 'Jos',
                    'L': 'Stânga', 'R': 'Dreapta'
                }
                eq_str = ", ".join([f"({translation_map.get(s1, s1)}, {translation_map.get(s2, s2)})" 
                                   for s1, s2 in equilibria])
                answer = f"Da, există echilibru Nash pur. Echilibrul(e) este(sunt): {eq_str}."
            else:
                answer = "Acest joc nu are niciun echilibru Nash pur."

            return question, answer

        # --- Fallback for static JSON entry ---
        question = self.format_text(variant.get("question", ""), params)
        answer = self.format_text(variant.get("answer", ""), params)
        return question, answer
