from langchain_core.runnables import RunnablePassthrough
from src.providers.llm_factory import LLMFactory
from src.core.nodes.prompts.step2_prompts import step2_prompt
from src.utils import transform_json_to_text
import json
from src.utils import load_default_content

llm_provider="vertexai"
model="gemini-2.0-pro-exp-02-05"

def create_step2_node(state):
    story_text = load_default_content()

    """Create second analysis node with Gemini 1.5 Pro configuration."""
    llm = LLMFactory.create(
        provider=llm_provider,
        model=model,  # More advanced model for deeper analysis
        response_mime_type="application/json",
        response_schema={
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "scene_number": {"type": "integer"},
                "title": {"type": "string"},
                "description": {"type": "string"},
                "camera": {"type": "string"},
                "character": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "variation": {"type": "string"},
                        "action": {"type": "string"}
                    },
                    "required": ["name", "variation", "action"]
                },
                "background": {"type": "string"}
                },
                "required": ["scene_number", "title", "description", "camera", "character", "background"]
            }
        }
    )
    
    # Create the base chain
    base_chain = RunnablePassthrough() | step2_prompt | llm
    
    story_unified_text = transform_json_to_text(state["story_unified_prompts"])
    
    result = base_chain.invoke({"story_text": story_text, "story_unified_text": story_unified_text})
    # Extract the content from the AI message
    ai_message_content = result.content

    # Parse the JSON content and verify it matches the schema
    ai_message_content_json = json.loads(ai_message_content)

    conversation_entry = {
        "step": "step2",
        "input": story_text,
        "output": ai_message_content,
        "raw_output": result,
    }

    return {"scenes": ai_message_content_json,
            "conversation_history": [conversation_entry]}
    