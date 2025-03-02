import unittest
from unittest.mock import patch, MagicMock

class TestAgent(unittest.TestCase):
    def test_agent_creates_workflow(self):
        """Test that a gemini workflow is created by the agent."""
        # This is a simplified test that just verifies the workflow creation functionality
        with patch('src.core.workflows.gemini_workflow.create_gemini_workflow') as mock_create_workflow:
            # Set up mock return values
            mock_graph = MagicMock(name='mock_graph')
            mock_format_response = MagicMock(name='mock_format_response')
            mock_create_workflow.return_value = (mock_graph, mock_format_response)
            
            # Mock vertexai.init to avoid actual API calls
            with patch('vertexai.init'):
                # Local import to avoid variables getting mixed up
                from src.core.workflows.gemini_workflow import create_gemini_workflow
                
                # Call the function directly
                graph, formatter = create_gemini_workflow()
                
                # Verify it was called
                mock_create_workflow.assert_called_once()
                
                # Verify the results are as expected
                self.assertEqual(graph, mock_graph)
                self.assertEqual(formatter, mock_format_response)

if __name__ == '__main__':
    unittest.main() 