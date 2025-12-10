# ui/client.py

import random
from core.question_factory import generate_question_and_answer
from core.evaluator import evaluate_answer


def run_cli():
    """
    Run the CLI interface for the question generation system.
    
    The new simplified version uses the handler-based system which
    automatically selects and generates questions from JSON templates.
    """
    topic = input("Enter question type (e.g., n-queens, generalised-hanoi, graph-coloring, knights-tour, nash-equilibrium, csp, minimax): ").strip()
    
    # The new system handles everything automatically
    # We just pass empty params and let the handlers select random variants
    question, correct_answer = generate_question_and_answer(topic, params={})
    
    if not question:
        print("Unknown topic or generation failed.")
        return
    
    print("\n--- ÎNTREBARE ---")
    print(question)
    print("-----------------\n")
    
    user_answer = input("Răspunsul tău: ")
    
    # Evaluate the answer
    score = evaluate_answer(correct_answer, user_answer)
    
    print(f"\n--- EVALUARE ---")
    print(f"Răspuns corect: {correct_answer}")
    print(f"Scorul tău: {score}%")
    print("----------------\n")


if __name__ == "__main__":
    run_cli()
