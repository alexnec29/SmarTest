# core/base_question_handler.py

import random
from typing import Dict, Any, List, Tuple
from abc import ABC, abstractmethod


class BaseQuestionHandler(ABC):
    """
    Base class for handling question generation.
    Provides common functionality to avoid code repetition.
    """
    
    def __init__(self, template: Dict[str, Any]):
        """
        Initialize with a template loaded from JSON.
        
        Args:
            template: Dictionary containing question templates and metadata
        """
        self.template = template
        self.questions = template.get("questions", [])
        self.params_definition = template.get("params", {})
    
    def select_question_variant(self, variant_index: int = None) -> Dict[str, Any]:
        """
        Select a question variant from the template.
        
        Args:
            variant_index: Specific variant to select. If None, selects randomly.
            
        Returns:
            Dictionary containing the selected question variant
        """
        if not self.questions:
            return {}
        
        if variant_index is not None and 0 <= variant_index < len(self.questions):
            return self.questions[variant_index]
        
        return random.choice(self.questions)
    
    def prepare_params(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Prepare parameters by merging provided params with defaults from template.
        
        Args:
            params: User-provided parameters
            
        Returns:
            Merged parameters with defaults applied
        """
        result = {}
        
        # Apply defaults from template
        for key, meta in self.params_definition.items():
            if isinstance(meta, dict):
                # If meta has choices, randomly select one as default
                if "choices" in meta and meta["choices"]:
                    default = meta.get("default", random.choice(meta["choices"]))
                else:
                    default = meta.get("default")
            else:
                default = meta
            
            result[key] = default
        
        # Override with user-provided params
        if params:
            result.update(params)
        
        return result
    
    def format_text(self, text: str, params: Dict[str, Any]) -> str:
        """
        Format text with parameters, handling missing keys gracefully.
        
        Args:
            text: Template text with {placeholders}
            params: Parameters to substitute
            
        Returns:
            Formatted text
        """
        try:
            return text.format(**params)
        except KeyError:
            # If some keys are missing, return the text as-is
            return text
    
    def generate_from_template(self, variant: Dict[str, Any], params: Dict[str, Any]) -> Tuple[str, str]:
        """
        Generate question and answer from a template variant.
        
        Args:
            variant: Question variant from template
            params: Parameters for generation
            
        Returns:
            Tuple of (question, answer)
        """
        question_template = variant.get("question", "")
        answer_template = variant.get("answer", "")
        
        question = self.format_text(question_template, params)
        answer = self.format_text(answer_template, params)
        
        return question, answer
    
    def generate(self, params: Dict[str, Any] = None, variant_index: int = None) -> Tuple[str, str]:
        """
        Main generation method. Can be overridden for custom logic.
        
        Args:
            params: Parameters for generation
            variant_index: Specific variant to use
            
        Returns:
            Tuple of (question, answer)
        """
        # Prepare parameters
        prepared_params = self.prepare_params(params)
        
        # Select question variant
        variant = self.select_question_variant(variant_index)
        
        if not variant:
            return "", ""
        
        # Check if custom generation is needed
        if self.needs_custom_generation(variant, prepared_params):
            return self.generate_custom(variant, prepared_params)
        
        # Default: generate from template
        return self.generate_from_template(variant, prepared_params)
    
    def needs_custom_generation(self, variant: Dict[str, Any], params: Dict[str, Any]) -> bool:
        """
        Determine if custom generation logic is needed.
        Can be overridden in subclasses.
        
        Args:
            variant: Question variant
            params: Parameters
            
        Returns:
            True if custom generation is needed
        """
        return variant.get("requires_computation", False)
    
    @abstractmethod
    def generate_custom(self, variant: Dict[str, Any], params: Dict[str, Any]) -> Tuple[str, str]:
        """
        Custom generation logic. Must be implemented by subclasses that need it.
        
        Args:
            variant: Question variant
            params: Parameters
            
        Returns:
            Tuple of (question, answer)
        """
        pass
