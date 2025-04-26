

# Embeddings model for text vectorization

import os
from typing import List
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from together import Together
from SmartLegalAssistant.utils.exception import CustomException

# Load environment variables from .env
load_dotenv()

class EmbeddingModel(ABC):
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


class TogetherAIEmbeddings(EmbeddingModel):
    """Embeddings model for text vectorization using TogetherAI."""

    def __init__(self, model_name: str = "BAAI/bge-large-en-v1.5", api_key: str = None):
        """Initialize Together AI Embeddings model."""
        self.model_name = model_name
        self.api_key = api_key or os.getenv("TOGETHER_AI_API_KEY")
        self.client = None  # Initialize client to None

        if not self.api_key:
            raise ValueError(
                "Please provide a Together AI API key or set the TOGETHER_AI_API_KEY environment variable."
            )

        try:
            self.client = Together(api_key=self.api_key)
        except Exception as e:
            raise CustomException(
                e,
                error_type="TogetherAIInitializationError",
                context={"model_name": self.model_name},
                log_immediately=True,
            )

    def embed(self, text: str) -> List[float]:
        """Embeds the given text into a vector representation."""
        return self.embed_query(text)

    def batch_embed(self, texts: List[str]) -> List[List[float]]:
        """Embeds a batch of texts into a list of vector representations."""
        return self.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        """Embeds the given text into a vector representation."""
        try:
            response = self.client.embeddings.create(
                model=self.model_name,
                input=[text]
            )
            return response.data[0].embedding
        except Exception as e:
            raise CustomException(
                e,
                error_type="TogetherAIEmbeddingError",
                context={"model_name": self.model_name, "input_text": text},
                log_immediately=True,
            )

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """Embeds a list of documents into a list of vector representations."""
        try:
            response = self.client.embeddings.create(
                model=self.model_name,
                input=documents
            )
            return [doc.embedding for doc in response.data]
        except Exception as e:
            raise CustomException(
                e,
                error_type="TogetherAIEmbeddingError",
                context={"model_name": self.model_name, "input_documents": documents},
                log_immediately=True,
            )


def get_embedding_model(model_type: str = "together", **kwargs) -> EmbeddingModel:
    """Factory function to create embedding models."""
    if model_type == "together":
        return TogetherAIEmbeddings(**kwargs)
    else:
        raise ValueError(f"Unsupported embedding model type: {model_type}")



# -------------------------------------------------------------------------
# ✅ Quick TEST (Runs if you directly run embeddings.py)
# -------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        print("🔵 Initializing TogetherAI Embedding model...")
        embed_model = get_embedding_model()

        # Single text embedding
        text = "Artificial Intelligence is transforming industries."
        print("🔵 Embedding single text...")
        single_embedding = embed_model.embed(text)
        assert isinstance(single_embedding, list) and len(single_embedding) > 0
        print("✅ Single text embedding successful.")

        # Batch embedding
        texts = [
            "Machine learning enables computers to learn from data.",
            "Natural language processing powers chatbots and translators."
        ]
        print("🔵 Embedding batch texts...")
        batch_embeddings = embed_model.batch_embed(texts)
        assert isinstance(batch_embeddings, list) and all(isinstance(vec, list) for vec in batch_embeddings)
        print("✅ Batch text embedding successful.")

        print("\n🎯 All tests completed successfully!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
