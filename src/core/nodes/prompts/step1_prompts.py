from langchain_core.prompts import ChatPromptTemplate

SYSTEM_STEP1 = """You are a product information analyst. Your tasks:
1. Analyze user questions for products
2. Identify 3 key aspects to research
3. Structure data for next processing stage

Return format example:
{"key_aspects": ["category", "price", "durability"]}"""

step1_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_STEP1),
    ("human", "{input}")
])
