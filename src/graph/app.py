from langchain_core.messages import HumanMessage

from core.workflows.product_workflow import create_product_workflow
from providers.llm_factory import LLMFactory

class SimpleLangGraphApp:
    def __init__(self, project: str, location: str, provider: str = "vertexai") -> None:
        self.project_id = project
        self.location = location
        self.llm_provider = provider
        self.runnable = None

    def set_up(self) -> None:
        llm = LLMFactory.create(self.llm_provider)
        self.runnable = create_product_workflow(llm)

    def query(self, message: str):
        """Query the application.

        Args:
            message: The user message.

        Returns:
            str: The LLM response.
        """
        if not self.runnable:
            raise RuntimeError("App not set up. Call set_up() first.")
            
        chat_history = self.runnable.invoke(HumanMessage(message))
        return chat_history[-1].content 
