# ui/enhanced_client.py

"""
Enhanced CLI for SmarTest application.
Supports generating multiple questions, selecting topics, and building tests.
"""

import os
from typing import List
from core.test_builder import TestBuilder
from core.evaluator import evaluate_answer
from core.pdf_generator import PDFGenerator, is_pdf_available


def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 60)
    print("SmarTest - AI EXAM QUESTION GENERATOR")
    print("=" * 60)
    print("1. Generate a single question")
    print("2. Generate a test (multiple questions)")
    print("3. Answer a saved test")
    print("4. Exit")
    print("=" * 60)


def display_topics(builder: TestBuilder):
    """Display available topics."""
    topics = builder.get_available_topics()
    print("\nAvailable Topics:")
    print("-" * 60)
    for i, (topic_id, topic_name) in enumerate(topics.items(), 1):
        print(f"{i}. {topic_name} ({topic_id})")
    print("-" * 60)


def select_topics(builder: TestBuilder) -> List[str]:
    """
    Allow user to select topics.
    
    Returns:
        List of selected topic IDs
    """
    topics = builder.get_available_topics()
    topic_list = list(topics.keys())
    
    display_topics(builder)
    print("\nSelect topics (comma-separated numbers, or 'all' for all topics):")
    selection = input("> ").strip().lower()
    
    if selection == 'all':
        return topic_list
    
    try:
        indices = [int(x.strip()) - 1 for x in selection.split(',')]
        selected = [topic_list[i] for i in indices if 0 <= i < len(topic_list)]
        return selected if selected else topic_list
    except (ValueError, IndexError):
        print("Invalid selection. Using all topics.")
        return topic_list


def generate_single_question():
    """Generate and answer a single question."""
    from core.question_factory import generate_question_and_answer
    from core.evaluator import load_keywords_for_topic
    
    builder = TestBuilder()
    display_topics(builder)
    
    topic_input = input("\nEnter topic ID (e.g., n-queens): ").strip().lower()
    
    # Validate topic
    topics = builder.get_available_topics()
    if topic_input not in topics:
        print(f"Unknown topic. Using 'n-queens'.")
        topic_input = 'n-queens'
    
    print(f"\nGenerating question for: {topics[topic_input]}")
    question, correct_answer = generate_question_and_answer(topic_input, params={})
    
    if not question:
        print("Failed to generate question.")
        return
    
    print("\n" + "=" * 60)
    print("QUESTION")
    print("=" * 60)
    print(question)
    print("=" * 60)
    
    user_answer = input("\nYour answer: ").strip()
    
    if not user_answer:
        print("No answer provided.")
        return
    
    # Load keywords for this topic
    keywords = load_keywords_for_topic(topic_input)
    
    # Evaluate with keywords
    score = evaluate_answer(correct_answer, user_answer, keywords)
    
    print("\n" + "=" * 60)
    print("EVALUATION RESULT")
    print("=" * 60)
    print(f"Your score: {score}%")
    print(f"\nCorrect answer:")
    print(correct_answer)
    print("=" * 60)


def generate_test():
    """Generate a test with multiple questions."""
    builder = TestBuilder()
    
    # Get number of questions
    try:
        num_questions = int(input("\nHow many questions do you want? (default: 5): ").strip() or "5")
        if num_questions < 1:
            num_questions = 5
    except ValueError:
        num_questions = 5
    
    # Select topics
    selected_topics = select_topics(builder)
    
    if not selected_topics:
        print("No topics selected. Aborting.")
        return
    
    print(f"\nGenerating {num_questions} questions from {len(selected_topics)} topics...")
    
    try:
        questions, answers = builder.generate_test(
            topics=selected_topics,
            num_questions=num_questions
        )
    except Exception as e:
        print(f"Error generating test: {e}")
        return
    
    # Display questions
    print("\n" + builder.get_questions_text())
    
    # Ask if user wants to save
    save = input("\nSave questions to file? (y/n): ").strip().lower()
    if save == 'y':
        # Ask for format
        if is_pdf_available():
            file_format = input("Format (txt/pdf, default: txt): ").strip().lower() or "txt"
        else:
            file_format = "txt"
            print("PDF generation not available. Using text format.")
        
        if file_format == "pdf":
            questions_file = input("Questions filename (default: questions.pdf): ").strip() or "questions.pdf"
            answers_file = input("Answers filename (default: answers.pdf): ").strip() or "answers.pdf"
            
            # Sanitize filenames
            import os
            questions_file = os.path.basename(questions_file)
            answers_file = os.path.basename(answers_file)
            if not questions_file.endswith('.pdf'):
                questions_file += '.pdf'
            if not answers_file.endswith('.pdf'):
                answers_file += '.pdf'
            
            try:
                pdf_gen = PDFGenerator()
                pdf_gen.generate_questions_pdf(questions, questions_file)
                pdf_gen.generate_answers_pdf(answers, answers_file)
                print(f"\n✓ Questions saved to: {questions_file}")
                print(f"✓ Answers saved to: {answers_file}")
            except Exception as e:
                print(f"Error generating PDFs: {e}")
        else:
            questions_file = input("Questions filename (default: questions.txt): ").strip() or "questions.txt"
            answers_file = input("Answers filename (default: answers.txt): ").strip() or "answers.txt"
            
            try:
                builder.save_questions_to_file(questions_file)
                builder.save_answers_to_file(answers_file)
                print(f"\n✓ Questions saved to: {questions_file}")
                print(f"✓ Answers saved to: {answers_file}")
            except Exception as e:
                print(f"Error saving files: {e}")
    
    # Ask if user wants to answer now
    answer_now = input("\nDo you want to answer the questions now? (y/n): ").strip().lower()
    if answer_now == 'y':
        answer_test(questions, answers)


