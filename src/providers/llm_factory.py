from langchain_google_vertexai import ChatVertexAI
# from langchain_openai import ChatOpenAI

class LLMFactory:
    """Factory for creating LLM instances."""
    
    SUPPORTED_PROVIDERS = ["vertexai", "openai"]
    
    @classmethod
    def create(cls, provider: str, **kwargs):
        if provider not in cls.SUPPORTED_PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}")
            
        if provider == "vertexai":
            # Extract Vertex AI specific parameters
            response_mime_type = kwargs.pop("response_mime_type", "text/plain")
            response_schema = kwargs.pop("response_schema", None)
            
            return ChatVertexAI(
                model=kwargs.get("model", "gemini-1.5-pro"),
                response_mime_type=response_mime_type,
                response_schema=response_schema
            )
        # elif provider == "openai":
        #     return ChatOpenAI(model=kwargs.get("model", "gpt-4"))
