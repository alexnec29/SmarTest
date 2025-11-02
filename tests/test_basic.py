"""
Teste unitare pentru funcționalitățile de bază.
Rulare: python -m pytest tests/test_basic.py -v
Sau: python tests/test_basic.py (fără pytest)
"""

import sys
import os

# Adaugă directorul părinte la path pentru import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.question_factory import create_question, QuestionFactory
from core.evaluator import evaluate_question
from core.question_types.n_queens import NQueensQuestion


class TestQuestionGeneration:
    """Teste pentru generarea întrebărilor."""

    def test_question_creation(self):
        """Test: Întrebarea se creează corect."""
        q = create_question("n-queens", "medium")
        assert q is not None, "Întrebarea ar trebui să fie creată"
        assert q.question_text is not None, "Textul întrebării ar trebui să existe"
        assert q.correct_answer is not None, "Răspunsul corect ar trebui să existe"
        print("✓ Test question_creation passed")

    def test_parameters_generated(self):
        """Test: Parametrii sunt generați corect."""
        q = create_question("n-queens", "hard")
        assert "n" in q.params, "Parametrul 'n' ar trebui să existe"
        assert q.params["n"] in [10, 12, 15], "n ar trebui să fie 10, 12 sau 15 pentru 'hard'"
        print(f"✓ Test parameters_generated passed (n={q.params['n']})")

    def test_difficulty_levels(self):
        """Test: Dificultățile generează valori diferite pentru n."""
        easy = create_question("n-queens", "easy")
        medium = create_question("n-queens", "medium")
        hard = create_question("n-queens", "hard")

        assert easy.params["n"] in [4, 5], f"Easy: n={easy.params['n']} ar trebui să fie 4 sau 5"
        assert medium.params["n"] in [6, 7, 8], f"Medium: n={medium.params['n']} ar trebui să fie 6-8"
        assert hard.params["n"] in [10, 12, 15], f"Hard: n={hard.params['n']} ar trebui să fie 10-15"
        print("✓ Test difficulty_levels passed")

    def test_answer_consistency(self):
        """Test: Răspunsul este consistent cu parametrii întrebării."""
        q = NQueensQuestion("medium")
        q.params = {"n": 8, "problems": [], "main_problem": "n-queens"}

        answer1 = q.generate_correct_answer()
        answer2 = q.generate_correct_answer()

        assert answer1 == answer2, "Răspunsurile ar trebui să fie identice pentru aceiași parametri"
        assert "Backtracking" in answer1, f"Răspunsul pentru n=8 ar trebui să conțină 'Backtracking', nu '{answer1}'"
        print("✓ Test answer_consistency passed")

    def test_detailed_answer_generation(self):
        """Test: Răspunsul detaliat este mai lung decât cel punctual."""
        q = create_question("n-queens", "medium")

        short = q.get_answer(detailed=False)
        detailed = q.get_answer(detailed=True)

        assert len(detailed) > len(short), "Răspunsul detaliat ar trebui să fie mai lung"
        assert "RĂSPUNS DETALIAT" in detailed, "Răspunsul detaliat ar trebui să aibă header"
        print("✓ Test detailed_answer_generation passed")

    def test_keywords_generation(self):
        """Test: Keywords sunt generate corect."""
        q = create_question("n-queens", "easy")
        keywords = q.get_keywords()

        assert "backtracking" in keywords, "Keywords ar trebui să conțină 'backtracking'"
        assert "n-queens" in keywords, "Keywords ar trebui să conțină 'n-queens'"
        print(f"✓ Test keywords_generation passed (keywords={keywords})")