def answer_test(questions: List = None, correct_answers: List = None):
    """
    Answer a test (either newly generated or loaded from file).
    
    Args:
        questions: List of question objects (if already generated)
        correct_answers: List of correct answers (if already generated)
    """
    from core.evaluator import load_keywords_for_topic
    from core.test_parser import load_test_and_answers
    import os
    
    if questions is None:
        # Load from file
        filename = input("\nEnter questions filename: ").strip()
        # Sanitize filename
        filename = os.path.basename(filename)
        if not os.path.exists(filename):
            print(f"File not found: {filename}")
            return
        
        # Try to find corresponding answer file
        answer_filename = None
        if filename.endswith('.txt'):
            # Try common patterns like "test.txt" -> "answers.txt" or "test_answers.txt"
            base_name = filename.replace('.txt', '')
            possible_answer_files = [
                base_name.replace('test', 'answers') + '.txt',
                base_name.replace('questions', 'answers') + '.txt',
                base_name + '_answers.txt',
                'answers.txt',
                'example_answers.txt'
            ]
            for af in possible_answer_files:
                if os.path.exists(af):
                    answer_filename = af
                    break
        
        # Ask user if they want to provide answer file
        if not answer_filename:
            answer_file_input = input("\nEnter answer filename (or press Enter to skip): ").strip()
            if answer_file_input:
                answer_file_input = os.path.basename(answer_file_input)
                if os.path.exists(answer_file_input):
                    answer_filename = answer_file_input
        
        # Parse files
        try:
            questions, correct_answers = load_test_and_answers(filename, answer_filename)
            if answer_filename:
                print(f"\n✓ Loaded {len(questions)} questions from '{filename}'")
                print(f"✓ Loaded {len(correct_answers)} answers from '{answer_filename}'")
            else:
                print(f"\n✓ Loaded {len(questions)} questions from '{filename}'")
                print("⚠ No answer file loaded - manual evaluation only")
                correct_answers = None
        except Exception as e:
            print(f"Error parsing test file: {e}")
            return
    
    # Answer each question
    user_answers = []
    scores = []
    
    print("\n" + "=" * 60)
    print("ANSWERING TEST")
    print("=" * 60)
    
    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}/{len(questions)}:")
        print(q['question'])
        print("-" * 60)
        user_answer = input("Your answer: ").strip()
        user_answers.append(user_answer)
        
        if correct_answers and i <= len(correct_answers):
            # Load keywords for this question's topic
            keywords = load_keywords_for_topic(q.get('topic', ''))
            score = evaluate_answer(correct_answers[i-1], user_answer, keywords)
            scores.append(score)
    
    # Display results
    print("\n" + "=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)
    
    if scores:
        for i, (q, score, user_ans, correct_ans) in enumerate(
            zip(questions, scores, user_answers, correct_answers), 1
        ):
            print(f"\nQuestion {i}: {score}%")
            print(f"Your answer: {user_ans}")
            print(f"Correct answer: {correct_ans}")
            print("-" * 60)
        
        avg_score = sum(scores) / len(scores)
        print(f"\nAverage Score: {avg_score:.1f}%")
        print("=" * 60)
    else:
        print("\nNo automatic evaluation available.")
        print("Please check your answers manually.")
        print("=" * 60)


def run_enhanced_cli():
    """Run the enhanced CLI interface."""
    print("\nWelcome to SmarTest!")
    
    while True:
        display_menu()
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == '1':
            generate_single_question()
        elif choice == '2':
            generate_test()
        elif choice == '3':
            answer_test()
        elif choice == '4':
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please select 1-4.")


if __name__ == "__main__":
    run_enhanced_cli()
