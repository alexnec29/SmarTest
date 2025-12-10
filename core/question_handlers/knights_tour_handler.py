# core/question_handlers/knights_tour_handler.py

from typing import Dict, Any, Tuple
from ..base_question_handler import BaseQuestionHandler


class KnightsTourHandler(BaseQuestionHandler):
    """Handler for Knight's Tour problem questions."""
    
    def generate_custom(self, variant: Dict[str, Any], params: Dict[str, Any]) -> Tuple[str, str]:
        """
        Generate Knight's Tour question and answer with computation.
        
        Args:
            variant: Question variant
            params: Parameters including 'board_size' and 'start_pos'
            
        Returns:
            Tuple of (question, answer)
        """
        board_size = params.get("board_size", 8)
        start_pos = params.get("start_pos", [1, 1])
        question_id = variant.get("id", "")
        
        # Format start_pos as string for template
        if isinstance(start_pos, list):
            params["start_pos"] = f"({start_pos[0]}, {start_pos[1]})"
        
        # Generate question from template
        question = self.format_text(variant.get("question", ""), params)
        
        # Generate computed answer
        if question_id == "solvability":
            answer = self._generate_solvability_answer(board_size)
        else:
            # Fallback to template
            answer = self.format_text(variant.get("answer", ""), params)
        
        return question, answer
    
    def _generate_solvability_answer(self, board_size: int) -> str:
        """Generate answer for solvability question."""
        # Tur închis (se termină pe o poziție de unde poate reveni la start)
        if board_size % 2 != 0 and board_size > 1:
            return f"Un tur închis nu este posibil pe o tablă de dimensiune impară ({board_size}x{board_size}). Un tur deschis este posibil."
        elif board_size <= 4:
            return f"Un tur închis nu este posibil pe o tablă {board_size}x{board_size}. Turul este posibil doar pe table NxN unde N >= 5."
        else:
            return "Da, un Tur al Calului închis este posibil pe majoritatea tablelor de dimensiuni mari, inclusiv pe o tablă 8x8."
