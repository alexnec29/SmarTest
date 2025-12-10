from typing import Dict, Any
import random
import json
import os

# Calea către folderul cu template-uri
TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "templates")
TEMPLATE_FILE = "csp.json"

def load_template() -> Dict[str, Any]:
    """Încarcă template-ul JSON pentru CSP."""
    template_path = os.path.join(TEMPLATES_PATH, TEMPLATE_FILE)
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template-ul JSON nu a fost găsit: {template_path}")
    with open(template_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_csp_problem() -> Dict[str, Any]:
    """Generează o problemă CSP simplă cu 3 variabile și 3 valori."""
    variables = ["V1", "V2", "V3"]
    domains = {v: [1, 2, 3] for v in variables}
    constraints = [
        ("V1", "V2", lambda a, b: a != b),
        ("V2", "V3", lambda a, b: a < b)
    ]
    partial_assignment = {random.choice(variables): random.choice([1, 2, 3])}
    return {
        "variables": variables,
        "domains": domains,
        "constraints": constraints,
        "partial_assignment": partial_assignment,
        "optimization": "Forward Checking (FC)"
    }

def solve_csp_with_fc(problem: Dict[str, Any]) -> str:
    """Aplică Forward Checking pe problema CSP și returnează primul pas valid."""
    variables = problem["variables"]
    domains = problem["domains"]
    constraints = problem["constraints"]
    current_domains = {v: list(domains[v]) for v in domains}
    assignment = dict(problem["partial_assignment"])

    # Aplicare Forward Checking pe asignarea parțială
    for assigned_var, assigned_val in assignment.items():
        for c_var, d_var, constraint_func in constraints:
            if c_var == assigned_var:
                current_domains[d_var] = [val for val in current_domains[d_var] if constraint_func(assigned_val, val)]
            elif d_var == assigned_var:
                current_domains[c_var] = [val for val in current_domains[c_var] if constraint_func(val, assigned_val)]

    # Selectare variabilă rămasă
    remaining_vars = [v for v in variables if v not in assignment]
    if remaining_vars:
        next_var = remaining_vars[0]
        for value in current_domains[next_var]:
            temp_assignment = assignment.copy()
            temp_assignment[next_var] = value

            # Verifică consistența cu constrângerile
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

def generate_question(params: Dict[str, Any] = None) -> str:
    """Generează o întrebare din template-ul JSON, cu valori dinamice pentru variabile și domenii."""
    template = load_template()
    problem = generate_csp_problem()

    # Construim înlocuirile pentru template
    replacements = {
        "variables": ", ".join(problem["variables"]),
        "domains": str(problem["domains"]),
        "constraints": "V1 != V2, V2 < V3",
        "partial_assignment": str(problem["partial_assignment"]),
        "optimization": problem["optimization"]
    }

    # Păstrăm problema în params pentru a fi folosită în generate_answer
    if params is not None:
        params["csp_problem"] = problem

    return template["question"].format(**replacements)


def generate_answer(params: Dict[str, Any] = None) -> str:
    template = load_template()

    # Dacă nu există problemă CSP în params, generăm una
    if params is None:
        params = {}
    if "csp_problem" not in params:
        params["csp_problem"] = generate_csp_problem()

    # Calculăm răspunsul dinamic
    result = solve_csp_with_fc(params["csp_problem"])

    return template["answer"].format(fc_result=result)

