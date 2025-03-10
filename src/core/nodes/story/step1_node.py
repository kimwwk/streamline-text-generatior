from langchain_core.runnables import RunnablePassthrough
from src.providers.llm_factory import LLMFactory
from src.core.nodes.prompts.step1_prompts import step1_prompt
import json
from src.utils import load_default_content

llm_provider="vertexai"
model="gemini-2.0-pro-exp-02-05"

def create_step1_node(state):

    story_text = load_default_content()

    """Create first analysis node with Gemini Pro configuration."""
    llm = LLMFactory.create(
        provider=llm_provider,
        model=model,
        response_mime_type="application/json",
        response_schema={
            "type": "object",
            "properties": {
                "story_title": {"type": "string"},
                "art_style": {"type": "string"},
                "era_and_region": {"type": "string"},
                "characters": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "variation": {"type": "string"}
                        },
                        "required": ["name", "description", "variation"]
                    }
                },
                "negative_prompts": {"type": "string"}
            },
            "required": ["story_title", "art_style", "era_and_region", "characters", "negative_prompts"]
        }
    )
    
    # Create the base chain
    base_chain = RunnablePassthrough() | step1_prompt | llm

    result = base_chain.invoke(story_text)
    # Extract the content from the AI message
    ai_message_content = result.content

    # Parse the JSON content and verify it matches the schema
    ai_message_content_json = json.loads(ai_message_content)
    
    # Verify required fields are present
    required_fields = ["story_title", "art_style", "era_and_region", "characters", "negative_prompts"]
    for field in required_fields:
        if field not in ai_message_content_json:
            raise ValueError(f"Required field '{field}' missing from LLM response")
    
    # Update the state with the parsed JSON result
    conversation_entry = {
        "step": "step1",
        "input": story_text,
        "output": ai_message_content,
        "raw_output": result,
    }
    return {"story_unified_prompts": ai_message_content_json, 
            "conversation_history": [conversation_entry]}
    
