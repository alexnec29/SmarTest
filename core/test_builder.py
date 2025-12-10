# core/test_builder.py

import random
from typing import List, Dict, Any, Tuple
from .question_factory import generate_question_and_answer


class TestBuilder:
    """
    Builder for creating tests with multiple questions.
    Allows selecting topics and generating multiple questions.
    """
    
    # Available topics/chapters
    AVAILABLE_TOPICS = {
        "n-queens": "N-Queens Problem (Backtracking)",
        "knights-tour": "Knight's Tour Problem",
        "graph-coloring": "Graph Coloring (CSP)",
        "generalised-hanoi": "Generalized Hanoi Towers",
        "minimax": "Minimax with Alpha-Beta Pruning",
        "nash-equilibrium": "Nash Equilibrium (Game Theory)",
        "csp": "Constraint Satisfaction Problems",
    }
    
    def __init__(self):
        """Initialize the test builder."""
        self.questions = []
        self.answers = []
        self.topics = []
    
    def get_available_topics(self) -> Dict[str, str]:
        """
        Get dictionary of available topics.
        
        Returns:
            Dictionary mapping topic IDs to descriptions
        """
        return self.AVAILABLE_TOPICS.copy()
    
    def generate_test(
        self, 
        topics: List[str] = None, 
        num_questions: int = 5,
        params: Dict[str, Any] = None
    ) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        Generate a test with multiple questions.
        
        Args:
            topics: List of topic IDs to include. If None, uses all topics.
            num_questions: Number of questions to generate
            params: Optional parameters for question generation
            
        Returns:
            Tuple of (questions_list, answers_list)
            Each question is a dict with: {id, topic, question, params}
            Each answer is a string
        """
        params = params or {}
        
        # Use all topics if none specified
        if not topics:
            topics = list(self.AVAILABLE_TOPICS.keys())
        
        # Validate topics
        valid_topics = [t for t in topics if t in self.AVAILABLE_TOPICS]
        if not valid_topics:
            raise ValueError(f"No valid topics provided. Available: {list(self.AVAILABLE_TOPICS.keys())}")
        
        questions = []
        answers = []
        
        for i in range(num_questions):
            # Select topic (cycle through if more questions than topics)
            topic = valid_topics[i % len(valid_topics)]
            
            # Generate question and answer
            question_text, answer_text = generate_question_and_answer(topic, params)
            
            # Create question object
            question_obj = {
                "id": i + 1,
                "topic": topic,
                "topic_name": self.AVAILABLE_TOPICS[topic],
                "question": question_text,
                "params": params.copy()
            }
            
            questions.append(question_obj)
            answers.append(answer_text)
        
        # Store for later use
        self.questions = questions
        self.answers = answers
        self.topics = valid_topics
        
        return questions, answers
    
    def get_questions_text(self, include_topic: bool = True) -> str:
        """
        Get all questions as formatted text.
        
        Args:
            include_topic: Whether to include topic name with each question
            
        Returns:
            Formatted string with all questions
        """
        if not self.questions:
            return "No questions generated yet."
        
        lines = []
        lines.append("=" * 80)
        lines.append("TEST - ARTIFICIAL INTELLIGENCE")
        lines.append("=" * 80)
        lines.append("")
        
        for q in self.questions:
            lines.append(f"Question {q['id']}:")
            if include_topic:
                lines.append(f"Topic: {q['topic_name']}")
            lines.append("")
            lines.append(q['question'])
            lines.append("")
            lines.append("-" * 80)
            lines.append("")
        
        return "\n".join(lines)
    
    def get_answers_text(self) -> str:
        """
        Get all answers as formatted text.
        
        Returns:
            Formatted string with all answers
        """
        if not self.answers:
            return "No answers generated yet."
        
        lines = []
        lines.append("=" * 80)
        lines.append("ANSWER KEY")
        lines.append("=" * 80)
        lines.append("")
        
        for i, answer in enumerate(self.answers, 1):
            lines.append(f"Answer {i}:")
            lines.append("")
            lines.append(answer)
            lines.append("")
            lines.append("-" * 80)
            lines.append("")
        
        return "\n".join(lines)
    
    def save_questions_to_file(self, filename: str, include_topic: bool = True):
        """
        Save questions to a text file.
        
        Args:
            filename: Output filename
            include_topic: Whether to include topic names
        """
        content = self.get_questions_text(include_topic)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def save_answers_to_file(self, filename: str):
        """
        Save answers to a text file.
        
        Args:
            filename: Output filename
        """
        content = self.get_answers_text()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
