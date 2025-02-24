from typing import Literal
from langchain_core.messages import BaseMessage

def router(state: list[BaseMessage]) -> Literal["get_product_details", "__end__"]:
    """Initiates product details retrieval if the user asks for a product."""
    # Get the tool_calls from the last message in the conversation history.
    tool_calls = state[-1].tool_calls
    # If there are any tool_calls
    if len(tool_calls):
        # Return the name of the tool to be called
        return "get_product_details"
    else:
        # End the conversation flow.
        return "__end__" 