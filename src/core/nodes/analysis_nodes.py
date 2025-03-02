from langchain_core.runnables import RunnablePassthrough
from src.providers.llm_factory import LLMFactory
from src.core.nodes.prompts import step1_prompts, step2_prompts
from typing import Dict, Any

def create_analysis_nodes(llm_provider="vertexai", model="gemini-2.0-pro-exp-02-05"):
    """Create reusable analysis nodes with configured components."""
    llm = LLMFactory.create(llm_provider, model=model)
    
    def _step1_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """First analysis step that processes the input content."""
        chain = RunnablePassthrough() | step1_prompts.step1_prompt | llm
        result = chain.invoke({"input": state["content"]})
        return {"step1_result": result.content}

    def _step2_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Second analysis step that processes the result from step 1."""
        chain = RunnablePassthrough() | step2_prompts.step2_prompt | llm
        result = chain.invoke({"input": state["step1_result"]})
        return {"step2_result": result.content}

    return _step1_node, _step2_node
