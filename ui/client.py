# ui/client.py
# TODO: Implement a minimal CLI interface for testing

import random
from core.question_factory import generate_question_and_answer
from core.evaluator import evaluate_answer


def run_cli():
    # MODIFICARE CRITICĂ: Promptul include acum TOATE subiectele
    topic = input("Enter question type (e.g., n-queens, generalised-hanoi, graph-coloring, knights-tour, nash-equilibrium, csp, minimax): ").strip()

    params = {} # Inițializăm un dicționar gol pentru parametri

    if topic.lower() == "n-queens":
        ask_type = random.choice(["strategy", "num_solutions", "first_solution_example"])
        n = random.choice([4, 8, 10])
        params = {"n": n, "ask_type": ask_type}
        print(f"Selected random n-Queens question: ask_type={ask_type}, n={n}")
        question, correct_answer = generate_question_and_answer(topic, params)

    elif topic.lower() == "generalised-hanoi":
        ask_type = random.choice(["moves_strategy", "min_moves", "complexity"])
        n_discs = random.choice([3, 4])
        n_pegs = random.choice([3, 4])
        params = {"n_discs": n_discs, "n_pegs": n_pegs, "ask_type": ask_type}
        print(f"Selected random Generalised Hanoi question: ask_type={ask_type}, n_discs={n_discs}, n_pegs={n_pegs}")
        question, correct_answer = generate_question_and_answer(topic, params)
        
    elif topic.lower() == "graph-coloring":
        ask_type = random.choice(["chromatic_number", "is_k_colorable", "strategy"])
        graph_id = random.choice(["k4", "wheel5"])
        k_colors = random.choice([2, 3, 4])
        params = {"graph_id": graph_id, "ask_type": ask_type, "k_colors": k_colors}
        print(f"Selected random Graph Coloring question: graph_id={graph_id}, ask_type={ask_type}, k_colors={k_colors}")
        question, correct_answer = generate_question_and_answer(topic, params)

    elif topic.lower() == "knights-tour": 
        ask_type = random.choice(["strategy", "solvability", "complexity"])
        board_size = random.choice([5, 6, 8])
        start_pos = random.choice([(1, 1), (3, 4)])
        params = {"board_size": board_size, "ask_type": ask_type, "start_pos": start_pos}
        print(f"Selected random Knight's Tour question: board_size={board_size}, ask_type={ask_type}")
        question, correct_answer = generate_question_and_answer(topic, params)

    elif topic.lower() == "nash-equilibrium": # <--- LOGICA NOUĂ (Dinamizat în modulul său)
        print("Selected Nash Equilibrium question (dynamic matrix).")
        # generate_question_and_answer va genera o matrice nouă și răspunsul corect la fiecare rulare
        question, correct_answer = generate_question_and_answer(topic)
        
    elif topic.lower() == "csp": # <--- LOGICA NOUĂ (Satisfacerea Constrângerilor)
        # params este pasat prin funcție, iar modulul CSP îl populează cu problema
        print("Selected Constraint Satisfaction Problem (CSP) question.")
        question, correct_answer = generate_question_and_answer(topic, params)
        
    elif topic.lower() == "minimax": # <--- LOGICA NOUĂ (Minimax/Alpha-Beta)
        # params este pasat prin funcție, iar modulul Minimax îl populează cu arborele
        print("Selected Minimax/Alpha-Beta Pruning question.")
        question, correct_answer = generate_question_and_answer(topic, params)

    else:
        # Fallback pentru topicuri necunoscute
        print(f"Selected generic topic: {topic}")
        question, correct_answer = generate_question_and_answer(topic)

    if not question:
        print("Unknown topic or generation failed.")
        return

    print("\n--- ÎNTREBARE ---")
    print(question)
    print("-----------------\n")
    user_answer = input("Răspunsul tău: ")
    
    # Notă: Dacă utilizați noile tipuri (CSP, Minimax), 
    # asigurați-vă că 'params' este inclus în apelul generatorului de întrebări 
    # pentru ca răspunsul corect să fie calculat corect (logica este gestionată în factory.py)
    
    # Reapelăm generate_question_and_answer pentru a ne asigura că folosim aceiași parametri 
    # stocați în timpul generării întrebării (utile pentru CSP/Minimax)
    
    _, correct_answer_for_eval = generate_question_and_answer(topic, params)
    
    score = evaluate_answer(correct_answer_for_eval, user_answer)

    print(f"\n--- EVALUARE ---")
    print(f"Răspuns corect: {correct_answer_for_eval}")
    print(f"Scorul tău: {score}%")
    print("----------------\n")


# TODO: Add option to run multiple questions / generate PDF later

if __name__ == "__main__":
    run_cli()