from langchain_core.runnables import RunnablePassthrough
from src.providers.llm_factory import LLMFactory
from src.core.nodes.prompts.step2_prompts import step2_prompt

def create_step2_node(llm_provider="vertexai", model="gemini-2.0-pro-exp-02-05"):
    """Create second analysis node with Gemini 1.5 Pro configuration."""
    llm = LLMFactory.create(
        provider=llm_provider,
        model=model,  # More advanced model for deeper analysis
        response_mime_type="application/json",
        response_schema={
            "type": "object",
            "properties": {
                "complex_analysis": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["complex_analysis"]
        }
    )
    
    # Create the base chain
    base_chain = RunnablePassthrough() | step2_prompt | llm
    
    # Wrap the chain to handle state updates
    def node_with_state_handling(state):
        result = base_chain.invoke(state["step1_result"])
        return {"step2_result": result, **state}
    
    return node_with_state_handling
