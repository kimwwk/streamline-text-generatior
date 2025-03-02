from langchain_core.runnables import RunnablePassthrough
from src.providers.llm_factory import LLMFactory
from src.core.nodes.prompts.step2_prompts import step2_prompt
import json

# example step1_result
# {
#   "art_style": "Soft watercolor textures with pastel tones, reminiscent of early Disney animation, with a touch of Studio Ghibli's whimsical charm. The color palette will include gentle blues, soft pinks, and warm yellows to create a dreamy and inviting atmosphere.",
#   "characters": [
#     {
#       "description": "A young woman with long, golden-blonde hair, blue eyes, and fair skin, wearing a simple, elegant medieval-style gown in light blue with delicate white trim.",
#       "name": "Princess",
#       "role": "Default"
#     },
#     {
#       "description": "A young woman with long, golden-blonde hair, blue eyes and fair skin, wearing dirty and tattered servant's clothes made of rough brown fabric.",
#       "name": "Princess",
#       "role": "Kitchen Maid"
#     },
#      {
#       "description": "A young woman with long, golden-blonde hair, blue eyes, and fair skin, wearing the most splendid clothing, include luxury dress and jewelry.",
#       "name": "Princess",
#       "role": "Married"
#     },
#     {
#       "description": "A tall, slender man with a crooked chin, brown hair, and brown eyes, wearing regal attire consisting of a rich, dark red tunic and a golden crown.",
#       "name": "King Thrushbeard",
#       "role": "Default"
#     },
#     {
#       "description": "A slender man with a crooked chin, brown hair, and brown eyes, dressed in dirty, ragged clothes of a traveling musician, carrying a fiddle.",
#       "name": "King Thrushbeard",
#       "role": "Fiddler"
#     },
#       {
#       "description": "A slender man with a crooked chin, brown hair, and brown eyes, wearing velvet and silk, with gold chains about his neck.",
#       "name": "King Thrushbeard",
#       "role": "King's son"
#     },
#     {
#       "description": "An older man with graying hair, kind eyes, and a stern but gentle expression, wearing royal attire with a golden crown.",
#       "name": "Old King",
#       "role": "Default"
#     }
#   ],
#   "era_and_region": "Medieval period with European-inspired settings, featuring castles, forests, meadows, and a small village.",
#   "negative_prompts": "Text, naked, nude, logo, cropped, two heads, four arms, lazy eye, blurry, unfocused, worst quality, low quality",
#   "story_title": "King Thrushbeard"
# }

def transform_step1_result(step1_result):
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
        step1_result = state["step1_result"]

        # Convert step1_result to JSON if it's not already
        if not isinstance(state["step1_result"], dict):
            step1_result = json.loads(step1_result)
        
        # print("step1_result value:", state["step1_result"])
        story_unified_text = transform_step1_result(step1_result)
        
        result = base_chain.invoke({"story_text": story_text, "story_unified_text": story_unified_text})
        # Extract the content from the AI message
        result = result.content
        
        return {"step2_result": result, **state}
    
    return node_with_state_handling
