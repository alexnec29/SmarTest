# core/test_parser.py

"""
Parser for test and answer files.
Parses questions and answers from saved text files.
"""

import re
from typing import List, Dict, Any, Tuple


def parse_test_file(content: str) -> List[Dict[str, Any]]:
    """
    Parse a test file and extract questions with their metadata.
    
    Args:
        content: The content of the test file
        
    Returns:
        List of question dictionaries with keys: id, topic, topic_name, question
    """
    questions = []
    
    # Split by question markers
    question_pattern = r"Question (\d+):"
    parts = re.split(question_pattern, content)
    
    # Skip the header (parts[0])
    for i in range(1, len(parts), 2):
        if i + 1 >= len(parts):
            break
            
        question_num = int(parts[i])
        question_block = parts[i + 1]
        
        # Extract topic if present
        topic_match = re.search(r"Topic:\s*(.+?)(?:\n|$)", question_block)
        topic_name = topic_match.group(1).strip() if topic_match else ""
        
        # Map topic name to topic ID
        topic_id = map_topic_name_to_id(topic_name)
        
        # Extract the actual question text (everything after topic and before separator)
        # Remove the topic line and separator lines
        question_text = re.sub(r"Topic:\s*.+?\n+", "", question_block)
        question_text = re.sub(r"-{60,}", "", question_text).strip()
        
        questions.append({
            "id": question_num,
            "topic": topic_id,
            "topic_name": topic_name,
            "question": question_text
        })
    
    return questions


def parse_answer_file(content: str) -> List[str]:
    """
    Parse an answer file and extract answers.
    
    Args:
        content: The content of the answer file
        
    Returns:
        List of answer strings
    """
    answers = []
    
    # Split by answer markers
    answer_pattern = r"Answer (\d+):"
    parts = re.split(answer_pattern, content)
    
    # Skip the header (parts[0])
    for i in range(1, len(parts), 2):
        if i + 1 >= len(parts):
            break
            
        answer_block = parts[i + 1]
        
        # Extract the actual answer text (remove separator lines)
        answer_text = re.sub(r"-{60,}", "", answer_block).strip()
        answers.append(answer_text)
    
    return answers


def map_topic_name_to_id(topic_name: str) -> str:
    """
    Map a topic name to its ID.
    
    Args:
        topic_name: The full topic name (e.g., "N-Queens Problem (Backtracking)")
        
    Returns:
        The topic ID (e.g., "n-queens")
    """
    # Topic mapping based on TestBuilder.AVAILABLE_TOPICS
    topic_mapping = {
        "N-Queens Problem (Backtracking)": "n-queens",
        "Knight's Tour Problem": "knights-tour",
        "Graph Coloring (CSP)": "graph-coloring",
        "Generalized Hanoi Towers": "generalised-hanoi",
        "Minimax with Alpha-Beta Pruning": "minimax",
        "Nash Equilibrium (Game Theory)": "nash-equilibrium",
        "Constraint Satisfaction Problems": "csp",
    }
    
    return topic_mapping.get(topic_name, "")


def load_test_and_answers(test_filename: str, answer_filename: str = None) -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Load questions and answers from files.
    
    Args:
        test_filename: Path to the test file
        answer_filename: Optional path to the answer file
        
    Returns:
        Tuple of (questions, answers)
    """
    import os
    
    # Load test file
    if not os.path.exists(test_filename):
        raise FileNotFoundError(f"Test file not found: {test_filename}")
    
    with open(test_filename, 'r', encoding='utf-8') as f:
        test_content = f.read()
    
    questions = parse_test_file(test_content)
    
    # Load answer file if provided
    answers = []
    if answer_filename and os.path.exists(answer_filename):
        with open(answer_filename, 'r', encoding='utf-8') as f:
            answer_content = f.read()
        answers = parse_answer_file(answer_content)
    
    return questions, answers
