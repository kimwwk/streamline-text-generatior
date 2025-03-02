from langchain_core.prompts import ChatPromptTemplate

SYSTEM_STEP2 = """**I want to create and streamline a 20-scene storyboard for a storybook.**

**Because I need to keep costs and effort low with minimal technical overhead,** I’m going for “low coherent” images—just enough detail to illustrate each scene without heavy post-processing or extensive prompt engineering.

I have all my plan below. **My request** is, Please confirm you understand the plan and generate only 20 scene prompts for the story. Use the unified text (story title, art style, era, character definitions) as contextual guidance to ensure consistency, but do not repeat them in the output. The final output should follow the "Scene Prompt Format" and include only the scene-specific details (items 1-6).

## Pre Scene Generation Definition

please make use of below information.

1.  design the unified text to be potentially included in all scene.
{story_unified_text}
2.  design various unified camera angle so that the scene can choose the most appropriate one to use.
    - medium shots are standard
    - wide shots for prominent environment
    - close-up for important props or character(s)
    - slight Dutch angle for dramatic moments

## **Scene Prompt Format**

For each scene, please provide detailed yet concise descriptions for the following items:

1. **Scene Number**

   - Example: `1`

2. **Scene Title**

   - Example: `"A Royal Awakening"`

3. **Scene Summary**

   - A brief narrative or mood description in 1-2 sentences.
   - Example: `"The princess awakens at dawn in her tower room, gazing out of the window as she contemplates the day ahead."`

4. **Camera / Vantage**

   - Specify the camera angle or focus in a short instruction.
   - Example: `"Medium shot focusing on the princess and the tower room interior."`

5. **Character Details (If any)**

   - Provide the following for **at most one character** featured in the scene:
     - **Name**: E.g., `"The Proud Princess"`
     - **Variation**: E.g., `"Default"`
     - **Expression**: E.g., `"eyes wide with excitement,"` `"with a thoughtful gaze."`
     - **Pose** (if applicable): E.g., `"standing at the window,"` `"seated on the bed."`
     - **Props** (if any): E.g., `"holding a diary,"` `"with a crown placed nearby."`

6. **Environment / Background Settings**
   - Describe the location, time of day, and key background elements briefly but vividly.
   - Example: `"A sunlit tower room with pastel walls, a wooden bed, and an open window letting in soft morning light."`

### Important Notes

- When generating any prompts, you should not put the name of the character(s) because image generation models are not able to recognize it.
- When generating any prompts, do not mention thing irrelavant to the scene. For examples, what is the character(s) thinking.
- When generating "Environment/Background Settings", ensure color palette or lighting mention is consistent with character(s)
- When generating "Environment/Background Settings", do not add the main character(s), as the character(s) and background are generated separately.
- When generating "Environment/Background Settings", the background is relevant to the character(s). For instance, if the character is sleeping on a bed, the background should feature the bed, pillow, or soft materials, rather than a bedroom scene.
- Keep it Short, But Complete: Avoid overly long prompts. Provide just enough detail so the AI can capture the story moment.
- Understanding steps of my work flow can help you create better prompts being used to generate images.

## My Work Flow

1. Using techniques of storyboarding, create scenes to tell a story.
2. For each scene, generate "Scene Details" to create corresponding images.
3. Generate scene images one by one."""

step2_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_STEP2),
    ("human", "{story_text}")
])
