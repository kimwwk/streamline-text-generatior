from typing import Annotated, Dict, Any, List
from typing_extensions import TypedDict
import operator
import os

from langgraph.graph import StateGraph, END
from src.core.nodes.story.step1_node import create_step1_node
from src.core.nodes.story.step2_node import create_step2_node


class StoryState(TypedDict):
    """State definition for the Story workflow."""
    input: str | None  # Generic input field that can be empty
    step1_result: Dict[str, Any] | None  # Result from step1 
    step2_result: Dict[str, Any] | None  # Result from step2
    metadata: Annotated[Dict[str, Any], operator.or_] | None  # Optional metadata that can be merged
    conversation_history: Annotated[List[Dict[str, Any]], operator.add] | None  # Full conversation history

# Function to load default content from file
def load_default_content(file_path="src/entities/default_story.txt"):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        # Return empty string or a placeholder if file doesn't exist
        return ""

def create_story_workflow():
    workflow = StateGraph(StoryState)
    story_text = load_default_content()
    
    # Create nodes from their individual modules
    step1_node = create_step1_node(story_text)
    step2_node = create_step2_node(story_text)
    
    # Build workflow graph
    workflow.add_node("step1", step1_node)
    workflow.add_node("step2", step2_node)
    workflow.set_entry_point("step1")
    workflow.add_edge("step1", "step2")
    workflow.add_edge("step2", END)
    
    return workflow.compile() 