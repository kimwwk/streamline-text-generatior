from core.workflows.product_workflow import create_product_workflow
from core.workflows.gemini_workflow import create_gemini_workflow, GeminiState
from providers.llm_factory import LLMFactory
from config.settings import PROJECT_ID, LOCATION, STAGING_BUCKET, credentials
import vertexai

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
    credentials=credentials
)

# Create Gemini-specific workflow
graph = create_gemini_workflow()

# Example of how to use the graph with the typed state
def process_with_gemini(input_text: str):
    """Process input text using the Gemini workflow."""
    # Initialize the state with proper typing based on GeminiState
    initial_state = {"content": input_text, "metadata": {}}
    
    # Execute the workflow
    result = graph.invoke(initial_state)
    
    # Access the final result
    return result.get("step2_result", "No result found")

# Example usage
if __name__ == "__main__":
    sample_input = "This is a sample text to analyze."
    result = process_with_gemini(sample_input)
    print(f"Analysis result: {result}")
