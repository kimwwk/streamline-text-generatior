import pytest
import sys
import os

# Add the src directory to the Python path so that imports work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define fixtures that can be reused across tests here if needed
@pytest.fixture
def mock_llm_response():
    """A fixture to provide a standard mock LLM response"""
    class MockResponse:
        def __init__(self, content="Test response"):
            self.content = content
    
    return MockResponse() 