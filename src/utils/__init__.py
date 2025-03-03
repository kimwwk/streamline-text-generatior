def transform_json_to_text(unified_story_prompts_json):
    """
    Transform a story prompts dictionary into readable text format.
    
    Args:
        unified_story_prompts_json (dict): Dictionary containing story prompts data
        
    Returns:
        str: Formatted text representation of the story prompts
    """
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
    # text_parts.append(f"\n**Negative Prompts:** \"{unified_story_prompts_json['negative_prompts']}\"")
    
    return "\n".join(text_parts)
