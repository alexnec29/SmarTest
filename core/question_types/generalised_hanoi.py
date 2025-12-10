# core/question_types/generalised_hanoi.py
# Am creat subdirectorul "question_types" pentru a urmări structura

def generate_question(n_discs: int = 3, n_pegs: int = 3, ask_type: str = "moves_strategy") -> str:
    """
    Generează întrebarea pentru problema Turnurilor Hanoi Generalizate (n discuri, m bețe).
    n_pegs trebuie să fie >= 3.
    ask_type poate fi: "moves_strategy", "min_moves", "complexity"
    """
    if ask_type == "moves_strategy":
        return f"Problem Generalised Hanoi ({n_discs} discs, {n_pegs} pegs): What is the minimum number of moves required to transfer all discs from the start peg to the end peg?"
    elif ask_type == "min_moves":
        return f"Problem Generalised Hanoi ({n_discs} discs, {n_pegs} pegs): What is the *exact* minimum number of moves required?"
    elif ask_type == "complexity":
        return f"Problem Generalised Hanoi ({n_discs} discs, {n_pegs} pegs): What is the time complexity of the optimal algorithm in terms of n_discs (n)?"
    else:
        return f"Problem Generalised Hanoi ({n_discs} discs, {n_pegs} pegs): What is the minimum number of moves required to transfer all discs from the start peg to the end peg?"

def generate_answer(n_discs: int = 3, n_pegs: int = 3, ask_type: str = "moves_strategy") -> str:
    """
    Generează răspunsul pentru problema Turnurilor Hanoi Generalizate.
    Notă: Formula generală pentru k bețe și n discuri este complexă.
    Vom da răspunsuri exacte pentru cazuri simple (n=3, 4 discuri) și formula generală.
    """
    if ask_type == "moves_strategy":
        return "The minimum number of moves is an open problem for the general case (n_pegs > 3). The optimal solution is generally found using a recursive approach (Frame-Stewart algorithm or similar) which minimizes the total number of transfers."
    elif ask_type == "min_moves":
        if n_pegs == 3:
            # Standard Hanoi: 2^n - 1
            moves = (2 ** n_discs) - 1
            return f"For 3 pegs, the minimum number of moves is $2^{{{n_discs}}} - 1$, which is {moves}."
        elif n_pegs == 4 and n_discs == 4:
            # Caz cunoscut (Frame-Stewart)
            return "For 4 discs and 4 pegs, the minimum is 9 moves (using Frame-Stewart algorithm)."
        else:
            return f"The exact minimum number of moves for {n_discs} discs and {n_pegs} pegs is difficult to compute and generally requires dynamic programming or a specialized solver. It is a value $M(n,k)$ where $M(n,3) = 2^n - 1$."
    elif ask_type == "complexity":
        if n_pegs == 3:
            return "The time complexity for 3 pegs is $O(2^n)$, where n is the number of discs."
        else:
            return "The time complexity for $k>3$ pegs is approximately $O((\\sqrt[k-2]{2})^n)$ based on the Frame-Stewart conjecture/algorithm, which is still exponential but better than $O(2^n)$."
    else:
        return "The minimum number of moves is an open problem for the general case (n_pegs > 3). The optimal solution is generally found using a recursive approach (Frame-Stewart algorithm or similar) which minimizes the total number of transfers."