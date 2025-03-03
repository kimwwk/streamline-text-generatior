from typing import Annotated, Dict, Any, List
from typing_extensions import TypedDict
import operator
import os

from langgraph.graph import StateGraph, END
from src.core.nodes.story.step1_node import create_step1_node
from src.core.nodes.story.step2_node import create_step2_node
from src.core.nodes.story.consolidate import create_consolidate_node


class StoryState(TypedDict):
    """State definition for the Story workflow."""
    input: str | None  # Generic input field that can be empty
    output: str | None  # Generic input field that can be empty
    story_unified_prompts: Dict[str, Any] | None 
    scenes: Dict[str, Any] | None 
    scene_prompts: str | None  # Final consolidated scene prompts ready for image generation
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
    consolidate_node = create_consolidate_node()
    
    # Add nodes to workflow
    workflow.add_node("step1", step1_node)
    workflow.add_node("step2", step2_node)
    workflow.add_node("consolidate", consolidate_node)
    
    # Define the workflow edges
    workflow.set_entry_point("step1")
    workflow.add_edge("step1", "step2")
    workflow.add_edge("step2", "consolidate")
    workflow.add_edge("consolidate", END)
    
    # Set default values for initial state
    # initial_state = {
    #     "story_text": story_text,
    #     "output": None,
    #     "story_unified_prompts": None,
    #     "scenes": None,
    #     "scene_prompts": None,
    #     "metadata": {},
    #     "conversation_history": []
    # }
    
    # Compile the workflow
    return workflow.compile() 