# TODO: Implement a minimal CLI interface for testing

import random
from core.question_factory import generate_question_and_answer
from core.evaluator import evaluate_answer


def run_cli():
    topic = input("Enter question type (e.g., n-queens, generalised-hanoi): ").strip() # <--- MODIFICARE AICI
    if topic.lower() == "n-queens":
        ask_type = random.choice(["strategy", "num_solutions", "first_solution_example"])
        n=random.choice([4,8,10])
        params = {"n": n, "ask_type": ask_type}
        print(f"Selected random n-Queens question: ask_type={ask_type}, n={n}")
        question, correct_answer = generate_question_and_answer(topic, params)
    elif topic.lower() == "generalised-hanoi": # <--- ADAUGĂ ACEST BLOC
        ask_type = random.choice(["moves_strategy", "min_moves", "complexity"])
        n_discs=random.choice([3, 4])
        n_pegs=random.choice([3, 4])
        params = {"n_discs": n_discs, "n_pegs": n_pegs, "ask_type": ask_type}
        print(f"Selected random Generalised Hanoi question: ask_type={ask_type}, n_discs={n_discs}, n_pegs={n_pegs}")
        question, correct_answer = generate_question_and_answer(topic, params)
    else:
        question, correct_answer = generate_question_and_answer(topic)

    if not question:
        print("Unknown topic.")
        return

    print("Question:", question)
    user_answer = input("Your answer: ")
    score = evaluate_answer(correct_answer, user_answer)

    print(f"Correct answer: {correct_answer}")
    print(f"Your score: {score}%")


# TODO: Add option to run multiple questions / generate PDF later

if __name__ == "__main__":
    run_cli()
