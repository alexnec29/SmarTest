# TODO: Implement a minimal CLI interface for testing

from core.question_factory import generate_question_and_answer
from core.evaluator import evaluate_answer


def run_cli():
    topic = input("Enter question type (e.g., n-queens): ")
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
