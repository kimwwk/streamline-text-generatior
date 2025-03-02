from langgraph.graph import StateGraph, END
from src.core.nodes.analysis_nodes import create_analysis_nodes
from src.core.nodes.output import format_response

def create_gemini_workflow():
    workflow = StateGraph(dict)
    
    # Create nodes with default configuration
    step1, step2 = create_analysis_nodes()
    
    # Build workflow graph
    workflow.add_node("step1", step1)
    workflow.add_node("step2", step2)
    workflow.set_entry_point("step1")
    workflow.add_edge("step1", "step2")
    workflow.add_edge("step2", END)
    
    return workflow, format_response
