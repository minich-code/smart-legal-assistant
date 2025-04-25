

"""
Logging utilities for the RAG application.
"""
import logging
import os
import json
import datetime
from typing import Dict, Any, Optional

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class RAGLogger:
    """Logger for RAG operations with feedback collection."""
    
    def __init__(self, log_dir: str = "logs", log_level: int = logging.INFO):
        """Initialize the logger.
        
        Args:
            log_dir: Directory to store logs
            log_level: Logging level
        """
        self.logger = logging.getLogger("rag-app")
        self.logger.setLevel(log_level)
        
        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Create file handler for logging to file
        log_file = os.path.join(log_dir, f"rag_{datetime.datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        
        # Create formatter and add to handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # Add handlers to logger if not already added
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
    
    def log_query(self, query: str, user_id: Optional[str] = None) -> None:
        """Log a user query.
        
        Args:
            query: The user's query
            user_id: Optional user identifier
        """
        self.logger.info(f"Query: {query} | User: {user_id or 'anonymous'}")
    
    def log_retrieval(self, query: str, num_docs: int, top_score: float) -> None:
        """Log retrieval statistics.
        
        Args:
            query: The query that was processed
            num_docs: Number of documents retrieved
            top_score: Highest relevance score
        """
        self.logger.info(f"Retrieved {num_docs} documents for query: '{query}' | Top score: {top_score:.4f}")
    
    def log_response(self, response_data: Dict[str, Any]) -> None:
        """Log the complete RAG response.
        
        Args:
            response_data: Complete response data including sources
        """
        # Log basic info to regular log
        self.logger.info(f"Generated response for: '{response_data.get('query', 'unknown')}' | "
                         f"Sources: {len(response_data.get('sources', []))}")
        
        # Log detailed info to structured log file
        try:
            # Create a simplified version for logging
            log_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "query": response_data.get("query", ""),
                "num_sources": len(response_data.get("sources", [])),
                "response_length": len(response_data.get("response", "")),
                "source_scores": [s.get("score", 0) for s in response_data.get("sources", [])[:5]],
            }
            
            # Save detailed log to JSON
            os.makedirs("logs/detailed", exist_ok=True)
            log_file = f"logs/detailed/rag_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(log_file, "w") as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to log detailed response: {str(e)}")
    
    def log_feedback(self, query_id: str, feedback: Dict[str, Any]) -> None:
        """Log user feedback on responses.
        
        Args:
            query_id: Identifier for the query
            feedback: Feedback data
        """
        self.logger.info(f"Feedback for query {query_id}: Rating: {feedback.get('rating', 'N/A')}")
        
        # Save feedback to separate file
        try:
            os.makedirs("logs/feedback", exist_ok=True)
            feedback_file = "logs/feedback/feedback.jsonl"
            
            feedback_entry = {
                "timestamp": datetime.datetime.now().isoformat(),
                "query_id": query_id,
                "rating": feedback.get("rating"),
                "comment": feedback.get("comment", ""),
                "helpful": feedback.get("helpful", False),
                "accurate": feedback.get("accurate", False)
            }
            
            # Append to JSONL file
            with open(feedback_file, "a") as f:
                f.write(json.dumps(feedback_entry) + "\n")
                
        except Exception as e:
            self.logger.error(f"Failed to log feedback: {str(e)}")
    
    def log_error(self, error_message: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Log an error.
        
        Args:
            error_message: Error message
            details: Optional error details
        """
        if details:
            self.logger.error(f"{error_message} | Details: {json.dumps(details)}")
        else:
            self.logger.error(error_message)