import vertexai
from core.workflows.product_workflow import create_product_workflow
from providers.llm_factory import LLMFactory
from config.settings import PROJECT_ID, LOCATION, STAGING_BUCKET, credentials

# Initialize Vertex AI
vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
    credentials=credentials
)

llm_provider = "vertexai"
llm = LLMFactory.create(llm_provider)

graph = create_product_workflow(llm)
