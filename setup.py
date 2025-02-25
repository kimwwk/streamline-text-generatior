from setuptools import setup, find_packages

setup(
    name="langgraph_local",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "google-cloud-aiplatform[langchain,reasoningengine]",
        "cloudpickle==3.0.0",
        "pydantic==2.7.4",
        "langgraph",
        "httpx",
        "python-dotenv",
        "openai>=1.0.0",
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
        "typing-extensions>=4.0.0",
        "networkx>=3.0",
        "graphviz>=0.20.0"
    ],
    python_requires=">=3.9",
    description="A modular language processing system with LLM-agnostic architecture",
    author="Your Name", 
    license="Apache 2.0",
)
