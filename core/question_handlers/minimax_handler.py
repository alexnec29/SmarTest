# core/question_handlers/minimax_handler.py

from typing import Dict, Any, Tuple, List
import random
from ..base_question_handler import BaseQuestionHandler


class MinimaxHandler(BaseQuestionHandler):
    """Handler for Minimax problem questions."""
    
    def generate_minimax_tree(self) -> Dict[str, Any]:
        """Generate a simple minimax tree with 4 leaves."""
        leaf_values = [random.randint(1, 10) for _ in range(4)]
        
        tree_description = (
            "Nivel 0 (Rădăcină - MAX):\n"
            "  - Nod 1 (MIN) are frunzele: A (Valoare: {0}) și B (Valoare: {1})\n"
            "  - Nod 2 (MIN) are frunzele: C (Valoare: {2}) și D (Valoare: {3})"
        ).format(*leaf_values)
        
        return {
            "values": leaf_values,  # [A, B, C, D]
            "description": tree_description
        }
    
    def solve_minimax_alpha_beta(self, leaf_values: List[int]) -> Tuple[int, int]:
        """Calculate root value and visited leaf nodes."""
        A, B, C, D = leaf_values
        
        visited_leaves = 0
        alpha = -float('inf')
        beta = float('inf')
        
        # Calculate Node 1 (MIN)
        val1 = A
        visited_leaves += 1
        beta = min(beta, val1)
        
        val1 = min(val1, B)
        visited_leaves += 1
        beta = min(beta, val1)
        
        result_node1 = val1
        
        # Calculate Node 2 (MIN)
        alpha = max(alpha, result_node1)
        
        val2 = C
        visited_leaves += 1
        
        val2 = min(val2, D)
        visited_leaves += 1
        
        result_node2 = val2
        
        # Root (MAX)
        root_value = max(result_node1, result_node2)
        
        return root_value, visited_leaves
    
    def generate_custom(self, variant: Dict[str, Any], params: Dict[str, Any]) -> Tuple[str, str]:
        """
        Generate Minimax question and answer with computation.
        
        Args:
            variant: Question variant
            params: Parameters (empty for minimax, uses generated tree)
            
        Returns:
            Tuple of (question, answer)
        """
        question_id = variant.get("id", "")
        
        if question_id == "alpha_beta_pruning":
            # Generate a new tree problem
            problem = self.generate_minimax_tree()
            params["tree_description"] = problem["description"]
            
            # Generate question from template
            question = self.format_text(variant.get("question", ""), params)
            
            # Calculate answer
            root_value, visited_leaves = self.solve_minimax_alpha_beta(problem["values"])
            answer = f"Valoarea din rădăcină va fi: {root_value}. Numărul de noduri frunze vizitate va fi: {visited_leaves}."
            
            return question, answer
        else:
            # Fallback to template
            question = self.format_text(variant.get("question", ""), params)
            answer = self.format_text(variant.get("answer", ""), params)
            return question, answer
