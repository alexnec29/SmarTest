# ui/client.py
# TODO: Implement a minimal CLI interface for testing

import random
from core.question_factory import generate_question_and_answer
from core.evaluator import evaluate_answer


def run_cli():
    # MODIFICARE CRITICĂ: Promptul include acum TOATE subiectele
    topic = input("Enter question type (e.g., n-queens, generalised-hanoi, graph-coloring, knights-tour): ").strip()

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

    elif topic.lower() == "knights-tour": # <-- NOUA LOGICĂ
        ask_type = random.choice(["strategy", "solvability", "complexity"])
        board_size = random.choice([5, 6, 8])
        start_pos = random.choice([(1, 1), (3, 4)])
        params = {"board_size": board_size, "ask_type": ask_type, "start_pos": start_pos}
        print(f"Selected random Knight's Tour question: board_size={board_size}, ask_type={ask_type}")
        question, correct_answer = generate_question_and_answer(topic, params)

    else:
        # Fallback pentru topicuri necunoscute
        question, correct_answer = generate_question_and_answer(topic)

    if not question:
        print("Unknown topic or generation failed.")
        return

    print("Question:", question)
    user_answer = input("Your answer: ")
    score = evaluate_answer(correct_answer, user_answer)

    print(f"Correct answer: {correct_answer}")
    print(f"Your score: {score}%")


# TODO: Add option to run multiple questions / generate PDF later

if __name__ == "__main__":
    run_cli()