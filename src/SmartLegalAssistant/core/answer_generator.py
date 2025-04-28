# answer_generator.py

from typing import List, Dict, Any, Optional, Union
from SmartLegalAssistant.utils.prompt_templates import get_template, format_template
from SmartLegalAssistant.core.llm import LanguageModel


class AnswerGenerator:
    """Answer generation class for RAG system."""

    def __init__(
            self,
            llm: LanguageModel,
            default_template_type: str = "legal_assistant",
            max_context_length: int = 4000,
            temperature: float = 0.2
    ):
        """Initialize the answer generator.

        Args:
            llm: Language model for answer generation
            default_template_type: Default prompt template type to use
            max_context_length: Maximum context length to send to LLM
            temperature: Temperature parameter for generation
        """
        self.llm = llm
        self.default_template_type = default_template_type
        self.max_context_length = max_context_length
        self.temperature = temperature

    def generate_answer(
            self,
            query: str,
            retrieved_chunks: List[str],
            template_type: Optional[str] = None,
            custom_template: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate an answer based on retrieved chunks and query.

        Args:
            query: User query
            retrieved_chunks: List of relevant text chunks
            template_type: Type of prompt template to use (overrides default)
            custom_template: Custom template string (overrides template_type)

        Returns:
            Dictionary containing answer and metadata
        """
        if not retrieved_chunks:
            return {
                "answer": "I don't have enough information to answer this question.",
                "has_context": False,
                "template_used": template_type or self.default_template_type
            }

        # Select the appropriate template
        if custom_template:
            template = custom_template
            template_used = "custom"
        else:
            template_used = template_type or self.default_template_type
            template = get_template(template_used)

        # Prepare context by combining chunks
        context = self._prepare_context(retrieved_chunks)

        # Format the prompt template
        prompt = format_template(template, context=context, query=query)

        # Generate answer using LLM
        answer = self.llm.generate(prompt, temperature=self.temperature)

        return {
            "answer": answer,
            "has_context": True,
            "template_used": template_used,
            "context_char_count": len(context),
            "chunks_used": len(retrieved_chunks)
        }

    def _prepare_context(self, chunks: List[str]) -> str:
        """Prepare and potentially trim context to fit within token limits.

        Args:
            chunks: List of text chunks

        Returns:
            Combined context string
        """
        # Simple concat with separator
        context = "\n\n---\n\n".join(chunks)

        # If context is too long, truncate it
        if len(context) > self.max_context_length:
            context = context[:self.max_context_length] + "..."

        return context


# Integration example
class RAGPipeline:
    """Complete RAG pipeline combining retrieval and answer generation."""

    def __init__(
            self,
            retriever,
            answer_generator: AnswerGenerator,
            default_top_k: int = 25,
    ):
        """Initialize the RAG pipeline.

        Args:
            retriever: Document retriever instance
            answer_generator: Answer generator instance
            default_top_k: Default number of documents to retrieve
        """
        self.retriever = retriever
        self.answer_generator = answer_generator
        self.default_top_k = default_top_k

    def process_query(
            self,
            query: str,
            top_k: Optional[int] = None,
            use_query_expansion: bool = False,
            rerank_results: bool = True,
            template_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Process a query through the complete RAG pipeline.

        Args:
            query: User query
            top_k: Number of documents to retrieve
            use_query_expansion: Whether to expand the query
            rerank_results: Whether to rerank results
            template_type: Type of prompt template to use

        Returns:
            Dictionary with answer, retrieved documents, and metadata
        """
        # Retrieve relevant documents
        retrieved_chunks, sources = self.retriever.retrieve(
            query=query,
            top_k=top_k or self.default_top_k,
            use_query_expansion=use_query_expansion,
            rerank_results=rerank_results
        )

        # Generate answer
        result = self.answer_generator.generate_answer(
            query=query,
            retrieved_chunks=retrieved_chunks,
            template_type=template_type
        )

        # Create formatted chunks for better display
        formatted_chunks = []
        for i, (chunk, source) in enumerate(zip(retrieved_chunks, sources)):
            formatted_chunks.append({
                "index": i + 1,
                "text": chunk,
                "reference": source["reference"],
                "score": source["score"]
            })

        # Add retrieval metadata and documents to result
        result.update({
            "sources": sources,
            "retrieved_chunks": retrieved_chunks,  # Raw chunks
            "formatted_chunks": formatted_chunks,  # Nicely formatted for display
            "retrieval_count": len(retrieved_chunks),
            "query": query,
        })

        return result


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    from SmartLegalAssistant.core.embeddings import get_embedding_model
    from SmartLegalAssistant.core.vector_store import get_vector_store
    from SmartLegalAssistant.core.llm import get_language_model
    from SmartLegalAssistant.core.reranker import get_reranker
    from SmartLegalAssistant.core.retriever import Retriever

    load_dotenv()

    # Initialize components
    embedding_model = get_embedding_model()
    index_name = os.getenv("PINECONE_INDEX_NAME", "smart-legal")
    vector_store = get_vector_store(index_name=index_name)
    llm = get_language_model()
    reranker = get_reranker()

    # Set up retriever
    retriever = Retriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
        llm=llm,
        reranker=reranker,
        min_score_threshold=0.40
    )

    # Set up answer generator
    answer_generator = AnswerGenerator(
        llm=llm,
        default_template_type="legal_assistant",
        temperature=0.2
    )

    # Set up complete pipeline
    rag_pipeline = RAGPipeline(
        retriever=retriever,
        answer_generator=answer_generator
    )

    # Process a test query
    query = "what company names are you not allowed to use when naming your company"
    result = rag_pipeline.process_query(query)

    print(f"\n🔵 Query: {query}")
    print(f"\n🟢 Generated Answer ({result['template_used']} template):\n")
    print(result["answer"])
    print(f"\n🟡 Based on {result['retrieval_count']} relevant documents.\n")

    print("\n📝 Retrieved Context Chunks (sorted by relevance):\n")

    # Sort chunks by score descending
    sorted_chunks = sorted(result["formatted_chunks"], key=lambda x: x["score"], reverse=True)

    for idx, chunk_info in enumerate(sorted_chunks, start=1):
        print(f"📄 Chunk #{idx}")
        print(f"🔹 Score: {chunk_info['score']:.4f}")
        print(f"🔹 Reference: {chunk_info['reference']}\n")
        print(f"{chunk_info['text']}")
        print("\n" + "=" * 80 + "\n")