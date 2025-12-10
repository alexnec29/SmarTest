# core/question_handlers/generalised_hanoi_handler.py

from typing import Dict, Any, Tuple
from ..base_question_handler import BaseQuestionHandler


class GeneralisedHanoiHandler(BaseQuestionHandler):
    """Handler for Generalised Hanoi problem questions."""
    
    def generate_custom(self, variant: Dict[str, Any], params: Dict[str, Any]) -> Tuple[str, str]:
        """
        Generate Generalised Hanoi question and answer with computation.
        
        Args:
            variant: Question variant
            params: Parameters including 'n_discs' and 'n_pegs'
            
        Returns:
            Tuple of (question, answer)
        """
        n_discs = params.get("n_discs", 3)
        n_pegs = params.get("n_pegs", 3)
        question_id = variant.get("id", "")
        
        # Generate question from template
        question = self.format_text(variant.get("question", ""), params)
        
        # Generate computed answer
        if question_id == "min_moves":
            answer = self._generate_min_moves_answer(n_discs, n_pegs)
        elif question_id == "complexity":
            answer = self._generate_complexity_answer(n_pegs)
        else:
            # Fallback to template
            answer = self.format_text(variant.get("answer", ""), params)
        
        return question, answer
    
    def _generate_min_moves_answer(self, n_discs: int, n_pegs: int) -> str:
        """Generate answer for minimum moves question."""
        if n_pegs == 3:
            # Standard Hanoi: 2^n - 1
            moves = (2 ** n_discs) - 1
            return f"For 3 pegs, the minimum number of moves is $2^{{{n_discs}}} - 1$, which is {moves}."
        elif n_pegs == 4 and n_discs == 4:
            # Known case (Frame-Stewart)
            return "For 4 discs and 4 pegs, the minimum is 9 moves (using Frame-Stewart algorithm)."
        else:
            return f"The exact minimum number of moves for {n_discs} discs and {n_pegs} pegs is difficult to compute and generally requires dynamic programming or a specialized solver. It is a value $M(n,k)$ where $M(n,3) = 2^n - 1$."
    
    def _generate_complexity_answer(self, n_pegs: int) -> str:
        """Generate answer for complexity question."""
        if n_pegs == 3:
            return "The time complexity for 3 pegs is $O(2^n)$, where n is the number of discs."
        else:
            return "The time complexity for $k>3$ pegs is approximately $O((\\sqrt[k-2]{2})^n)$ based on the Frame-Stewart conjecture/algorithm, which is still exponential but better than $O(2^n)$."
