from langchain_core.runnables import RunnablePassthrough
from src.providers.llm_factory import LLMFactory
from src.core.nodes.prompts.step2_prompts import step2_prompt
import json
def transform_json_to_text(unified_story_prompts_json):
    """Transform step1 result dictionary into readable text format."""
    text_parts = []
    
    # Add story title
    text_parts.append(f"**Story Title:** {unified_story_prompts_json['story_title']}\n")
    
    # Add art style
    text_parts.append(f"**Art Style:** {unified_story_prompts_json['art_style']}\n")
    
    # Add era and region
    text_parts.append(f"**Era and Region:** {unified_story_prompts_json['era_and_region']}\n")
    
    # Add characters section
    text_parts.append("**Characters:**\n")
    
    # Group characters by name
    characters_by_name = {}
    for char in unified_story_prompts_json['characters']:
        if char['name'] not in characters_by_name:
            characters_by_name[char['name']] = []
        characters_by_name[char['name']].append(char)
    
    # Format each character group
    for name, variations in characters_by_name.items():
        text_parts.append(f"- **{name}:**\n")
        for var in variations:
            role = var['role']
            desc = var['description']
            if role == "Default":
                text_parts.append(f"  - Default Variation: \"{desc}\"\n")
            else:
                text_parts.append(f"  - {role} Variation: \"{desc}\"\n")
    
    # Add negative prompts
    text_parts.append(f"\n**Negative Prompts:** \"{unified_story_prompts_json['negative_prompts']}\"")
    
    return "\n".join(text_parts)


def create_step2_node(story_text, llm_provider="vertexai", model="gemini-2.0-pro-exp-02-05"):
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
    
    # Wrap the chain to handle state updates
    def node_with_state_handling(state):
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

        output = {
            "unified_text": state["story_unified_prompts"],
            "scenes": ai_message_content_json
        }

        return {"output_v1": output, 
                "scenes": ai_message_content_json,
                "conversation_history": [conversation_entry]}
    
    return node_with_state_handling
