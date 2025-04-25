

"""
Vector store integration for storing and retrieving documents focusing on Pinecone
"""

import os 
from typing import List, Dict, Any, Optional, Union
from abc import ABC, abstractmethod
import pinecone 


class VectorStore(ABC):
    """Abstract base class for vector stores."""
    @abstractmethod
    def query(self, vector: List[float], top_k: int=25, **kwargs) -> Dict[str, Any]:
        """Query the vector store for similar documents."""

        pass 

class PineconeDBStore(VectorStore):
    """Pinecone vector store for storing and retrieving documents."""

    def __init__(self, index_name: str, namespace: str = "", api_key: str = None, environment: str = None):
        
        """Initialize Pinecone vector store.
        
        Args: 
        Index_name: Name of the pinecone index 
        Namespace: Namespace of the pinecone index
        api_key: Pinecone API key (default to the env variable key)
        environment: Pinecone environment (default to the env variable)
        
        """

        self.index_name = index_name 
        self.namespace = namespace
        self.api_key = api_key or os.getenv("PINECONE_API_KEY")
        self.environment = environment or os.getenv("PINECONE_ENVIRONMENT")

        if not self.api_key or not self.environment:
            raise ValueError("Please provide a Pinecone API key and environment or set the PINECONE_API_KEY and PINECONE_ENVIRONMENT environment variables.")
        

        # Initialize the Pinecone 
        pinecone.init(api_key = self.api_key, environment = self.environment)
        self.index = pinecone.Index(self.index_name)


    def query(self, vector: List[float], top_k: int=25, include_metadata: bool = True,
              filter: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        
        """Query the vector store for similar documents.
        Args:
        vector: The vector to query.
        top_k: The number of results to return. Default is 25.
        include_metadata: Whether to include metadata in the results. Default is True.
        filter: A filter to apply to the query. Default is None.

        Returns:
        A dictionary containing the query results.       
        
        """
        query_params = {
            "top_k": top_k,
            "include_metadata": include_metadata,
            "vector": vector,
            "namespace": self.namespace
        }
        if filter:
            query_params = {"filter": filter}
            

        return self.index.query(**query_params)

class vectorstorefactory:
    """Factory class for vector stores."""
    @staticmethod
    def get_vector_store(store_type: str = "pinecone", **kwargs) -> VectorStore:
        """Get a vector store instance based on the provided index name.
        
        Args:
        store_type (str): Types of vector store to use ie. (Pinecone, FAISS, DataStax, Weaviate)
        index_name (str): Name of the index
        **kwargs : Additional keyword arguments to pass to the vector store constructor.
        
        Returns:
        vectorstore: An instance of the vector store.
        
        """

        if store_type == "pinecone":
            return PineconeDBStore(**kwargs)

        else:
            raise ValueError(f"Unknown vector store type: {store_type}")
        
    
        

