

"""
Configuration with Cohere API key.
"""
# Add this to the DEFAULT_CONFIG dictionary in config.py
DEFAULT_CONFIG = {
    # Existing configuration...
    
    # Cohere settings
    "COHERE_API_KEY": os.environ.get("COHERE_API_KEY", ""),
    "USE_COHERE_RERANK": True,
    "COHERE_RERANK_MODEL": "rerank-multilingual-v2.0",
    
    # Other existing configuration...
}

# Also update the validate method to check for Cohere API key when reranking is enabled
def validate(self) -> bool:
    """Validate the configuration.
    
    Returns:
        True if configuration is valid, False otherwise
    """
    required_keys = [
        "TOGETHER_API_KEY",
        "PINECONE_API_KEY",
        "PINECONE_ENVIRONMENT",
        "PINECONE_INDEX_NAME"
    ]
    
    # Add Cohere API key to required keys if Cohere reranking is enabled
    if self._config.get("USE_COHERE_RERANK", False):
        required_keys.append("COHERE_API_KEY")
    
    for key in required_keys:
        if not self._config.get(key):
            print(f"Missing required configuration: {key}")
            return False
    
    return True