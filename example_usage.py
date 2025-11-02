"""
Exemplu de utilizare a sistemului cu clase.
Demonstrează cum întrebarea și răspunsul sunt legate automat!
"""

from core.question_factory import create_question, QuestionFactory
from core.evaluator import evaluate_question


def demo_basic_usage():
    """Demonstrează utilizarea de bază."""
    print("=" * 70)
    print("DEMO 1: Utilizare de bază")
    print("=" * 70)

    # Creează o întrebare (parametrii sunt generați automat!)
    question = create_question("n-queens", difficulty="medium")

    # Afișează întrebarea
    print("\nÎNTREBARE:")
    print(question.get_question())

    # Afișează răspunsul punctual
    print("\n" + "-" * 70)
    print("RĂSPUNS PUNCTUAL:")
    print(question.get_answer(detailed=False))

    # Afișează răspunsul detaliat
    print("\n" + "-" * 70)
    print("RĂSPUNS DETALIAT:")
    print(question.get_answer(detailed=True))

    # Evaluează un răspuns de la utilizator
    print("\n" + "-" * 70)
    print("EVALUARE RĂSPUNS UTILIZATOR:")

    user_answer = "Backtracking with Forward Checking"  # Exemplu răspuns
    result = evaluate_question(question, user_answer)

    print(f"\nRăspuns utilizator: {user_answer}")
    print(f"Scor: {result['score']}%")
    print(f"Feedback: {result['feedback']}")
    print(f"Răspuns corect: {result['correct_answer']}")


def demo_multiple_questions():
    """Demonstrează generarea mai multor întrebări."""
    print("\n\n" + "=" * 70)
    print("DEMO 2: Generarea mai multor întrebări")
    print("=" * 70)

    for i in range(3):
        print(f"\n--- Întrebarea {i + 1} ---")

        # Fiecare întrebare are parametri diferiți!
        q = create_question("n-queens", "medium")

        print(f"Parametri generați: {q.params}")
        print(f"Întrebare: {q.get_question()[:100]}...")
        print(f"Răspuns: {q.get_answer()}")


def demo_different_difficulties():
    """Demonstrează dificultăți diferite."""
    print("\n\n" + "=" * 70)
    print("DEMO 3: Dificultăți diferite")
    print("=" * 70)

    for difficulty in ["easy", "medium", "hard"]:
        print(f"\n--- Dificultate: {difficulty.upper()} ---")

        q = create_question("n-queens", difficulty)

        print(f"n = {q.params['n']}")
        print(f"Răspuns: {q.get_answer()}")
        print(f"Keywords: {q.get_keywords()}")


def demo_export_to_dict():
    """Demonstrează exportul ca dicționar (pentru JSON/PDF)."""
    print("\n\n" + "=" * 70)
    print("DEMO 4: Export ca dicționar")
    print("=" * 70)

    q = create_question("n-queens", "hard")
    data = q.to_dict()

    import json
    print("\nJSON export:")
    print(json.dumps(data, indent=2, ensure_ascii=False))


def demo_evaluation_accuracy():
    """Demonstrează precizia evaluării."""
    print("\n\n" + "=" * 70)
    print("DEMO 5: Precizie evaluare")
    print("=" * 70)

    q = create_question("n-queens", "medium")
    correct = q.get_answer()

    print(f"Răspuns corect: {correct}")
    print("\nTestare variante de răspuns:\n")

    test_answers = [
        correct,  # Răspuns perfect
        "Backtracking with FC",  # Sinonime
        "Backtraking",  # Greșeală de scriere
        "Forward Checking",  # Parțial corect
        "Dynamic Programming",  # Complet greșit
        "",  # Gol
    ]

    for answer in test_answers:
        result = evaluate_question(q, answer)
        print(f"'{answer[:30]}...' → Scor: {result['score']}% - {result['feedback']}")


def demo_available_types():
    """Afișează tipurile de întrebări disponibile."""
    print("\n\n" + "=" * 70)
    print("DEMO 6: Tipuri disponibile")
    print("=" * 70)

    types = QuestionFactory.get_available_types()
    print(f"\nTipuri de întrebări disponibile: {types}")
    print("\nPentru a adăuga un nou tip:")
    print("1. Creați o clasă care moștenește QuestionBase")
    print("2. Implementați metodele abstracte")
    print("3. Înregistrați: QuestionFactory.register('nume', ClasaVoastra)")


if __name__ == "__main__":
    # Rulează toate demo-urile
    demo_basic_usage()
    demo_multiple_questions()
    demo_different_difficulties()
    demo_export_to_dict()
    demo_evaluation_accuracy()
    demo_available_types()

    print("\n\n" + "=" * 70)
    print("✅ Demo complet! Acum înțelegi cum funcționează sistemul!")
    print("=" * 70)