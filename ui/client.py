"""
Interfață CLI pentru testarea aplicației.
Actualizat pentru a folosi arhitectura cu clase.
"""

from core.question_factory import create_question, QuestionFactory
from core.evaluator import evaluate_question


def print_separator(char="=", length=70):
    """Helper pentru afișare separatori."""
    print(char * length)


def run_cli():
    """Rulează interfața CLI interactivă."""
    print_separator()
    print("🎓 SmarTest - Sistem de generare și evaluare întrebări AI")
    print_separator()

    # Afișează tipurile disponibile
    available_types = QuestionFactory.get_available_types()
    print(f"\nTipuri de întrebări disponibile: {', '.join(available_types)}")

    while True:
        print("\n" + "─" * 70)

        # Selectează tipul întrebării
        topic = input(f"\nIntroduceți tipul întrebării ({', '.join(available_types)}) sau 'exit': ").strip()

        if topic.lower() == 'exit':
            print("\n👋 La revedere!")
            break

        if topic.lower() not in available_types:
            print(f"❌ Tip necunoscut! Alegeți din: {', '.join(available_types)}")
            continue

        # Selectează dificultatea
        difficulty = input("Dificultate (easy/medium/hard) [medium]: ").strip() or "medium"
        if difficulty not in ["easy", "medium", "hard"]:
            print("⚠️ Dificultate invalidă, folosim 'medium'")
            difficulty = "medium"

        # Generează întrebarea
        print("\n🔄 Generez întrebare...")
        question = create_question(topic, difficulty)

        if not question:
            print("❌ Eroare la generarea întrebării!")
            continue

        # Afișează întrebarea
        print_separator("─")
        print("📝 ÎNTREBARE:")
        print_separator("─")
        print(question.get_question())

        # Afișează parametrii (pentru debugging)
        print(f"\n[Debug] Parametri generați: {question.params}")

        # Opțiune: afișare răspuns corect imediat (pentru testare)
        show_answer = input("\n❓ Doriți să vedeți răspunsul corect înainte? (da/nu) [nu]: ").strip().lower()
        if show_answer in ['da', 'yes', 'y']:
            print_separator("─")
            print("✅ RĂSPUNS CORECT:")
            print_separator("─")
            print(question.get_answer(detailed=False))

            show_detailed = input("\nDoriți răspunsul detaliat? (da/nu) [nu]: ").strip().lower()
            if show_detailed in ['da', 'yes', 'y']:
                print("\n📚 RĂSPUNS DETALIAT:")
                print_separator("─")
                print(question.get_answer(detailed=True))

            continue  # Sari peste evaluare

        # Citește răspunsul utilizatorului
        print_separator("─")
        print("✏️ Introduceți răspunsul dvs.:")
        print("(Lăsați gol și apăsați Enter de 2 ori pentru a termina)")
        print_separator("─")

        user_lines = []
        empty_count = 0
        while empty_count < 2:
            line = input()
            if not line.strip():
                empty_count += 1
            else:
                empty_count = 0
                user_lines.append(line)

        user_answer = " ".join(user_lines).strip()

        if not user_answer:
            print("⚠️ Răspuns gol, trecem la întrebarea următoare.")
            continue

        # Evaluează răspunsul
        print("\n🔍 Evaluez răspunsul...")
        result = evaluate_question(question, user_answer, fuzzy=True)

        # Afișează rezultatele
        print_separator("=")
        print("📊 REZULTATE EVALUARE")
        print_separator("=")

        # Scor cu emoji
        score = result['score']
        if score >= 90:
            emoji = "🌟"
        elif score >= 70:
            emoji = "✅"
        elif score >= 50:
            emoji = "⚠️"
        else:
            emoji = "❌"

        print(f"\n{emoji} SCOR: {score}%")
        print(f"\n💬 FEEDBACK: {result['feedback']}")

        # Afișează detalii
        if 'details' in result and result['details']:
            details = result['details']

            if 'found_keywords' in details and details['found_keywords']:
                print(f"\n✓ Keywords găsite: {', '.join(details['found_keywords'])}")

            if 'missing_keywords' in details and details['missing_keywords']:
                print(f"\n✗ Keywords lipsă: {', '.join(details['missing_keywords'])}")

            if 'partial_matches' in details and details['partial_matches']:
                print("\n≈ Potriviri parțiale:")
                for kw, sim in details['partial_matches']:
                    print(f"  • {kw} (similaritate: {sim:.0%})")

        # Afișează răspunsul corect
        print_separator("─")
        print("✅ RĂSPUNS CORECT:")
        print_separator("─")
        print(result['correct_answer'])

        # Opțiune pentru răspuns detaliat
        show_detailed = input("\n📚 Doriți să vedeți răspunsul detaliat? (da/nu) [da]: ").strip().lower()
        if show_detailed not in ['nu', 'no', 'n']:
            print_separator("─")
            print("📖 RĂSPUNS DETALIAT:")
            print_separator("─")
            print(result['detailed_answer'])

        # Întrebare nouă?
        continue_quiz = input("\n🔄 Încercați altă întrebare? (da/nu) [da]: ").strip().lower()
        if continue_quiz in ['nu', 'no', 'n', 'exit']:
            print("\n👋 La revedere!")
            break


def run_batch_mode(count: int = 5, topic: str = "n-queens", difficulty: str = "medium"):
    """
    Mod batch: generează mai multe întrebări dintr-o dată.
    Util pentru testare.

    Args:
        count: Număr de întrebări de generat
        topic: Tipul întrebării
        difficulty: Dificultatea
    """
    print_separator()
    print(f"📦 BATCH MODE - Generare {count} întrebări")
    print_separator()

    questions = []
    for i in range(count):
        q = create_question(topic, difficulty)
        if q:
            questions.append(q)
            print(f"✓ Întrebarea {i + 1} generată (n={q.params.get('n', 'N/A')})")

    print(f"\n✅ {len(questions)} întrebări generate cu succes!")

    # Opțional: salvează în JSON
    save = input("\n💾 Salvați întrebările în JSON? (da/nu) [nu]: ").strip().lower()
    if save in ['da', 'yes', 'y']:
        import json
        data = [q.to_dict() for q in questions]

        filename = f"questions_{topic}_{difficulty}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✅ Salvat în '{filename}'")


if __name__ == "__main__":
    import sys

    # Suport pentru argumente CLI
    if len(sys.argv) > 1:
        if sys.argv[1] == "batch":
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            topic = sys.argv[3] if len(sys.argv) > 3 else "n-queens"
            difficulty = sys.argv[4] if len(sys.argv) > 4 else "medium"
            run_batch_mode(count, topic, difficulty)
        else:
            print("Utilizare: python client.py [batch <count> <topic> <difficulty>]")
    else:
        run_cli()