class TestEvaluation:
    """Teste pentru evaluarea răspunsurilor."""

    def test_perfect_answer(self):
        """Test: Răspuns perfect primește scor maxim."""
        q = create_question("n-queens", "medium")
        result = evaluate_question(q, q.correct_answer)

        assert result["score"] >= 95, f"Răspuns perfect ar trebui să primească ≥95%, nu {result['score']}%"
        print(f"✓ Test perfect_answer passed (score={result['score']}%)")

    def test_fuzzy_matching(self):
        """Test: Fuzzy matching funcționează pentru greșeli de scriere."""
        q = NQueensQuestion("medium")
        q.params = {"n": 8, "problems": [], "main_problem": "n-queens"}
        q.create()

        # "Backtraking" în loc de "Backtracking"
        result = evaluate_question(q, "Backtraking")

        assert result["score"] > 50, f"Fuzzy matching ar trebui să detecteze similaritatea (score={result['score']}%)"
        print(f"✓ Test fuzzy_matching passed (score={result['score']}%)")

    def test_wrong_answer(self):
        """Test: Răspuns greșit primește scor mic."""
        q = create_question("n-queens", "medium")
        result = evaluate_question(q, "Dynamic Programming")

        assert result["score"] < 30, f"Răspuns greșit ar trebui să primească <30%, nu {result['score']}%"
        print(f"✓ Test wrong_answer passed (score={result['score']}%)")

    def test_empty_answer(self):
        """Test: Răspuns gol primește scor 0."""
        q = create_question("n-queens", "medium")
        result = evaluate_question(q, "")

        assert result["score"] == 0, f"Răspuns gol ar trebui să primească 0%, nu {result['score']}%"
        print("✓ Test empty_answer passed")

    def test_partial_answer(self):
        """Test: Răspuns parțial primește scor parțial."""
        q = NQueensQuestion("medium")
        q.params = {"n": 10, "problems": [], "main_problem": "n-queens"}
        q.create()

        # Răspuns parțial: "Forward Checking" (lipsește "Backtracking")
        result = evaluate_question(q, "Forward Checking")

        assert 20 < result["score"] < 80, f"Răspuns parțial ar trebui 20-80%, nu {result['score']}%"
        print(f"✓ Test partial_answer passed (score={result['score']}%)")


class TestFactoryPattern:
    """Teste pentru Factory Pattern."""

    def test_factory_registration(self):
        """Test: Factory înregistrează tipuri corect."""
        types = QuestionFactory.get_available_types()

        assert "n-queens" in types, "Factory ar trebui să aibă 'n-queens' înregistrat"
        print(f"✓ Test factory_registration passed (types={types})")

    def test_invalid_type(self):
        """Test: Factory returnează None pentru tip invalid."""
        q = create_question("invalid-type", "medium")

        assert q is None, "Factory ar trebui să returneze None pentru tip invalid"
        print("✓ Test invalid_type passed")

    def test_export_to_dict(self):
        """Test: Întrebarea se exportă corect ca dicționar."""
        q = create_question("n-queens", "medium")
        data = q.to_dict()

        assert "type" in data, "Export ar trebui să conțină 'type'"
        assert "question" in data, "Export ar trebui să conțină 'question'"
        assert "answer" in data, "Export ar trebui să conțină 'answer'"
        assert "keywords" in data, "Export ar trebui să conțină 'keywords'"
        print(f"✓ Test export_to_dict passed (keys={list(data.keys())})")


def run_all_tests():
    """Rulează toate testele."""
    print("=" * 70)
    print("🧪 Rulare teste unitare SmarTest")
    print("=" * 70)

    test_classes = [TestQuestionGeneration, TestEvaluation, TestFactoryPattern]

    total_tests = 0
    passed_tests = 0
    failed_tests = []

    for test_class in test_classes:
        print(f"\n📦 {test_class.__name__}")
        print("-" * 70)

        instance = test_class()
        test_methods = [method for method in dir(instance) if method.startswith("test_")]

        for method_name in test_methods:
            total_tests += 1
            try:
                method = getattr(instance, method_name)
                method()
                passed_tests += 1
            except AssertionError as e:
                print(f"✗ {method_name} FAILED: {e}")
                failed_tests.append(f"{test_class.__name__}.{method_name}")
            except Exception as e:
                print(f"✗ {method_name} ERROR: {e}")
                failed_tests.append(f"{test_class.__name__}.{method_name}")

    # Sumar
    print("\n" + "=" * 70)
    print("📊 SUMAR TESTE")
    print("=" * 70)
    print(f"Total teste: {total_tests}")
    print(f"✓ Passed: {passed_tests}")
    print(f"✗ Failed: {len(failed_tests)}")

    if failed_tests:
        print("\nTeste eșuate:")
        for test in failed_tests:
            print(f"  - {test}")
        return False
    else:
        print("\n🎉 Toate testele au trecut cu succes!")
        return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)