from langgraph.graph import MessageGraph, END
from langgraph.prebuilt import ToolNode
from core.nodes.routing import route_product_request
from tools.product_tools import get_product_details

def create_product_workflow(llm, tool_node_name: str = "product_tools"):
    """Creates a workflow for handling product-related queries."""
    builder = MessageGraph()
    
    builder.add_node("model_router", _create_model_with_tools(llm))
    builder.add_node("tool_executor", ToolNode([get_product_details]))
    
    builder.set_entry_point("model_router")
    builder.add_conditional_edges(
        "model_router",
        route_product_request,
        {tool_node_name: "tool_executor", "__end__": END}
    )
    builder.add_edge("tool_executor", END)
    
    return builder.compile()

def _create_model_with_tools(llm_instance):
    """Binds tools to the LLM instance."""
    return llm_instance.bind_tools([get_product_details])
