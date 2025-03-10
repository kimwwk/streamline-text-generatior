from core.workflows.product_workflow import create_product_workflow
from src.core.workflows.story_workflow import create_story_workflow, StoryState
from providers.llm_factory import LLMFactory
from config.settings import PROJECT_ID, LOCATION, STAGING_BUCKET, credentials
import vertexai

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    credentials=credentials
)

# Create Story-specific workflow
graph = create_story_workflow()

# Example of how to use the graph with the typed state
def process_with_story(input_text: str):
    """Process input text using the Story workflow."""
    # Initialize the state with proper typing based on StoryState
    initial_state = {"content": input_text, "metadata": {}}
    
    # Execute the workflow
    result = graph.invoke(initial_state)
    
    # Access the final result
    return result.get("step2_result", "No result found")

# Example usage
if __name__ == "__main__":
    sample_input = "This is a sample text to analyze."
    result = process_with_story(sample_input)
    print(f"Analysis result: {result}")
