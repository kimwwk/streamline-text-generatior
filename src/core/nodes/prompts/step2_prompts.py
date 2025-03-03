from langchain_core.prompts import ChatPromptTemplate

SYSTEM_STEP2 = """**My request** is, using techniques of storyboarding, generate 20 scene for the story. Use "Pre Scene Generation Definition" as contextual guidance to ensure consistency. Each scene should follow the "Scene Format", that all descriptions (except scene number and title) will be taken to image generation models.

## Pre Scene Generation Definition

{story_unified_text}

**Camera Angles:** (the scene can choose the most appropriate one to use.)
- medium shots are standard
- wide shots for prominent environment
- close-up for important props or character(s)
- slight Dutch angle for dramatic moments

## Scene Format

### Scene Number

<example>
1
</example>

### Scene Title

<example>
A Royal Awakening
</example>

### Scene Description
A brief scene description in 1 sentences.

<example>The princess is reading in her tower room. </example>

### Camera / Vantage
Specify the camera angle or focus in a short instruction.

<example>Medium shot focusing on the princess and the tower room interior. </example>

### Character (If any)
Provide the following for **at most one character** featured in the scene:
- Name: <example>Princess</example>
- Variation: <example>Default</example>
- Action: <example>She smiles gentle, her eyes wide with excitement, standing at the window, holding a diary. </example>

### Environment / Background Settings
Describe the location, time of day, and key background elements briefly but vividly.

<example>A sunlit tower room with pastel walls, a wooden bed, and an open window letting in soft morning light. </example>

## Restrictions

- When generating any prompts, the scene should focus on only one single character. 
- Keep it Short, But Complete: Avoid overly long prompts. Provide just enough detail so the AI can capture the story moment.
- I need to keep costs and effort low with minimal technical overhead, I am going for "low coherent" images—just enough detail to illustrate each scene without heavy post-processing or extensive prompt engineering.

## Important Notes

- When generating any prompts, consider the integration of the scene with the storyboarding.
- When generating any prompts, do not include any characters' name, which is not able to recognize by image generation models.
- When generating any prompts, do not mention thing irrelavant to the scene. For examples, what is the character(s) thinking.
- When generating "Action" from "Character", consider the character's facial expression, pose and expression if it is relevant to the scene.
- When generating "Environment/Background Settings", do not include any main character(s).
- When generating "Environment/Background Settings", ensure color palette or lighting mention is consistent with character(s).
- When generating "Environment/Background Settings", the background is relevant to the character(s). For instance, if the character is sleeping on a bed, the background should feature the bed, pillow, or soft materials, rather than a bedroom scene.
"""

step2_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_STEP2),
    ("human", "{story_text}")
])
