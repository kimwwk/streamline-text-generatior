from typing import Literal
from langchain_core.messages import BaseMessage

def route_product_request(state: list[BaseMessage]) -> Literal["get_product_details", "__end__"]:
    """Routes the conversation based on whether product details are requested."""
    tool_calls = state[-1].tool_calls
    return "get_product_details" if len(tool_calls) else "__end__"
