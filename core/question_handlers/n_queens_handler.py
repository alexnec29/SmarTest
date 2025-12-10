# core/question_handlers/n_queens_handler.py

from typing import Dict, Any, Tuple
from ..base_question_handler import BaseQuestionHandler


class NQueensHandler(BaseQuestionHandler):
    """Handler for N-Queens problem questions."""
    
    def generate_custom(self, variant: Dict[str, Any], params: Dict[str, Any]) -> Tuple[str, str]:
        """
        Generate N-Queens question and answer with computation.
        
        Args:
            variant: Question variant
            params: Parameters including 'n'
            
        Returns:
            Tuple of (question, answer)
        """
        n = params.get("n", 8)
        question_id = variant.get("id", "")
        
        # Generate question from template
        question = self.format_text(variant.get("question", ""), params)
        
        # Generate computed answer
        if question_id == "num_solutions":
            answer = self._generate_num_solutions_answer(n)
        elif question_id == "first_solution_example":
            answer = self._generate_first_solution_answer(n)
        else:
            # Fallback to template
            answer = self.format_text(variant.get("answer", ""), params)
        
        return question, answer
    
    def _generate_num_solutions_answer(self, n: int) -> str:
        """Generate answer for number of solutions question."""
        solutions_map = {
            4: 2,
            8: 92,
            10: 724
        }
        
        if n in solutions_map:
            return f"There are {solutions_map[n]} distinct solutions for the {n}-Queens problem."
        else:
            return f"Counting all solutions for n={n} may be expensive; implement a solver to compute exact count."
    
    def _generate_first_solution_answer(self, n: int) -> str:
        """Generate answer for first solution example question."""
        solutions_map = {
            4: [1, 3, 0, 2],
            8: [0, 4, 7, 5, 2, 6, 1, 3],
            10: [0, 2, 5, 7, 9, 4, 8, 1, 3, 6]
        }
        
        if n in solutions_map:
            return f"One valid arrangement is: {solutions_map[n]}"
        else:
            return "Provide a valid arrangement as a list of column indices per row."
