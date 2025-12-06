# core/question_types/csp.py

from typing import Dict, Any, List, Tuple
import random

# Ex: Variabile: V1, V2, V3. Domenii: {1, 2, 3}. Constrângeri: V1 != V2, V2 < V3
def generate_csp_problem() -> Dict[str, Any]:
    """ Generează o problemă CSP simplă pentru 3 variabile și 3 valori. """
    variables = ["V1", "V2", "V3"]
    domains = {v: [1, 2, 3] for v in variables}
    
    # Constrângeri binare simple: V1!=V2, V2<V3
    constraints = [
        ("V1", "V2", lambda a, b: a != b),
        ("V2", "V3", lambda a, b: a < b)
    ]
    
    # Asignare parțială aleatorie pentru 1 variabilă (e.g., V1=2)
    partial_assignment = {random.choice(variables): random.choice([1, 2, 3])}
    
    # Asigurăm că asignarea parțială este validă pentru a avea soluții potențiale
    # (Logica simplificată aici pentru a nu complica generarea problemei)
    
    return {
        "variables": variables,
        "domains": domains,
        "constraints": constraints,
        "partial_assignment": partial_assignment,
        "optimization": "Forward Checking (FC)"
    }

def solve_csp_with_fc(problem: Dict[str, Any]) -> str:
    """ Simulează rezolvarea cu Backtracking + Forward Checking (FC). """
    variables = problem["variables"]
    domains = problem["domains"]
    constraints = problem["constraints"]
    
    # Copierea domeniilor pentru a simula FC
    current_domains = {v: list(domains[v]) for v in domains}
    assignment = dict(problem["partial_assignment"])
    
    # Aplica FC inițial pe baza asignării parțiale
    for assigned_var, assigned_val in assignment.items():
        for c_var, d_var, constraint_func in constraints:
            if c_var == assigned_var:
                # Reducere domeniu pentru d_var
                new_domain = [val for val in current_domains[d_var] if constraint_func(assigned_val, val)]
                current_domains[d_var] = new_domain
            elif d_var == assigned_var:
                # Reducere domeniu pentru c_var
                new_domain = [val for val in current_domains[c_var] if constraint_func(val, assigned_val)]
                current_domains[c_var] = new_domain

    # Backtracking simplificat:
    remaining_vars = [v for v in variables if v not in assignment]
    
    # Dacă rămân variabile (simulăm doar primul pas al soluției):
    if remaining_vars:
        next_var = remaining_vars[0] # Selectează prima variabilă rămasă (fără MRV)
        
        for value in current_domains[next_var]:
            # Asignare și testare:
            temp_assignment = assignment.copy()
            temp_assignment[next_var] = value
            
            # Verifică dacă noua asignare parțială este consistentă cu constrângerile inițiale
            is_consistent = True
            for c_var, d_var, constraint_func in constraints:
                val_c = temp_assignment.get(c_var)
                val_d = temp_assignment.get(d_var)
                if val_c is not None and val_d is not None:
                    if not constraint_func(val_c, val_d):
                        is_consistent = False
                        break
            
            if is_consistent:
                # Returnează prima soluție parțială validă (pentru scopul întrebării)
                return f"Asignarea continuă cu: {next_var} = {value}. Asignarea parțială devine: {temp_assignment}"
                
    
    # Fallback
    return f"Nu s-a putut găsi o asignare consistentă pentru continuarea rezolvării, dat fiind {problem['optimization']}."

def generate_question(params: Dict[str, Any] = None) -> str:
    problem = generate_csp_problem()
    
    vars_str = ", ".join(problem["variables"])
    domains_str = ", ".join(f"{v}: {d}" for v, d in problem["domains"].items())
    partial_str = ", ".join(f"{v} = {val}" for v, val in problem["partial_assignment"].items())
    
    constraints_str = "V1 != V2, V2 < V3" 
    
    question = (
        f"Date fiind variabilele ({vars_str}), domeniile ({domains_str}), constrângerile ({constraints_str}) "
        f"și asignarea parțială ({partial_str}), care va fi asignarea variabilei rămase dacă se aplică Backtracking cu optimizarea {problem['optimization']} pentru primul pas?"
    )
    # Stocăm problema în parametri pentru a o putea folosi în generate_answer
    if params is None:
        params = {}
    params["csp_problem"] = problem
    return question

def generate_answer(params: Dict[str, Any] = None) -> str:
    if params and "csp_problem" in params:
        problem = params["csp_problem"]
        return solve_csp_with_fc(problem)
    return "Eroare la generarea răspunsului CSP."