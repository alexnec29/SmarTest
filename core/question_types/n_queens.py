"""
Implementare completă pentru întrebări tip n-Queens.
Demonstrează cum parametrii leagă întrebarea de răspuns.
"""
import random
from typing import Dict, List
from .base import QuestionBase


class NQueensQuestion(QuestionBase):
    """
    Clasă pentru întrebări despre problema n-Queens.
    Întrebarea: Care este strategia optimă pentru problema n-Queens?
    """

    # Mapare dificultate -> valori posibile pentru n
    DIFFICULTY_MAP = {
        "easy": [4, 5],
        "medium": [6, 7, 8],
        "hard": [10, 12, 15]
    }

    # Strategii disponibile și când sunt optime
    STRATEGIES = {
        "backtracking": "optimal pentru toate dimensiunile",
        "backtracking_fc": "optimal cu Forward Checking pentru n > 8",
        "backtracking_mrv": "optimal cu MRV pentru n > 10",
        "backtracking_ac3": "optimal cu AC-3 pentru n > 12"
    }

    def generate_params(self) -> Dict:
        """
        Generează parametri aleatori pe baza dificultății.

        Returns:
            Dict cu 'n' (dimensiunea tablei) și 'problems' (lista de probleme)
        """
        # Alege n pe baza dificultății
        n_value = random.choice(self.DIFFICULTY_MAP[self.difficulty])

        # Generează lista de probleme pentru comparație
        problems = ["n-queens", "graph-coloring", "generalized-hanoi", "knights-tour"]
        random.shuffle(problems)

        return {
            "n": n_value,
            "problems": problems[:3],  # Selectează 3 din 4
            "main_problem": "n-queens"
        }

    def generate_question_text(self) -> str:
        """
        Generează textul întrebării folosind parametrii.

        Returns:
            String cu întrebarea formatată
        """
        n = self.params["n"]
        problems = self.params["problems"]

        question = (
            f"Problema identificată: {n}-Queens\n\n"
            f"Având în vedere problema {n}-Queens și comparând-o cu următoarele "
            f"probleme: {', '.join(problems)}, care este cea mai potrivită strategie "
            f"de rezolvare dintre cele menționate la curs?\n\n"
            f"Strategii disponibile: Backtracking, Backtracking + FC, "
            f"Backtracking + MRV, Backtracking + AC-3"
        )

        return question

    def generate_correct_answer(self) -> str:
        """
        Generează răspunsul corect pe baza parametrilor.
        Răspunsul depinde de valoarea lui n!

        Returns:
            String cu răspunsul punctual
        """
        n = self.params["n"]

        # Logica de selectare a strategiei optime
        if n <= 8:
            strategy = "Backtracking"
        elif n <= 10:
            strategy = "Backtracking cu Forward Checking (FC)"
        elif n <= 12:
            strategy = "Backtracking cu Minimum Remaining Values (MRV)"
        else:
            strategy = "Backtracking cu Arc Consistency (AC-3)"

        return strategy

    def generate_detailed_answer(self) -> str:
        """
        Generează răspuns detaliat cu explicații și justificări.

        Returns:
            String cu explicații pas cu pas
        """
        n = self.params["n"]
        strategy = self.correct_answer

        explanation = f"""
RĂSPUNS DETALIAT pentru {n}-Queens:

Strategia optimă: {strategy}

JUSTIFICARE:
1. Problema {n}-Queens este o problemă de satisfacere a restricțiilor (CSP)
   - Variabile: Pozițiile damelor pe cele {n} coloane
   - Domeniu: Fiecare damă poate fi pe oricare din cele {n} rânduri
   - Restricții: Nicio damă nu ataca alta (rând, coloană, diagonală)

2. De ce {strategy}?
"""

        if n <= 8:
            explanation += """
   - Pentru dimensiuni mici (n ≤ 8), Backtracking simplu este suficient
   - Spațiul de căutare este relativ mic (~16.777.216 stări pentru n=8)
   - Overhead-ul optimizărilor nu se justifică
   - Complexitate: O(n!) în worst case, dar pruning natural este eficient
"""
        elif n <= 10:
            explanation += """
   - Pentru dimensiuni medii (8 < n ≤ 10), Forward Checking devine eficient
   - FC elimină valori din domenii înainte de a face backtrack
   - Reduce semnificativ numărul de explorări inutile
   - Spațiul de căutare crește exponențial (>3.6M stări pentru n=10)
"""
        elif n <= 12:
            explanation += """
   - Pentru dimensiuni mari (10 < n ≤ 12), MRV este crucial
   - MRV selectează variabila cu cele mai puține valori rămase
   - Detectează fail-urile mai devreme în arbore
   - Combinat cu FC, reduce dramatic spațiul de căutare
"""
        else:
            explanation += """
   - Pentru dimensiuni foarte mari (n > 12), AC-3 este necesar
   - AC-3 face arc consistency pe toate constrângerile
   - Propagă restricțiile înainte de căutare
   - Essential pentru probleme cu >14.000.000 stări
"""

        explanation += f"""
3. Comparație cu alte probleme:
   - Graph Coloring: Similar, dar cu structură diferită
   - Generalized Hanoi: Problema de planning, nu CSP
   - Knight's Tour: Hamilton path, backtracking cu heuristici specifice

4. Complexitate pentru {n}-Queens:
   - Număr de soluții posibile: O({n}^{n})
   - Cu {strategy}: Complexitate redusă semnificativ
   - Timp de execuție estimat: {'<1s' if n <= 10 else '1-10s' if n <= 12 else '>10s'}

CONCLUZIE: {strategy} este alegerea optimă pentru n={n}.
"""

        return explanation.strip()

    def get_keywords(self) -> List[str]:
        """
        Returnează keywords pentru evaluare automată.

        Returns:
            Lista de cuvinte cheie relevante
        """
        n = self.params["n"]
        keywords = ["backtracking", "n-queens", "csp", "constraint"]

        # Adaugă keywords specifice pe baza lui n
        if n > 8:
            keywords.extend(["forward checking", "fc"])
        if n > 10:
            keywords.extend(["mrv", "minimum remaining values"])
        if n > 12:
            keywords.extend(["ac-3", "arc consistency"])

        return keywords


# Funcții helper pentru backwards compatibility
def generate_question(difficulty: str = "medium") -> str:
    """Generează întrebare (backwards compatible)."""
    q = NQueensQuestion(difficulty)
    return q.get_question()


def generate_answer(detailed: bool = False) -> str:
    """
    ATENȚIE: Această funcție NU funcționează corect!
    Nu există legătură între întrebare și răspuns.
    Folosiți clasa NQueensQuestion în loc!
    """
    q = NQueensQuestion()
    return q.get_answer(detailed)