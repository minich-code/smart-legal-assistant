

## Reranking module that uses Cohere API

import os 
import cohere 
from typing import List, Dict, Any, Optional, Union


class Reranker:
    """ Base class for reranking implementations"""

    def rerank(self, query: str, documents: List[Dict[str, Any]], top_n: Optional[int]) -> List[Dict[str, Any]]:
        """Rerank the top_n documents based on the query.
        
        Args:
            query (str): The query to rerank.
            documents (List[Dict[str, Any]]): The list of documents to rerank.
            top_n (Optional[int]): The number of top documents to return.

        Return:
            List[Dict[str, Any]]: The list of reranked documents.
        """
        

        raise NotImplementedError("Subclasses must implement the rerank method.")

class CohereReranker(Reranker):
    """ Implement using cohere reranker """

    def __init__(self, api_key: Optional[str] = None, model: str = "rerank-multilingual-v2.0"):
        """ Initialize Cohere Reranker 
        
        Args:
            api_key: Cohere API key 
            model: Cohere reranking model to use 
        """

        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("Please provide a Cohere API key or set the COHERE_API_KEY environment variable.")
        
        self.model = model
        self.model = cohere.Client(self.api_key)


    def rerank(self, query: str, documents: List[Dict[str, Any]], top_n: Optional[int]) -> List[Dict[str, Any]]:
        """ Rerank documents using Cohere reranker model 
        
        Args:
            query (str): The query to rerank.
            documents (List[Dict[str, Any]]): The list of documents to rerank.
            top_n (Optional[int]): The number of top documents to return.

        Return:
            List[Dict[str, Any]]: The list of reranked documents.
        
        """

        if not documents:
            return []
        
        # Extract documents texts 
        doc_texts = [doc.get["text", ""] for doc in documents]

        # Call the cohere rerank model 
        results = self.Client.rerank(
            model=self.model,
            query=query,
            documents=doc_texts,
            top_n=top_n or len(documents))

        # Rerank the documents based on rank results
        reranked_docs = []

        for results in results.results:
            # Get original document and add rerank score 

            original_doc = documents[results.index]
            original_doc["rerank_score"] = results.relevance_score
            reranked_docs.append(original_doc)

        return reranked_docs
    
# Factory function to get the right reranker 
def get_reranker(reranker_type: str = "cohere", **kwargs) -> Reranker:
    """ Get a reranker instance based on the provided reranker type.
    
    Args:
    reranker_type (str): Types of reranker to use ie. (cohere)
    **kwargs : Additional keyword arguments to pass to the reranker constructor.
    
    Returns:
    reranker: An instance of the reranker.
    
    """
    if reranker_type == "cohere":
        return CohereReranker(**kwargs)
    
    else:
        raise ValueError(f"Unknown reranker type: {reranker_type}")




        
       
    

    