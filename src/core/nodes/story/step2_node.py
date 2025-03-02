from langchain_core.runnables import RunnablePassthrough
from src.providers.llm_factory import LLMFactory
from src.core.nodes.prompts.step2_prompts import step2_prompt

def transform_json_to_text(step1_result):
    """Transform step1 result dictionary into readable text format."""
    text_parts = []
    
    # Add story title
    text_parts.append(f"**Story Title:** {step1_result['story_title']}\n")
    
    # Add art style
    text_parts.append(f"**Art Style:** {step1_result['art_style']}\n")
    
    # Add era and region
    text_parts.append(f"**Era and Region:** {step1_result['era_and_region']}\n")
    
    # Add characters section
    text_parts.append("**Characters:**\n")
    
    # Group characters by name
    characters_by_name = {}
    for char in step1_result['characters']:
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
                text_parts.append(f"  - Default: \"{desc}\"\n")
            else:
                text_parts.append(f"  - **{role} Variation:** \"{desc}\"\n")
    
    # Add negative prompts
    text_parts.append(f"\n**Negative Prompts:** \"{step1_result['negative_prompts']}\"")
    
    return "\n".join(text_parts)


def create_step2_node(story_text, llm_provider="vertexai", model="gemini-2.0-pro-exp-02-05"):
    """Create second analysis node with Gemini 1.5 Pro configuration."""
    llm = LLMFactory.create(
        provider=llm_provider,
        model=model,  # More advanced model for deeper analysis
        # response_mime_type="application/json",
    )
    
    # Create the base chain
    base_chain = RunnablePassthrough() | step2_prompt | llm
    
    # Wrap the chain to handle state updates
    def node_with_state_handling(state):
        story_unified_text = transform_json_to_text(state["unified_story_prompts"])
        
        result = base_chain.invoke({"story_text": story_text, "story_unified_text": story_unified_text})
        # Extract the content from the AI message
        ai_message_content = result.content

        conversation_entry = {
            "step": "step2",
            "input": story_text,
            "output": ai_message_content,
            "raw_output": result,
        }

        return {"step2_result": result, 
                "conversation_history": conversation_entry,
                **state}
    
    return node_with_state_handling
