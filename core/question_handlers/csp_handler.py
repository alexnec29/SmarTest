# core/question_handlers/csp_handler.py

from typing import Dict, Any, Tuple, List
import random
from ..base_question_handler import BaseQuestionHandler


class CSPHandler(BaseQuestionHandler):
    """Handler for CSP (Constraint Satisfaction Problem) questions."""
    
    def generate_csp_problem(self) -> Dict[str, Any]:
        """Generate a simple CSP problem with 3 variables and 3 values."""
        variables = ["V1", "V2", "V3"]
        domains = {v: [1, 2, 3] for v in variables}
        constraints = [
            ("V1", "V2", lambda a, b: a != b),
            ("V2", "V3", lambda a, b: a < b)
        ]
        
        # Generate a valid partial assignment
        # Choose one variable and a value that won't immediately violate constraints
        chosen_var = random.choice(["V1", "V3"])  # Avoid V2 as it's constrained by both
        if chosen_var == "V1":
            # V1 can be any value (V2 will be constrained to != V1)
            chosen_val = random.choice([1, 2, 3])
        else:  # V3
            # V3 should be >= 2 to allow V2 < V3
            chosen_val = random.choice([2, 3])
        
        partial_assignment = {chosen_var: chosen_val}
        
        return {
            "variables": variables,
            "domains": domains,
            "constraints": constraints,
            "partial_assignment": partial_assignment,
            "optimization": "Forward Checking (FC)"
        }
    
    def solve_csp_with_fc(self, problem: Dict[str, Any]) -> str:
        """Apply Forward Checking to the CSP problem and return the first valid step."""
        variables = problem["variables"]
        domains = problem["domains"]
        constraints = problem["constraints"]
        current_domains = {v: list(domains[v]) for v in domains}
        assignment = dict(problem["partial_assignment"])
        
        # Apply Forward Checking on partial assignment
        for assigned_var, assigned_val in assignment.items():
            for c_var, d_var, constraint_func in constraints:
                if c_var == assigned_var:
                    current_domains[d_var] = [val for val in current_domains[d_var] if constraint_func(assigned_val, val)]
                elif d_var == assigned_var:
                    current_domains[c_var] = [val for val in current_domains[c_var] if constraint_func(val, assigned_val)]
        
        # Select remaining variable
        remaining_vars = [v for v in variables if v not in assignment]
        if remaining_vars:
            next_var = remaining_vars[0]
            for value in current_domains[next_var]:
                temp_assignment = assignment.copy()
                temp_assignment[next_var] = value
                
                # Check consistency with constraints
                is_consistent = True
                for c_var, d_var, constraint_func in constraints:
                    val_c = temp_assignment.get(c_var)
                    val_d = temp_assignment.get(d_var)
                    if val_c is not None and val_d is not None and not constraint_func(val_c, val_d):
                        is_consistent = False
                        break
                
                if is_consistent:
                    return f"{next_var} = {value}, asignare parțială: {temp_assignment}"
        
        return "Nu există o asignare consistentă pentru pasul următor."
    
    def generate_custom(self, variant: Dict[str, Any], params: Dict[str, Any]) -> Tuple[str, str]:
        """
        Generate CSP question and answer with computation.
        
        Args:
            variant: Question variant
            params: Parameters (will be populated with CSP problem)
            
        Returns:
            Tuple of (question, answer)
        """
        question_id = variant.get("id", "")
        
        if question_id == "csp_forward_checking":
            # Generate CSP problem
            problem = self.generate_csp_problem()
            
            # Build replacements for template
            params["variables"] = ", ".join(problem["variables"])
            params["domains"] = str(problem["domains"])
            params["constraints"] = "V1 != V2, V2 < V3"
            params["partial_assignment"] = str(problem["partial_assignment"])
            params["optimization"] = problem["optimization"]
            
            # Calculate answer
            fc_result = self.solve_csp_with_fc(problem)
            params["fc_result"] = fc_result
            
            # Generate question and answer from template
            question = self.format_text(variant.get("question", ""), params)
            answer = self.format_text(variant.get("answer", ""), params)
            
            return question, answer
        else:
            # Fallback to template
            question = self.format_text(variant.get("question", ""), params)
            answer = self.format_text(variant.get("answer", ""), params)
            return question, answer
