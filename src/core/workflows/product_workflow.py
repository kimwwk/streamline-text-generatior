from langgraph.graph import MessageGraph, END
from langgraph.prebuilt import ToolNode
from core.nodes.routing import route_product_request
from core.nodes.tools.product_tools import get_product_details
from core.nodes.output import format_response

def create_product_workflow(llm, tool_node_name: str = "product_tools_node"):
    """Creates a workflow for handling product-related queries."""
    builder = MessageGraph()
    
    builder.add_node("model_router", _create_model_with_tools(llm))
    builder.add_node(tool_node_name, ToolNode([get_product_details]))
    builder.add_node("format_output", format_response)
    
    builder.set_entry_point("model_router")
    builder.add_conditional_edges(
        "model_router",
        route_product_request,
        {tool_node_name: tool_node_name, "__end__": END}
    )
    builder.add_edge(tool_node_name, "format_output")
    builder.add_edge("format_output", END)
    
    return builder.compile()

def _create_model_with_tools(llm_instance):
    """Binds tools to the LLM instance."""
    return llm_instance.bind_tools([get_product_details])
