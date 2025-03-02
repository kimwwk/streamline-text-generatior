from langchain_core.prompts import ChatPromptTemplate

SYSTEM_STEP2 = """**I want to create and streamline a 20-scene storyboard for a storybook.**

**My request** is, using techniques of storyboarding, generate 20 scene prompts for the story. Use "Pre Scene Generation Definition" as contextual guidance to ensure consistency. Each scene should follow the "Scene Prompt Format".

## Pre Scene Generation Definition

{story_unified_text}

**Camera Angles:** (the scene can choose the most appropriate one to use.)
- medium shots are standard
- wide shots for prominent environment
- close-up for important props or character(s)
- slight Dutch angle for dramatic moments

## Scene Prompt Format

1. **Scene Number**

<example>
1
</example>

2. **Scene Title**

<example>
A Royal Awakening
</example>

3. **Scene Description**
A brief narrative or mood description in 1-2 sentences.

<example>
The princess awakens at dawn in her tower room, gazing out of the window as she contemplates the day ahead.
</example>

4. **Camera / Vantage**
Specify the camera angle or focus in a short instruction.

<example>
Medium shot focusing on the princess and the tower room interior.
</example>

5. **Character (If any)**
Provide the following for **at most one character** featured in the scene:
- Name: <example>Princess</example>
- Variation: <example>Default</example>
- Action: <example>She smiles gentle, her eyes wide with excitement, standing at the window, holding a diary. </example>

6. **Environment / Background Settings**
Describe the location, time of day, and key background elements briefly but vividly.

<example>
A sunlit tower room with pastel walls, a wooden bed, and an open window letting in soft morning light.
</example>

### Important Notes

- When generating any prompts, you should not put the name of the character(s) because image generation models are not able to recognize it.
- When generating any prompts, do not mention thing irrelavant to the scene. For examples, what is the character(s) thinking.
- When generating "Action" from "Character", consider the character's facial expression, pose and expression if it is relevant to the scene.
- When generating "Environment/Background Settings", ensure color palette or lighting mention is consistent with character(s)
- When generating "Environment/Background Settings", do not add the main character(s), as the character(s) and background are generated separately.
- When generating "Environment/Background Settings", the background is relevant to the character(s). For instance, if the character is sleeping on a bed, the background should feature the bed, pillow, or soft materials, rather than a bedroom scene.
- Keep it Short, But Complete: Avoid overly long prompts. Provide just enough detail so the AI can capture the story moment.
- I need to keep costs and effort low with minimal technical overhead, I am going for "low coherent" images—just enough detail to illustrate each scene without heavy post-processing or extensive prompt engineering.

"""

step2_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_STEP2),
    ("human", "{story_text}")
])
