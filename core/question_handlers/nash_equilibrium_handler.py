# core/question_handlers/nash_equilibrium_handler.py

from typing import Dict, Any, Tuple
from ..base_question_handler import BaseQuestionHandler


class NashEquilibriumHandler(BaseQuestionHandler):
    """Handler for Nash Equilibrium problem questions."""
    
    def generate_custom(self, variant: Dict[str, Any], params: Dict[str, Any]) -> Tuple[str, str]:
        """
        Generate Nash Equilibrium question and answer with computation.
        
        Args:
            variant: Question variant
            params: Parameters (empty for nash, uses static example)
            
        Returns:
            Tuple of (question, answer)
        """
        question_id = variant.get("id", "")
        
        if question_id == "nash_equilibrium_dynamic":
            # For now, use the static example from the template
            # In the future, we could generate random game matrices
            question = (
                "Pentru jocul dat în forma normală (matricea atașată), există echilibru Nash pur? Care este acesta?\n\n"
                "Matricea jocului (Jucătorul 1 alege rândul, Jucătorul 2 alege coloana):\n"
                "Format (Recompensă J1, Recompensă J2)\n\n"
                "        Jucătorul 2\n"
                "          Stânga   Dreapta\n"
                "Jucătorul 1\n"
                "    Sus     (1, 2)    (0, 1)\n"
                "    Jos     (2, 1)    (1, 0)"
            )
            
            # Calculate Nash equilibrium
            # (Jos, Stânga) is the equilibrium because:
            # - If J1 chooses 'Jos', J2 prefers 'Stânga' (gets 1 vs 0)
            # - If J2 chooses 'Stânga', J1 prefers 'Jos' (gets 2 vs 1)
            answer = "Da, există un echilibru Nash pur. Acesta este (Jos, Stânga)."
            
            return question, answer
        else:
            # Fallback to template
            question = self.format_text(variant.get("question", ""), params)
            answer = self.format_text(variant.get("answer", ""), params)
            return question, answer
