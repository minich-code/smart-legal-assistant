

# Vector store
import os
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from pinecone import Pinecone
from dotenv import load_dotenv
from SmartLegalAssistant.utils.exception import CustomException
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Or DEBUG for more detailed output
logger = logging.getLogger(__name__)


class VectorStore(ABC):
    """Abstract base class for vector stores."""

    @abstractmethod
    def query(self, vector: List[float], top_k: int = 30, **kwargs) -> Dict[str, Any]:
        """Query the vector store for similar documents."""
        pass


class PineconeStore(VectorStore):
    """Pinecone vector store for storing and retrieving documents."""

    def __init__(self, index_name: str, namespace: str = "", api_key: str = None, environment: str = None):
        """
        Initialize Pinecone vector store.

        Args:
            index_name: Name of the Pinecone index.
            namespace: Namespace of the Pinecone index (optional).
            api_key: Pinecone API key (defaults to env variable).
            environment: Pinecone environment (defaults to env variable).
        """
        self.index_name = index_name
        self.namespace = namespace
        self.api_key = api_key or os.getenv("PINECONE_API_KEY")
        self.environment = environment or os.getenv("PINECONE_ENVIRONMENT")

        if not self.api_key:
            raise ValueError(
                "Please provide a Pinecone API key or set the PINECONE_API_KEY environment variable."
            )

        if not self.environment:
            raise ValueError(
                "Please provide a Pinecone environment or set the PINECONE_ENVIRONMENT environment variable."
            )

        try:
            # Create Pinecone client
            logger.debug("Initializing Pinecone client...")
            self.pc = Pinecone(api_key=self.api_key, environment=self.environment)

            # Debug: List available indexes
            logger.debug("Listing available Pinecone indexes...")
            available_indexes = self.pc.list_indexes()
            logger.debug(f"Available Pinecone indexes: {available_indexes.names()}")

            # Connect to existing index
            if self.index_name not in available_indexes.names():
                raise ValueError(f"Pinecone index '{self.index_name}' does not exist. Available indexes: {available_indexes.names()}")

            logger.debug(f"Connecting to Pinecone index '{self.index_name}'...")
            self.index = self.pc.Index(self.index_name)

        except Exception as e:
            raise CustomException(
                e,
                error_type="PineconeInitializationError",
                context={"index_name": self.index_name, "environment": self.environment},
                log_immediately=True,
            )

    def query(self, vector: List[float], top_k: int = 30, include_metadata: bool = True,
              filter: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Query the vector store for similar documents.

        Args:
            vector: The vector to query.
            top_k: Number of results to return. Defaults to 25.
            include_metadata: Whether to include metadata in results. Defaults to True.
            filter: Optional filter to apply to the query.

        Returns:
            A dictionary containing the query results.
        """
        query_params = {
            "vector": vector,
            "top_k": top_k,
            "include_metadata": include_metadata,
            "namespace": self.namespace
        }
        if filter:
            query_params["filter"] = filter

        try:
            logger.debug(f"Querying Pinecone index '{self.index_name}' with vector: {vector[:5]}..., top_k: {top_k}, namespace: {self.namespace}, filter: {filter}")
            result = self.index.query(**query_params)
            return result
        except Exception as e:
            raise CustomException(
                e,
                error_type="PineconeQueryError",
                context={"index_name": self.index_name, "vector": vector[:5], "top_k": top_k, "namespace": self.namespace, "filter": filter},
                log_immediately=True,
            )


# Factory function to get the right vector store
def get_vector_store(index_name: Optional[str] = None, store_type: str = "pinecone", **kwargs) -> VectorStore:
    """
    Factory function to create vector stores.

    Args:
        index_name: Name of the index to use (required for Pinecone)
        store_type: Type of vector store to use ('pinecone', etc.)
        **kwargs: Additional config for the vector store

    Returns:
        A vector store instance.
    """
    if store_type == "pinecone":
        if index_name is not None:
            kwargs["index_name"] = index_name
        return PineconeStore(**kwargs)
    else:
        raise ValueError(f"Unsupported vector store type: {store_type}")

# -----------------------------
# Test Suite (Run when executing directly)
# -----------------------------
if __name__ == "__main__":
    try:
        print("🔵 Loading environment variables...")
        load_dotenv()

        # Debug environment variables
        print(f"PINECONE_INDEX_NAME from env: {os.getenv('PINECONE_INDEX_NAME')}")

        # Use hardcoded index name if needed
        index_name = os.getenv("PINECONE_INDEX_NAME", "smart-legal")
        print(f"Using index name: {index_name}")

        print("🔵 Initializing Pinecone Vector Store...")
        vector_store = get_vector_store(
            store_type="pinecone",
            index_name=index_name
        )

        # Test 1: Check if the index exists
        print("🔵 Checking if index exists...")
        try:
            pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENVIRONMENT"))
            available_indexes = pc.list_indexes()
            if index_name in available_indexes.names():
                print(f"✅ Index '{index_name}' exists.")
            else:
                raise ValueError(f"Index '{index_name}' does not exist.")
        except Exception as e:
            raise CustomException(e, error_type="PineconeIndexCheckError", context={"index_name": index_name}, log_immediately=True)

        # Test 2: Check for a specific vector ID
        vector_id_to_check = "086b5238-dc64-478b-8e4a-b407725b319e"
        print(f"🔵 Checking for vector ID '{vector_id_to_check}'...")
        try:
            fetch_response = vector_store.index.fetch(ids=[vector_id_to_check], namespace=vector_store.namespace)
            if vector_id_to_check in fetch_response.vectors:
                print(f"✅ Vector ID '{vector_id_to_check}' found in index.")
            else:
                print(f"❌ Vector ID '{vector_id_to_check}' not found in index.")
        except Exception as e:
            raise CustomException(e, error_type="PineconeVectorCheckError", context={"index_name": index_name, "vector_id": vector_id_to_check}, log_immediately=True)

        print("\n🎯 Vector store test completed successfully!")

    except CustomException as e:
        print(f"❌ Vector store test failed: {e}")
    except Exception as e:
        print(f"❌ Vector store test failed with unexpected error: {e}")