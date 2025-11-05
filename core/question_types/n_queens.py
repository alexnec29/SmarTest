# TODO: Implement question generation for n-Queens
def generate_question(n: int = 8, ask_type: str = "strategy") -> str:
    """
    Generează întrebarea pentru n-Queens.
    ask_type poate fi: "strategy", "num_solutions", "first_solution_example"
    """
    if ask_type == "strategy":
        return f"Problem {n}-Queens: What is the most suitable solving strategy?"
    elif ask_type == "num_solutions":
        return f"Problem {n}-Queens: How many distinct solutions exist?"
    elif ask_type == "first_solution_example":
        return f"Problem {n}-Queens: Provide one valid arrangement (column indices per row)."
    else:
        return f"Problem {n}-Queens: What is the most suitable solving strategy?"


def generate_answer(n: int = 8, ask_type: str = "strategy") -> str:
    """
    Generează răspunsul pentru întrebarea n-Queens.
    Răspunsuri pentru câteva valori comune; pentru altele recomand un solver.
    """
    if ask_type == "strategy":
        return f"Backtracking is the most suitable strategy for {n}-Queens."
    elif ask_type == "num_solutions":
        if n == 8:
            return "There are 92 distinct solutions for the 8-Queens problem."
        elif n == 4:
            return "There are 2 distinct solutions for the 4-Queens problem."
        else:
            return f"Counting all solutions for n={n} may be expensive; implement a solver to compute exact count."
    elif ask_type == "first_solution_example":
        if n == 8:
            return "One valid arrangement is: [0, 4, 7, 5, 2, 6, 1, 3]"
        elif n == 4:
            return "One valid arrangement is: [1, 3, 0, 2]"
        else:
            return "Provide a valid arrangement as a list of column indices per row."
    else:
        return f"Backtracking is the most suitable strategy for {n}-Queens."