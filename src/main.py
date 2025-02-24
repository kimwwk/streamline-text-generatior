import vertexai
from config.settings import PROJECT_ID, LOCATION, STAGING_BUCKET, credentials
from graph.app import SimpleLangGraphApp

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