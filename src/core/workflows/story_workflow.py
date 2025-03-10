from typing import Annotated, Dict, Any, List
from typing_extensions import TypedDict
import operator
import os

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from src.core.nodes.story.step1_node import create_step1_node
from src.core.nodes.story.step2_node import create_step2_node
from src.core.nodes.story.consolidate import create_consolidate_node

class StoryState(TypedDict):
    """State definition for the Story workflow."""
    input: str | None  # Generic input field that can be empty
    output: str | None  # Generic input field that can be empty
    story_unified_prompts: Dict[str, Any] | None 
    scenes: Dict[str, Any] | None 
    pregenerated_clip_prompts: List[str] | None 
    pregenerated_t5_prompts: List[str] | None
    clip_prompts: List[str] | None
    t5_prompts: List[str] | None
    metadata: Annotated[Dict[str, Any], operator.or_] | None  # Optional metadata that can be merged
    conversation_history: Annotated[List[Any], operator.add] | None  # Full conversation history


def create_story_workflow():
    workflow = StateGraph(StoryState)
    
    # Add nodes to workflow
    workflow.add_node("step1", create_step1_node)
    workflow.add_node("step2", create_step2_node)
    workflow.add_node("consolidate", create_consolidate_node)
    
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