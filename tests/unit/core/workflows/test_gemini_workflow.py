import unittest
from unittest.mock import patch, MagicMock
from langgraph.graph import StateGraph, END

from src.core.workflows.gemini_workflow import create_gemini_workflow


class TestGeminiWorkflow(unittest.TestCase):
    
    @patch('src.core.workflows.gemini_workflow.create_analysis_nodes')
    @patch('src.core.workflows.gemini_workflow.format_response')
    def test_create_gemini_workflow(self, mock_format_response, mock_create_analysis_nodes):
        # Create mock step functions
        mock_step1 = MagicMock()
        mock_step2 = MagicMock()
        mock_create_analysis_nodes.return_value = (mock_step1, mock_step2)
        
        # Set up mock format_response
        mock_format_response_fn = MagicMock()
        mock_format_response.return_value = mock_format_response_fn
        
        # Create a mock StateGraph to verify it's being configured correctly
        mock_workflow = MagicMock(spec=StateGraph)
        
        with patch('src.core.workflows.gemini_workflow.StateGraph', return_value=mock_workflow) as mock_state_graph:
            workflow, response_formatter = create_gemini_workflow()
            
            # Assert StateGraph was created with the correct parameters
            mock_state_graph.assert_called_once_with(dict)
            
            # Assert nodes were added correctly
            mock_workflow.add_node.assert_any_call("step1", mock_step1)
            mock_workflow.add_node.assert_any_call("step2", mock_step2)
            
            # Assert entry point was set correctly
            mock_workflow.set_entry_point.assert_called_once_with("step1")
            
            # Assert edges were created correctly
            mock_workflow.add_edge.assert_any_call("step1", "step2")
            mock_workflow.add_edge.assert_any_call("step2", END)
            
            # Assert the returned objects are correct
            self.assertEqual(workflow, mock_workflow)
            self.assertEqual(response_formatter, mock_format_response)


if __name__ == '__main__':
    unittest.main() 