
# RAG Retrieval implementation with Cohere Rerank 


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
            llm: Optional[LanguageModel] = None
    ):
        
        """ Initialize the retriever with components 
        
        Args:
            embedding_model: Embedding model to use for document embeddings
            vector_store: Vector store to use for storing and retrieving documents
            reranker: Reranker to use for reranking documents for improving results order 
            llm: Language model to use for generating responses
        """

        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.reranker = reranker
        self.llm = llm

    def retrieve(
            self, 
            query: str,
            top_k: int = 25,
            use_query_expansion: bool = False,
            rerank_results: bool = False,
    ) -> Tuple[List[str], List[Dict[str, Any]]]:
        
        """Retrieve relevant documents for a given query.
        
        Args:
            query: The query to retrieve relevant documents for.
            top_k: The number of top documents to retrieve.
            use_query_expansion: Whether to use query expansion.
            rerank_results: Whether to rerank the retrieved documents.
        
        Returns:
            A tuple containing the retrieved documents and their metadata."""
        
        if use_query_expansion and self.llm:
            expanded_query = self._expand_query(query)
            # Combine original and expand query vectors 

            query_embedding = self.embedding_model.embed_query(query)
            expanded_query_embedding = self.embedding_model.embed_query(expanded_query)
            # Average the embeddings (simple fusion)
            query_embedding = [(q + e) / 2 for q, e in zip(query_embedding, expanded_query_embedding)]

        else:
            query_embedding = self.embedding_model.embed_query(query)



        # Query the vector store 
        search_results = self.vector_store.query(vector = query_embedding, top_k=top_k, include_metadata=True)

        # Process the results 
        retrieved_chunks = []
        sources = []

        for match in search_results["matches"]:
            text = match['metadata'].get("text", "")

            # Skip empty results 
            if not text.strip():
                continue

            # Extract reference information 
            ref = (
                match['metadata'].get("reference") or 
                match['metadata'].get("ref") or
                match['metadata'].get("source") or "Unknown"
                
            )

            retrieved_chunks.append(text)
            sources.append({
                "reference": ref,
                "text": text,
                "score": match.get('score', 0.0),
                "preview": text[200] + "..." # preview the first 200 characters 
            })

            # Rerank the results if requested and reranker available 
            if rerank_results and self.reranker:
                reranked_sources = self.reranker.rerank(query=query, documents=sources, top_n=top_k)
                # Extract text from reranked sources
                reranked_chunks = [source["text"] for source in reranked_sources]

                return reranked_chunks, reranked_sources

            return retrieved_chunks, sources
        

def _expand_query(self, query: str) -> str:
        """Expand the query using the LLM.
        
        Args:
            query: The query to expand (Original Query).
        
        Returns:
            The expanded query.
        """
        
        if not self.llm:
            return query 
        
        prompt = f"""
        Given the search query below, expand it with additional relevant terms to improve the search results
        Add related concepts and alternative phrasings to the search query.

        Original Query: "{query}"

        Expanded query: 
        """
        expanded = self.llm.generate(prompt, temperature = 0.3)

        # Clean the response 
        expanded = re.sub(r'^[^a-zA-Z0-9]*', '', expanded) # Remove leadin non alphanumeric characters
        
        
        
        return expanded
        
    





