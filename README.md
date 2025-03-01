# Modular LLM Workflow Engine

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-green)

A language processing system with modular workflows and LLM-agnostic architecture for product information handling.

## 🚀 Installation

### Linux/MacOS Setup
```bash
# Clone repository
git clone https://github.com/your-repo/product-workflows.git
cd product-workflows

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .

# Install langgraph development tools (optional)
pip install "langgraph[dev]"
```

## ⚙️ Configuration
Create `.env` file in project root:
```ini
PROJECT_ID="your-gcp-project"
LOCATION="your-gcp-region"
STAGING_BUCKET="gs://your-bucket"
LLM_PROVIDER="vertexai"  # or "openai"
```

## 📖 Basic Usage
```python
from core.workflows.app import SimpleLangGraphApp

# Initialize with VertexAI
app = SimpleLangGraphApp(
    project="your-project",
    location="us-central1",
    provider="vertexai"
)
app.set_up()

# Execute product query
response = app.query("Get details for premium headphones")
print(response)
```

## 🏗 Project Structure
```
src/
├── core/
│   ├── nodes/           # Processing components
│   │   ├── routing.py    # Message routing logic
│   │   ├── tools/        # Custom tools
│   │   └── output.py     # Response formatting
│   └── workflows/       # Workflow definitions
│       └── product_workflow.py  # Main workflow graph
├── providers/           # LLM integrations
│   └── llm_factory.py   # Provider switching
├── config/              # Environment setup
├── main.py              # Main entry point for CLI execution
└── agent.py             # Entry point for langgraph dev server
```

## 🔄 Workflow Flow
```
1. Input Reception → 2. Model Routing
       ↓
4. Output Formatting ← 3. Tool Execution
```

Key processing stages:
1. **Model Routing**: LLM decides between direct response or tool usage
2. **Tool Execution**: Product details retrieval from knowledge base
3. **Response Formatting**: Final output standardization

## ✨ Features
- **LLM Flexibility**: Switch between VertexAI/OpenAI via config
- **Modular Design**: Add new nodes without affecting existing flows
- **Structured Outputs**: Consistent formatting for API consumption
- **Tool System**: Extendable product information base
- **Local Testing**: Console interface for workflow validation

## 🛠 Development
```bash
# Run main application (CLI mode)
python -m src.main

# Run interactive development server
langgraph dev src.agent:graph

# Execute tests
pytest tests/ -v

# Generate coverage report
coverage run -m pytest tests/
coverage report
```

### Entry Points
The project has two main entry points:

1. **src/main.py**: Command-line interface for running predefined test queries
   - Use this for quick testing and batch processing
   - Run with `python -m src.main`

2. **src/agent.py**: Exposes the workflow graph for the LangGraph development server
   - Use this for interactive debugging and visualization
   - Run with `langgraph dev src.agent:graph`
   - Access the web interface at http://localhost:3000

## 📜 License
Apache 2.0 - See [LICENSE](LICENSE) for details
