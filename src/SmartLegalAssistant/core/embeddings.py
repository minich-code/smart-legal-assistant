
# Embeddings model for text vectorization 

import os 
from typing import List, Dict, Any 
from abc import ABC, abstractmethod
import together 

class EmbeddingsModel(ABC):
    """A base class for embedding models."""

    @abstractmethod 
    def embed(self, text: str) -> List[float]:
        """Embeds the given text into a vector representation."""

        pass 

    @abstractmethod 
    def batch_embed(self, texts: List[str]) -> List[List[float]]:
        """Embeds a batch of texts into a list of vector representations."""
        pass

    @abstractmethod 
    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """Embeds a list of documents into a list of vector representations."""

        pass 


class TogetherAIEmbeddings(EmbeddingsModel):
    """Embeddings model for text vectorization using TogetherAI."""

    def __init__(self, model_name: str = "BAAI/bge-large-en-v1.5", api_key:str = None):   
        """Initialize Together AI Embeddings model.

        Args:
            model_name (str, optional): The name of the embedding model. Defaults to "BAAI/bge-large-en-v1.5".
            api_key (str, optional): The Together AI API key for Together AI. Defaults to None. (Default to env variable)
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("TOGETHERAI_API_KEY")

        if not self.api_key:
            raise ValueError("Please provide a Together AI API key or set the TOGETHER AI_API_KEY environment variable.")


    def embed_query(self, text: str) -> List[float]:  
        """Embeds the given text into a vector representation."""

        response = self.client.Embeddings.create(
            model=self.model_name,
            input=[text]

        )
        return response["data"][0]["embedding"]
    

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """Embeds a list of documents into a list of vector representations."""

        response = self.client.Embeddings.create(
            model=self.model_name,
            input=documents

        )
        return [doc["embedding"] for doc in response["data"]]



# Factory function to get the proper embedding model 
class EmbeddingFactory:
    """ A factory class for embedding models."""

    @staticmethod
    def get_embedding_model(model_type: str = "together", **kwargs) -> EmbeddingsModel:
        """Get the embedding model based on the model type.

        Args:
            model_type (str): The type of embedding model to use. Defaults to "together".
            **kwargs: Additional keyword arguments to pass to the embedding model constructor.
        Returns:
            EmbeddingsModel: An instance of the embedding model.
        """
        if model_type == "together":
            return TogetherAIEmbeddings(**kwargs)
        
        else:
            raise ValueError(f"Unknown embedding model type: {model_type}")
        
        

        
        
        
        
