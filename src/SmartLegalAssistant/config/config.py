
"""
Configuration settings for the RAG application.
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Default configuration values
DEFAULT_CONFIG = {
    # API Keys
    "TOGETHER_API_KEY": os.environ.get("TOGETHER_API_KEY", ""),
    "PINECONE_API_KEY": os.environ.get("PINECONE_API_KEY", ""),
    "PINECONE_ENVIRONMENT": os.environ.get("PINECONE_ENVIRONMENT", ""),
    
    # Vector store settings
    "VECTOR_STORE_TYPE": "pinecone",
    "PINECONE_INDEX_NAME": os.environ.get("PINECONE_INDEX_NAME", ""),
    "PINECONE_NAMESPACE": os.environ.get("PINECONE_NAMESPACE", ""),
    
    # Embedding model settings
    "EMBEDDING_MODEL_TYPE": "together",
    "EMBEDDING_MODEL_NAME": "BAAI/bge-large-en-v1.5",
    
    # LLM settings
    "LLM_TYPE": "together",
    "LLM_MODEL_NAME": "mistralai/Mistral-Small-24B-Instruct-2501",
    "LLM_TEMPERATURE": 0.2,
    
    # Retrieval settings
    "DEFAULT_TOP_K": 40,
    "USE_QUERY_EXPANSION": False,
    "USE_RERANKING": False,
    
    # Prompt template settings
    "DEFAULT_PROMPT_TEMPLATE": "factual_qa",
    
    # Logging settings
    "LOG_LEVEL": "INFO",
    "LOG_DIR": "logs",
    
    # Application settings
    "APP_NAME": "RAG Assistant",
    "APP_DESCRIPTION": "Retrieve and answer questions from your documents",
    "DEFAULT_PAGE_TITLE": "RAG Assistant",
    "MAX_HISTORY_LENGTH": 10,
    
    # Advanced retrieval settings
    "CHUNK_SIZE": 500,
    "CHUNK_OVERLAP": 50,
    "BM25_WEIGHT": 0.2,  # For hybrid search
}

class Config:
    """Configuration manager for the application."""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure one config instance."""
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._config = DEFAULT_CONFIG.copy()
        return cls._instance
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key doesn't exist
            
        Returns:
            Configuration value
        """
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value
    
    def update(self, config_dict: Dict[str, Any]) -> None:
        """Update multiple configuration values.
        
        Args:
            config_dict: Dictionary of configuration keys and values
        """
        self._config.update(config_dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Get the complete configuration as a dictionary.
        
        Returns:
            Configuration dictionary
        """
        return self._config.copy()
    
    
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
        
        for key in required_keys:
            if not self._config.get(key):
                print(f"Missing required configuration: {key}")
                return False
        
        return True
    
    def get_embedding_config(self) -> Dict[str, Any]:
        """Get embedding model configuration.
        
        Returns:
            Embedding model configuration
        """
        return {
            "model_type": self.get("EMBEDDING_MODEL_TYPE"),
            "model_name": self.get("EMBEDDING_MODEL_NAME"),
            "api_key": self.get("TOGETHER_API_KEY")
        }
    
    def get_vector_store_config(self) -> Dict[str, Any]:
        """Get vector store configuration.
        
        Returns:
            Vector store configuration
        """
        return {
            "store_type": self.get("VECTOR_STORE_TYPE"),
            "index_name": self.get("PINECONE_INDEX_NAME"),
            "namespace": self.get("PINECONE_NAMESPACE"),
            "api_key": self.get("PINECONE_API_KEY"),
            "environment": self.get("PINECONE_ENVIRONMENT")
        }
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get language model configuration.
        
        Returns:
            Language model configuration
        """
        return {
            "model_type": self.get("LLM_TYPE"),
            "model_name": self.get("LLM_MODEL_NAME"),
            "api_key": self.get("TOGETHER_API_KEY"),
            "temperature": self.get("LLM_TEMPERATURE")
        }