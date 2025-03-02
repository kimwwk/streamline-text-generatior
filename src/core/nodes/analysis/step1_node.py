from langchain_core.runnables import RunnablePassthrough
from src.providers.llm_factory import LLMFactory
from src.core.nodes.prompts.step1_prompts import step1_prompt

def create_step1_node(llm_provider="vertexai", model="gemini-2.0-pro-exp-02-05"):
    """Create first analysis node with Gemini Pro configuration."""
    llm = LLMFactory.create(
        provider=llm_provider,
        model=model,
        response_mime_type="application/json",
        response_schema={
            "type": "object",
            "properties": {
                "key_aspects": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["key_aspects"]
        }
    )
    
    # Create the base chain
    base_chain = RunnablePassthrough() | step1_prompt | llm
    
    # Wrap the chain to handle state updates
    def node_with_state_handling(state):
        result = base_chain.invoke(state["content"])
        return {"step1_result": result, **state}
    
    return node_with_state_handling
