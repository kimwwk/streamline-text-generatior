import unittest
from unittest.mock import patch, MagicMock

from src.core.nodes.analysis_nodes import create_analysis_nodes


class TestAnalysisNodes(unittest.TestCase):
    
    @patch('src.core.nodes.analysis_nodes.LLMFactory')
    @patch('src.core.nodes.analysis_nodes.RunnablePassthrough')
    @patch('src.core.nodes.analysis_nodes.step1_prompts')
    @patch('src.core.nodes.analysis_nodes.step2_prompts')
    def test_create_analysis_nodes(self, mock_step2_prompts, mock_step1_prompts, 
                                  mock_runnable_passthrough, mock_llm_factory):
        # Set up mocks
        mock_llm = MagicMock()
        mock_llm_factory.create.return_value = mock_llm
        
        mock_step1_prompt = MagicMock()
        mock_step1_prompts.step1_prompt = mock_step1_prompt
        
        mock_step2_prompt = MagicMock()
        mock_step2_prompts.step2_prompt = mock_step2_prompt
        
        mock_runnable = MagicMock()
        mock_runnable_passthrough.return_value = mock_runnable
        mock_runnable.__or__.return_value = mock_runnable
        
        # Create the analysis nodes
        step1_node, step2_node = create_analysis_nodes()
        
        # Assert LLMFactory was called with correct parameters
        mock_llm_factory.create.assert_called_once_with("vertexai", model="gemini-2.0-pro-exp-02-05")
        
        # Test step1_node
        mock_result = MagicMock()
        mock_result.content = "Step 1 analysis result"
        mock_runnable.invoke.return_value = mock_result
        
        state = MagicMock()
        state.content = "Test input"
        
        result = step1_node(state)
        
        # Check that the runnable was invoked with the correct input
        mock_runnable.invoke.assert_called_with({"input": "Test input"})
        
        # Check that the result is correct
        self.assertEqual(result, {"step1_result": "Step 1 analysis result"})
        
        # Test step2_node
        mock_result.content = "Step 2 analysis result"
        
        state = {"step1_result": "Step 1 result"}
        result = step2_node(state)
        
        # Check that the runnable was invoked with the correct input
        mock_runnable.invoke.assert_called_with({"input": "Step 1 result"})
        
        # Check that the result is correct
        self.assertEqual(result, {"step2_result": "Step 2 analysis result"})
    
    @patch('src.core.nodes.analysis_nodes.LLMFactory')
    def test_create_analysis_nodes_custom_provider(self, mock_llm_factory):
        # Set up mocks
        mock_llm = MagicMock()
        mock_llm_factory.create.return_value = mock_llm
        
        # Create the analysis nodes with custom provider and model
        create_analysis_nodes(llm_provider="openai", model="gpt-4-turbo")
        
        # Assert LLMFactory was called with correct parameters
        mock_llm_factory.create.assert_called_once_with("openai", model="gpt-4-turbo")


if __name__ == '__main__':
    unittest.main() 