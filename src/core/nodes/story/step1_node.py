from langchain_core.runnables import RunnablePassthrough
from src.providers.llm_factory import LLMFactory
from src.core.nodes.prompts.step1_prompts import step1_prompt


    
def create_step1_node(story_text,llm_provider="vertexai", model="gemini-2.0-pro-exp-02-05"):
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
                            "role": {"type": "string"}
                        },
                        "required": ["name", "description"]
                    }
                },
                "negative_prompts": {"type": "string"}
            },
            "required": ["story_title", "art_style", "era_and_region", "characters", "negative_prompts"]
        }
    )
    
    # Create the base chain
    base_chain = RunnablePassthrough() | step1_prompt | llm
    
    # Wrap the chain to handle state updates
    def node_with_state_handling(state):
        result = base_chain.invoke(story_text)
        # Extract the content from the AI message
        content = result.content

        return {"step1_result": content, 
                "metadata": result,
                **state}
    
    return node_with_state_handling
