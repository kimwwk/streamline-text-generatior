import vertexai
from langchain_core.messages import HumanMessage

from core.workflows.product_workflow import create_product_workflow
from providers.llm_factory import LLMFactory
from config.settings import PROJECT_ID, LOCATION, STAGING_BUCKET, credentials

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
        """Query the application."""
        if not self.runnable:
            raise RuntimeError("App not set up. Call set_up() first.")
            
        response = self.runnable.invoke(HumanMessage(message))
        return response[-1].content

def main():
    # Initialize Vertex AI
    vertexai.init(
        project=PROJECT_ID,
        location=LOCATION,
        staging_bucket=STAGING_BUCKET,
        credentials=credentials
    )

    # Create and set up the agent
    agent = SimpleLangGraphApp(project=PROJECT_ID, location=LOCATION)
    agent.set_up()

    # Test queries
    test_queries = [
        "Get product details for shoes",
        "Get product details for coffee",
        "Get product details for smartphone",
        "Tell me about the weather"
    ]

    print("Testing local agent:")
    print("-" * 50)
    for query in test_queries:
        print(f"\nQuery: {query}")
        response = agent.query(query)
        print(f"Response: {response}")

if __name__ == "__main__":
    main() 
