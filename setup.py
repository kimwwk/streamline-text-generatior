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
        "python-dotenv"
    ],
) 