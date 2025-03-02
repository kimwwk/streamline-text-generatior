from typing import Annotated, Dict, Any
from typing_extensions import TypedDict
import operator

from langgraph.graph import StateGraph, END
from src.core.nodes.analysis.step1_node import create_step1_node
from src.core.nodes.analysis.step2_node import create_step2_node
from src.core.nodes.output import format_response

class GeminiState(TypedDict):
    """State definition for the Gemini workflow."""
    content: str  # Input content
    step1_result: Dict[str, Any]  # Result from step1
    step2_result: Dict[str, Any]  # Result from step2
    metadata: Annotated[Dict[str, Any], operator.or_]  # Optional metadata that can be merged

def create_gemini_workflow():
    workflow = StateGraph(GeminiState)
    
    # Create nodes from their individual modules
    step1_node = create_step1_node()
    step2_node = create_step2_node()
    
    # Build workflow graph
    workflow.add_node("step1", step1_node)
    workflow.add_node("step2", step2_node)
    workflow.set_entry_point("step1")
    workflow.add_edge("step1", "step2")
    workflow.add_edge("step2", END)
    
    return workflow.compile()
