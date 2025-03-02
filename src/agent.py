from core.workflows.product_workflow import create_product_workflow
from core.workflows.gemini_workflow import create_gemini_workflow
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
graph, format_response = create_gemini_workflow()
