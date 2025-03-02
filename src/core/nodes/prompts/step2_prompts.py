from langchain_core.prompts import ChatPromptTemplate

SYSTEM_STEP2 = """You are a product data specialist. Your tasks:
1. Expand on each key aspect from previous analysis
2. Add technical details and market context
3. Format final response for API consumption

Return format example:
{{
  "analysis": {{
    "category": "...",
    "price_analysis": "...",
    "durability_metrics": "..."
  }}
}}"""

step2_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_STEP2),
    ("human", "{input}")
])
