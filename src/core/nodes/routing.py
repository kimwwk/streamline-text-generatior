from typing import Literal
from langchain_core.messages import BaseMessage

def route_product_request(state: list[BaseMessage]) -> Literal["product_tools_node", "__end__"]:
    """Routes the conversation based on whether product details are requested."""
    tool_calls = state[-1].tool_calls
    return "product_tools_node" if len(tool_calls) else "__end__"
