from typing import Dict, Any, List
import json

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

from src.core.nodes.prompts.consolidate_prompts import CONSOLIDATE_SYSTEM_PROMPT, CONSOLIDATE_HUMAN_PROMPT
from src.providers.llm_factory import LLMFactory
from src.utils import transform_json_to_text

def create_scene_prompts_manual(scene, story_unified_prompts):

    # get the character name and variation from scene. handle the errors properly.
    character_name = scene["character"]["name"] if scene["character"] else None
    variation = scene["character"]["variation"] if scene["character"] else None
    if not variation:
        variation = "Default"

    # get the character unified text
    character_unified_text_items = story_unified_prompts["characters"]
    character_unified_text_item = next(x for x in character_unified_text_items if x["name"] == character_name and x["variation"] == variation)
    character_unified_text = character_unified_text_item["description"]

    # create prompts
    prompt_1 = (
        "Masterpiece, Highly detailed. "
        + scene["description"]
        + " "
        + character_unified_text
        + " "
        + scene["character"]["action"]
    )
    prompt_2 = (
        "Masterpiece, Highly detailed. "
        + scene["description"]
        + " "
        + scene["camera"]
        + " "
        + character_unified_text
        + " "
        + scene["character"]["action"]
        + " "
        + scene["background"]
        + " "
        + story_unified_prompts["art_style"]
        + " "
        + story_unified_prompts["era_and_region"]
    )

    return [prompt_1, prompt_2]

llm_provider="vertexai"
model="gemini-2.0-pro-exp-02-05"

def create_consolidate_node(state):
    """Create a node that consolidates scene descriptions and unified prompts into image generation prompts."""
    
    # Initialize the language model
    llm = LLMFactory.create(
        provider=llm_provider,
        model=model,
        response_mime_type="application/json",
        response_schema={
            "type": "object",
            "properties": {
                "clip_prompts": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "t5_prompts": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["clip_prompts", "t5_prompts"]
        }
    )
    
    # Setup the prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", CONSOLIDATE_SYSTEM_PROMPT),
            ("human", CONSOLIDATE_HUMAN_PROMPT),
        ]
    )
    
    # Create the chain
    chain = (
        prompt
        | llm
        | JsonOutputParser()
    )
    
    # Get the required inputs from the state
    scenes = state.get("scenes", {})
    story_unified_prompts = state.get("story_unified_prompts", {})
    
    # Skip processing if necessary data is missing
    if not scenes or not story_unified_prompts:
        return {
            "output": "Missing required data: scenes or story_unified_prompts",
            "scene_prompts": None
        }
    
    scene_prompts_1_list = []
    scene_prompts_2_list = []
    for scene_number in range(len(scenes)):
        scene = scenes[scene_number]
        scene_prompts_1, scene_prompts_2 = create_scene_prompts_manual(scene, story_unified_prompts)
        scene_prompts_1_list.append(scene_prompts_1)
        scene_prompts_2_list.append(scene_prompts_2)

    # Format the inputs for the prompt
    formatted_inputs = {
        "scene_prompts_1_list": json.dumps(scene_prompts_1_list, indent=2),
        "scene_prompts_2_list": json.dumps(scene_prompts_2_list, indent=2),
        "story_unified_prompts": transform_json_to_text(story_unified_prompts)
    }
    
    # Invoke the LLM chain
    result = chain.invoke(formatted_inputs)
    
    # Store the conversation entry
    conversation_entry = {
        "step": "3",
        "output": result,
        "raw_output": result,
    }
    
    # Return both the clip prompts and t5 prompts in the state
    return {
        "clip_prompts": result.get("clip_prompts", []),
        "t5_prompts": result.get("t5_prompts", []),
        "pregenerated_clip_prompts": scene_prompts_1_list,
        "pregenerated_t5_prompts": scene_prompts_2_list,
        "conversation_history": [conversation_entry]
    }
    
