from langchain_core.messages import BaseMessage

def format_response(state: list[BaseMessage]) -> str:
    """Formats the final response for the user."""
    return state[-1].content
