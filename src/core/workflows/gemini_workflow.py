from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from src.providers.llm_factory import LLMFactory
from src.nodes.prompts.step1_prompts import step1_prompt
from src.nodes.prompts.step2_prompts import step2_prompt

def format_response(state):
    return {
        "step1_analysis": state.get("step1_result"),
        "final_analysis": state.get("step2_result")
    }

def create_gemini_workflow():
    llm = LLMFactory.create("vertexai", model="gemini-2.0-pro-exp-02-05")
    
    def step1_node(state):
        result = (step1_prompt | llm).invoke({"input": state.content})
        return {"step1_result": result.content}
        
    def step2_node(state):
        result = (step2_prompt | llm).invoke({"input": state["step1_result"]})
        return {"step2_result": result.content}

    workflow = StateGraph(dict)
    workflow.add_node("step1", step1_node)
    workflow.add_node("step2", step2_node)
    workflow.set_entry_point("step1")
    workflow.add_edge("step1", "step2")
    workflow.add_edge("step2", END)
    
    return workflow, format_response
