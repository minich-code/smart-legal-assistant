
# RAG Retrieval implementation with Cohere Rerank (with Filtering)

from typing import List, Dict, Any, Optional, Tuple
import re

from SmartLegalAssistant.core.embeddings import EmbeddingModel
from SmartLegalAssistant.core.vector_store import VectorStore
from SmartLegalAssistant.core.llm import LanguageModel
from SmartLegalAssistant.core.reranker import Reranker


class Retriever:
    """Retrieval class for RAG."""

    def __init__(
        self,
        embedding_model: EmbeddingModel,
        vector_store: VectorStore,
        reranker: Optional[Reranker] = None,
        llm: Optional[LanguageModel] = None,
        min_score_threshold: float = 0.40  # 👈 added filtering threshold
    ):
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.reranker = reranker
        self.llm = llm
        self.min_score_threshold = min_score_threshold

    def retrieve(
        self,
        query: str,
        top_k: int = 25,
        use_query_expansion: bool = False,
        rerank_results: bool = True,  # 👈 rerank always defaulted to True
    ) -> Tuple[List[str], List[Dict[str, Any]]]:
        """Retrieve relevant documents for a given query."""

        processed_query = self._prepare_query(query, use_query_expansion)
        query_embedding = self.embedding_model.embed_query(processed_query)

        search_results = self.vector_store.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )

        retrieved_chunks = []
        sources = []

        for match in search_results.get("matches", []):
            score = match.get('score', 0.0)
            text = match['metadata'].get("text", "")

            if not text.strip():
                continue  # Skip empty chunks

            if score < self.min_score_threshold:
                continue  # 👈 Filter out low-score documents

            ref = (
                match['metadata'].get("reference")
                or match['metadata'].get("ref")
                or match['metadata'].get("source")
                or "Unknown"
            )

            retrieved_chunks.append(text)
            sources.append({
                "reference": ref,
                "text": text,
                "score": score,
                "preview": text[:200] + "..."
            })

        if rerank_results and self.reranker:
            reranked_sources = self.reranker.rerank(query=query, documents=sources, top_n=top_k)
            reranked_chunks = [source["text"] for source in reranked_sources]
            return reranked_chunks, reranked_sources

        return retrieved_chunks, sources

    def _prepare_query(self, query: str, use_query_expansion: bool) -> str:
        """Expand the query if needed."""
        if not use_query_expansion or not self.llm:
            return query
        expanded_query = self._expand_query(query)
        return expanded_query

    def _expand_query(self, query: str) -> str:
        """Expand the query using the LLM."""
        prompt = f"""
Given the search query below, expand it with additional relevant terms to improve the search results.
Add related concepts and alternative phrasings to the search query.

Original Query: "{query}"

Expanded query:
"""
        expanded = self.llm.generate(prompt, temperature=0.3)
        expanded = re.sub(r'^[^a-zA-Z0-9]*', '', expanded)
        return expanded


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    from SmartLegalAssistant.core.embeddings import get_embedding_model
    from SmartLegalAssistant.core.vector_store import get_vector_store
    from SmartLegalAssistant.core.llm import get_language_model
    from SmartLegalAssistant.core.reranker import get_reranker

    load_dotenv()

    embedding_model = get_embedding_model()
    index_name = os.getenv("PINECONE_INDEX_NAME", "smart-legal")
    vector_store = get_vector_store(index_name=index_name)
    llm = get_language_model()
    reranker = get_reranker()

    retriever = Retriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
        llm=llm,
        reranker=reranker,
        min_score_threshold=0.40  # 👈 Set your filtering here
    )

    query = "director duties in a company"
    retrieved_chunks, sources = retriever.retrieve(query, top_k=5, use_query_expansion=True)

    print(f"Retrieved {len(retrieved_chunks)} chunks after filtering and reranking.")
    for i, src in enumerate(sources, 1):
        print(f"{i}. Reference: {src['reference']} | Score: {src['score']:.2f} | Preview: {src['preview']}")
