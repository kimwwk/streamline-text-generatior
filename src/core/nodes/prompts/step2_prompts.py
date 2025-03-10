from langchain_core.prompts import ChatPromptTemplate

SYSTEM_STEP2 = """**Task**: Generate a complete 20-scene storyboard for a children's story using the provided definitions and story elements. Each scene will be directly used for image generation, so follow the format precisely.

## Unified Visual Style

{story_unified_text}

## Storyboard Requirements

- Generate exactly 20 scenes that tell a complete story
- Scenes should follow a clear narrative arc (introduction, rising action, climax, resolution)
- Each scene should be visually distinct while maintaining style consistency
- Each scene is a still image
- Each scene can only include one character. Do not even mention a second character in the scene.
- Ensure all scenes together tell a cohesive story with proper progression
- When mentioning as **Self-contained Descriptions**, it: 
   - MUST work as standalone prompts for image generation
   - NEVER use phrases like "Same" or "Similar to previous scene" 
   - NEVER use the name of the character like "Princess Amelia", "King's Daughter", etc.
   - NEVER include anything that cannot be visually represented like "thoughts", "feelings", "saying something", etc.
   - NEVER include anything tha is ambiguous, vague, or unclear

## Camera Angles Reference
- Medium shots: Standard for character introductions and dialogue
- Wide shots: For establishing locations or showing environment details
- Close-up shots: For emotional moments, important objects, or character expressions
- Dutch angle (slight tilt): For moments of tension or excitement

## Scene Format

Each scene must follow this exact format:

### Scene Number
A number from 1 to 20 indicating the scene's position in the sequence.

<example>
1
</example>

### Scene Title
A brief, descriptive title (3-7 words) that captures the essence of the scene.

<example>
A Royal Awakening
</example>

### Scene Description
**Self-contained Descriptions**: A single, concise sentence describing the key action or moment in the scene.

<example>The princess discovers a magical map hidden inside her favorite book.</example>

### Camera / Vantage
**Self-contained Descriptions**: A clear instruction for camera positioning and focus (use reference angles).

<example>Medium shot focusing on the princess and the open book in her hands.</example>

### Character (If any)
Details about the primary character in this scene:

- Name: match the name in the character from Unified Visual Style <example>Princess Amelia</example>
- Variation: match the variation in the character from Unified Visual Style <example>Default</example>
- Action: **Self-contained Descriptions** <example>Her eyes wide with wonder, gently touching the glowing map with her fingertips, leaning forward with curiosity.</example>

### Environment / Background Settings
**Self-contained Descriptions**: A vivid but concise description of the setting, atmosphere, and key background elements.

<example>A cozy tower room bathed in golden afternoon light, bookshelves lining the walls, dust particles dancing in sunbeams, with a large arched window revealing a distant mountain range.</example>

## Output Format
The output must be a valid JSON array with 20 objects, each containing scene_number, title, description, camera, character (with name, variation, action), and background fields.
"""

step2_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_STEP2),
    ("human", "{story_text}")
])
