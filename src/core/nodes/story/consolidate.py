from typing import Dict, Any, List
import json

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

from src.core.nodes.prompts.consolidate_prompts import CONSOLIDATE_SYSTEM_PROMPT, CONSOLIDATE_HUMAN_PROMPT
from src.providers.llm_factory import LLMFactory
from src.utils import transform_json_to_text


def create_consolidate_node(llm_provider="vertexai", model="gemini-2.0-pro-exp-02-05"):
    """Create a node that consolidates scene descriptions and unified prompts into image generation prompts."""
    
    # Initialize the language model
    llm = LLMFactory.create(
        provider=llm_provider,
        model=model,
        response_mime_type="application/json",
        response_schema={
            "type": "array",
            "items": {
                "type": "string"
            }
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
    
    def consolidate_prompts(state):
        """
        Consolidate scene descriptions with unified prompts to create image generation prompts.
        
        Args:
            state: The current workflow state containing scenes and story_unified_prompts
            
        Returns:
            Updated state with consolidated scene prompts
        """
        # Get the required inputs from the state
        scenes = state.get("scenes", {})
        story_unified_prompts = state.get("story_unified_prompts", {})
        
        # Skip processing if necessary data is missing
        if not scenes or not story_unified_prompts:
            return {
                "output": "Missing required data: scenes or story_unified_prompts",
                "scene_prompts": None
            }
        
        # Format the inputs for the prompt
        formatted_inputs = {
            "scenes": json.dumps(scenes, indent=2),
            "story_unified_prompts": transform_json_to_text(story_unified_prompts)
        }
        
        # Invoke the LLM chain
        result = chain.invoke(formatted_inputs)
        
        # Parse the result into a dictionary of scene prompts
        # ai_message_content = result.content

        # scene_prompts = json.loads(ai_message_content)

        conversation_entry = {
            "step": "3",
            "output": result,
            "raw_output": result,
        }
        # The raw text result needs to be processed into scene prompts
        # For simplicity, we'll split by scene number (expecting the LLM to format properly)
        # In a real implementation, a more robust parsing might be needed
        
        # Save the raw output and parsed scene prompts
        return {
            "scene_prompts": result,
            "conversation_history": [conversation_entry]
        }
    
    return consolidate_prompts
