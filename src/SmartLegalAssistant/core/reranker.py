


import os
from together import Together
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
load_dotenv()

class Reranker:
    """Base class for reranking implementations."""

    def rerank(self, query: str, documents: List[Dict[str, Any]], top_n: Optional[int]) -> List[Dict[str, Any]]:
        """Rerank the top_n documents based on the query."""
        raise NotImplementedError("Subclasses must implement the rerank method.")


class TogetherAIReranker(Reranker):
    """Reranker implementation using Together AI's Llama-Rank model."""

    def __init__(self, api_key: Optional[str] = None, model: str = "Salesforce/Llama-Rank-V1"):
        """Initialize Together AI Reranker.

        Args:
            api_key: Together AI API key
            model: Together AI reranking model to use
        """
        self.api_key = api_key or os.getenv("TOGETHER_AI_API_KEY")  # <-- Fixed here
        if not self.api_key:
            raise ValueError("Please provide a Together AI API key or set the TOGETHER_AI_API_KEY environment variable.")

        self.client = Together(api_key=self.api_key)
        self.model = model

    def rerank(self, query: str, documents: List[Dict[str, Any]], top_n: Optional[int]) -> List[Dict[str, Any]]:
        """Rerank documents using Together AI's reranker model."""
        if not documents:
            return []

        # Extract document texts
        doc_texts = [doc.get("text", "") for doc in documents]

        try:
            response = self.client.rerank.create(
                model=self.model,
                query=query,
                documents=doc_texts,
                top_n=top_n or len(doc_texts)
            )
        except Exception as e:
            print(f"Error while calling Together AI API: {e}")
            return []

        # Reorder documents based on reranking results
        reranked_docs = []
        for result in response.results:
            original_doc = documents[result.index]
            original_doc["rerank_score"] = result.relevance_score
            reranked_docs.append(original_doc)

        return reranked_docs


def get_reranker(reranker_type: str = "together_ai", **kwargs) -> Reranker:
    """Factory to get a reranker instance."""
    if reranker_type == "together_ai":
        return TogetherAIReranker(**kwargs)
    else:
        raise ValueError(f"Unknown reranker type: {reranker_type}")


# --- TEST SECTION (Together AI style example) ---

if __name__ == "__main__":
    reranker = get_reranker()

    query = "What animals can I find near Peru?"
    documents = [
        {
            "text": "The giant panda (Ailuropoda melanoleuca), also known as the panda bear or simply panda, is a bear species endemic to China."},
        {
            "text": "The llama is a domesticated South American camelid, widely used as a meat and pack animal by Andean cultures since the pre-Columbian era."},
        {
            "text": "The wild Bactrian camel (Camelus ferus) is an endangered species of camel endemic to Northwest China and southwestern Mongolia."},
        {
            "text": "The guanaco is a camelid native to South America, closely related to the llama. Guanacos are one of two wild South American camelids; the other species is the vicuña, which lives at higher elevations."},
    ]

    reranked_docs = reranker.rerank(query=query, documents=documents, top_n=2)

    for doc in reranked_docs:
        print(f"Document: {doc['text']}")
        print(f"Rerank Score: {doc['rerank_score']}")
        print("---")
