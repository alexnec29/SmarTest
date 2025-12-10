# core/question_factory.py

import json
import os
from typing import Tuple, Dict, Any

from .base_question_handler import BaseQuestionHandler
from .question_handlers import (
    NQueensHandler,
    KnightsTourHandler,
    GraphColoringHandler,
    GeneralisedHanoiHandler,
    MinimaxHandler,
    NashEquilibriumHandler,
    CSPHandler,
)

# Map topic names to handler classes
HANDLER_CLASSES = {
    "n-queens": NQueensHandler,
    "knights-tour": KnightsTourHandler,
    "knights_tour": KnightsTourHandler,
    "graph-coloring": GraphColoringHandler,
    "graph_coloring": GraphColoringHandler,
    "generalised-hanoi": GeneralisedHanoiHandler,
    "generalised_hanoi": GeneralisedHanoiHandler,
    "minimax": MinimaxHandler,
    "nash-equilibrium": NashEquilibriumHandler,
    "nash_equilibrium": NashEquilibriumHandler,
    "csp": CSPHandler,
}

TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), "..", "templates")


def load_template(topic: str) -> Dict[str, Any]:
    """
    Load a JSON template for a given topic.
    
    Args:
        topic: The topic name
        
    Returns:
        Dictionary containing the template data
    """
    path = os.path.join(TEMPLATES_PATH, f"{topic.replace('-', '_')}.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def generate_question_and_answer(topic: str, params: Dict[str, Any] = None) -> Tuple[Any, Any]:
    """
    Generate question and answer for the given topic.
    
    This is the main entry point for question generation. It:
    1. Loads the template for the topic
    2. Creates the appropriate handler
    3. Generates the question and answer dynamically
    
    Args:
        topic: The topic name (e.g., 'n-queens', 'minimax')
        params: Optional parameters for question generation
        
    Returns:
        Tuple of (question, answer)
    """
    params = params or {}
    
    # Normalize topic name
    topic_normalized = topic.lower().replace("-", "_")
    
    # Load template
    template = load_template(topic)
    
    if not template:
        # Unknown topic - return empty
        return None, None
    
    # Get handler class for this topic
    handler_class = HANDLER_CLASSES.get(topic.lower())
    
    if not handler_class:
        # No handler found - try to use template directly
        return _generate_from_template_only(template, params)
    
    # Create handler instance
    handler = handler_class(template)
    
    # Generate question and answer
    question, answer = handler.generate(params)
    
    return question, answer


def _generate_from_template_only(template: Dict[str, Any], params: Dict[str, Any]) -> Tuple[str, str]:
    """
    Fallback method to generate from template when no handler is available.
    
    Args:
        template: Template dictionary
        params: Parameters for generation
        
    Returns:
        Tuple of (question, answer)
    """
    # Get first question if multiple exist
    questions = template.get("questions", [])
    
    if questions:
        # Use first question variant
        variant = questions[0]
        question_template = variant.get("question", "")
        answer_template = variant.get("answer", "")
    else:
        # Old format - single question/answer
        question_template = template.get("question", "")
        answer_template = template.get("answer", "")
    
    # Apply default parameters from template
    params_definition = template.get("params", {})
    for key, meta in params_definition.items():
        if key not in params:
            if isinstance(meta, dict):
                params[key] = meta.get("default")
            else:
                params[key] = meta
    
    # Format templates
    try:
        question = question_template.format(**params)
    except Exception:
        question = question_template
    
    try:
        answer = answer_template.format(**params)
    except Exception:
        answer = answer_template
    
    return question, answer
