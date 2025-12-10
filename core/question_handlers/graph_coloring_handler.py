# core/question_handlers/graph_coloring_handler.py

from typing import Dict, Any, Tuple, List
from ..base_question_handler import BaseQuestionHandler


class GraphColoringHandler(BaseQuestionHandler):
    """Handler for Graph Coloring problem questions."""
    
    def get_example_graph(self, graph_id: str) -> Dict[str, Any]:
        """Get graph data by ID."""
        if graph_id == "k4":
            return {
                "nodes": [1, 2, 3, 4],
                "edges": [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)],
                "name": "Graful K4 (Complet, 4 noduri)",
                "chromatic_number": 4
            }
        elif graph_id == "wheel5":
            return {
                "nodes": [1, 2, 3, 4, 5],
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 3)],
                "name": "Graful Roată W5",
                "chromatic_number": 3
            }
        # Default to k4
        return self.get_example_graph("k4")
    
    def generate_custom(self, variant: Dict[str, Any], params: Dict[str, Any]) -> Tuple[str, str]:
        """
        Generate Graph Coloring question and answer with computation.
        
        Args:
            variant: Question variant
            params: Parameters including 'graph_id' and 'k_colors'
            
        Returns:
            Tuple of (question, answer)
        """
        graph_id = params.get("graph_id", "k4")
        k_colors = params.get("k_colors", 3)
        question_id = variant.get("id", "")
        
        # Get graph data
        graph = self.get_example_graph(graph_id)
        
        # Add graph info to params for formatting
        params["graph_name"] = graph["name"]
        params["nodes"] = str(graph["nodes"])
        edges_str = ", ".join([f"({u},{v})" for u, v in graph["edges"]])
        params["edges"] = "{" + edges_str + "}"
        
        # Generate question from template
        question = self.format_text(variant.get("question", ""), params)
        
        # Generate computed answer
        if question_id == "chromatic_number":
            answer = self._generate_chromatic_number_answer(graph)
        elif question_id == "is_k_colorable":
            answer = self._generate_k_colorable_answer(graph, k_colors)
        else:
            # Fallback to template
            answer = self.format_text(variant.get("answer", ""), params)
        
        return question, answer
    
    def needs_custom_generation(self, variant: Dict[str, Any], params: Dict[str, Any]) -> bool:
        """Graph coloring always needs custom generation to populate graph data."""
        return True
    
    def _generate_chromatic_number_answer(self, graph: Dict[str, Any]) -> str:
        """Generate answer for chromatic number question."""
        chromatic_number = graph.get("chromatic_number", 0)
        graph_name = graph.get("name", "")
        
        if "K4" in graph_name:
            return f"Graful K4 este un graf complet, deci numărul cromatic este egal cu numărul de noduri: {chromatic_number}."
        elif "W5" in graph_name:
            return f"Numărul cromatic este {chromatic_number} (pentru că nu este un graf complet și nu conține un ciclu impar)."
        else:
            return f"Numărul cromatic este {chromatic_number}."
    
    def _generate_k_colorable_answer(self, graph: Dict[str, Any], k_colors: int) -> str:
        """Generate answer for k-colorability question."""
        chromatic_number = graph.get("chromatic_number", 0)
        
        if k_colors >= chromatic_number:
            return "Da"
        else:
            return f"Nu. Graful necesită minim {chromatic_number} culori (numărul cromatic)."
