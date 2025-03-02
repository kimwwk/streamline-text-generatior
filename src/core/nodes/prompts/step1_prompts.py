from langchain_core.prompts import ChatPromptTemplate

# SYSTEM_STEP1 = """You are a product information analyst. Your tasks:
# 1. Analyze user questions for products
# 2. Identify 3 key aspects to research
# 3. Structure data for next processing stage

# Return format example:
# {{
#   "key_aspects": ["category", "price", "durability"]
# }}
# """

SYSTEM_STEP1 = """I'm working on a project to automatically create storyboards for children's stories.

I need your help generating unified and general visual prompts that will directly send to an AI image generator, Flux model.

## desired output description

- **Art Style**

  - Provide a detailed description of the desired art style for the illustrations.
  - Specify textures (e.g., soft watercolor, pencil sketch, digital art), color palettes (e.g., pastel tones, vibrant primaries), and any artistic inspiration (e.g., early Disney, Mary Blair, Studio Ghibli).

- **Era and Region**

  - Describe the setting, including time period (e.g., medieval, futuristic) and cultural or geographical influences (e.g., European-inspired, tropical, desert landscape).
  - Keep it short, do not include details.

- **Characters**

  - List the main characters with unified visual descriptions.
  - Include "default" appearances and any variations for specific story events (e.g., outfits, changes in status).
  - make sure to mention the core visual features across all variations to remain consistency to ensure the AI recognizes them as the same character. For example, you can use same text to keep consistent traits like eye color, hair color, and any distinguishing marks.
  - Do not include posture or facial expression.

- **Negative Prompts**
  - Specify elements or themes that should be avoided in the illustrations.
  - Ensure consistency with the desired tone, audience appropriateness, and story context (e.g., Text, naked, nude, logo, cropped, two heads, four arms, lazy eye, blurry, unfocused, worst quality, low quality).

## desired format

- **Story Title:** [Story Title prompt]
- **Art Style:** [Art Style prompt]
- **Era and Region:** [Era and Region prompt]
  - Character 1:
    - name: [Character 1 Name]
    - description: [Character 1 description]
    - role: Default [Required default role]
  - Character 1 [Optional]:
    - name: [Character 1 Name]
    - description: [Character 1 description]
    - role: [Character 1 additional variations]
  - Character 2:
    - name: [Character 2 Name]
    - description: [Character 2 description]
    - role: Default [Required default role]
  - ...
- **Negative Prompts:** [Negative prompt]"

## important notes

- all the description will send to image generation AI directly.
- write every prompt in 1-2 sentences.
- When generating any prompts, you should not put the name of the character(s) because image generation models are not able to recognize it.
- When generating any prompts, do not mention thing irrelavant to the scene. For examples, what is the character(s) thinking.
- Aim for low-coherence images with enough detail for basic illustration.
"""

step1_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_STEP1),
    ("human", "{input}")
])
