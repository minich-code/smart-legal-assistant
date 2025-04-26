"""
Main Streamlit application for the RAG assistant.
"""
import streamlit as st
import uuid
import time
from typing import Dict, Any

# Import core components
from SmartLegalAssistant.core.embeddings import get_embedding_model
from SmartLegalAssistant.core.vector_store import get_vector_store
from SmartLegalAssistant.core.llm import get_language_model
from SmartLegalAssistant.core.retriever import Retriever, RAGPipeline

# Import utilities
from utils.prompt_templates import get_template
from utils.logger import RAGLogger

# Import configuration
from config import Config

# Import UI components
from app.components.sidebar import render_sidebar

# Initialize configuration
config = Config()

# Setup page configuration
st.set_page_config(
    page_title=config.get("DEFAULT_PAGE_TITLE"),
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "query_history" not in st.session_state:
    st.session_state.query_history = []
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())
if "settings_applied" not in st.session_state:
    st.session_state.settings_applied = False

def initialize_rag_pipeline():
    """Initialize the RAG pipeline with current configuration.
    
    Returns:
        Initialized RAG pipeline
    """
    try:
        # Get configurations 
        embedding_config = config.get_embedding_config()
        vector_store_config = config.get_vector_store_config()
        llm_config = config.get_llm_config()

        # Initialize the components 
        embedding_model = get_embedding_model(**embedding_config)
        vector_store = get_vector_store(**vector_store_config)
        llm = get_language_model(**llm_config)

        # Initialize reranker if enabled 
        reranker = None 
        if config.get("USE_COHERE_RERANK", False):
            try:
                from SmartLegalAssistant.core.reranker import get_reranker 
                reranker = get_reranker(
                    reranker_type = "cohere", 
                    api_key = config.get("COHERE_API_KEY"),
                    model = config.get("COHERE_RERANK_MODEL", "rerank-multilingual-v2.0")
                )

            except Exception as e:
                st.warning(f"Error initializing cohere reranker: {str(e)}. Proceeding without reranking.")


        # Initialize retriever
        retriever = Retriever(
            embedding_model=embedding_model,
            vector_store=vector_store,
            llm=llm,
            reranker=reranker
        )

        # Get prompt template
        template_name = config.get("DEFAULT_PROMPT_TEMPLATE", "factual_qa")
        prompt_template = get_template(template_name)

        # Initialize RAG pipeline
        rag_pipeline = RAGPipeline(
            retriever=retriever,
            llm=llm,
            prompt_template=prompt_template
        )

        return rag_pipeline
    
    except Exception as e:
        st.error(f"Error initializing RAG pipeline: {str(e)}")
        return None


def on_settings_change(updated_settings: Dict[str, Any]):
    """Handle settings changes.
    
    Args:
        updated_settings: Updated settings
    """
    config.update(updated_settings)
    st.session_state.settings_applied = True

def format_sources(sources):
    """Format source information for display.
    
    Args:
        sources: List of source dictionaries
        
    Returns:
        Formatted source HTML
    """
    if not sources:
        return ""
    
    source_html = "<div style='margin-top: 20px; padding: 10px; background-color: #f0f2f6; border-radius: 5px;'>"
    source_html += "<h4>Sources:</h4>"
    
    for i, source in enumerate(sources, 1):
        ref = source.get('reference', 'Unknown')
        preview = source.get('preview', '')
        score = source.get('score', 0)
        
        source_html += f"""
        <div style='margin-bottom: 10px; padding: 8px; background-color: white; border-radius: 5px;'>
            <strong>{i}. {ref}</strong> (Score: {score:.2f})
            <div style='margin-top: 5px; font-size: 0.9em;'>{preview}</div>
        </div>
        """
    
    source_html += "</div>"
    return source_html

def display_response(response_data):
    """Display the RAG response with sources.
    
    Args:
        response_data: Response data from RAG pipeline
    """
    query = response_data.get("query", "")
    response = response_data.get("response", "")
    sources = response_data.get("sources", [])
    
    # Display response
    st.markdown("### Answer")
    st.markdown(response)
    
    # Display sources with toggle
    with st.expander("View Sources", expanded=False):
        st.markdown(format_sources(sources), unsafe_allow_html=True)
    
    # Display feedback buttons
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("👍 Helpful"):
            logger = RAGLogger()
            logger.log_feedback(
                query_id=f"{st.session_state.conversation_id}_{len(st.session_state.query_history)}",
                feedback={"rating": "helpful", "helpful": True}
            )
            st.success("Thanks for your feedback!")
    
    with col2:
        if st.button("👎 Not Helpful"):
            logger = RAGLogger()
            logger.log_feedback(
                query_id=f"{st.session_state.conversation_id}_{len(st.session_state.query_history)}",
                feedback={"rating": "not_helpful", "helpful": False}
            )
            st.error("Thanks for your feedback!")

def main():
    """Main application function."""
    # Render sidebar
    render_sidebar(config.to_dict(), on_settings_change)
    
    # Application header
    st.title("📚 RAG Assistant")
    st.markdown(
        """
        Ask questions about your knowledge base and get accurate answers backed by sources.
        """
    )
    
    # Check if configuration is valid
    if not config.validate():
        st.error(
            """
            ⚠️ Configuration Error: Missing required API keys or settings.
            
            Please check your .env file or environment variables and ensure all required configurations are set.
            Required: TOGETHER_API_KEY, PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME
            """
        )
        return
    
    # Query input
    query = st.text_input("Ask a question:", key="query_input")
    
    # Add options row beneath input
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        top_k = st.selectbox(
            "Results:",
            options=[10, 20, 30, 40, 50],
            index=3,  # Default to 40
            key="top_k_select"
        )
    
    with col2:
        advanced_options = st.checkbox("Advanced Options", key="advanced_options")
    
    # Show advanced options if checked
    if advanced_options:
        with st.expander("Advanced Retrieval Options", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                use_query_expansion = st.checkbox(
                    "Query Expansion",
                    value=config.get("USE_QUERY_EXPANSION", False),
                    help="Expand query with related terms"
                )
            with col2:
                use_reranking = st.checkbox(
                    "Rerank Results",
                    value=config.get("USE_RERANKING", False),
                    help="Rerank results by relevance"
                )
    else:
        use_query_expansion = config.get("USE_QUERY_EXPANSION", False)
        use_reranking = config.get("USE_RERANKING", False)
    
    # Submit button
    submit_button = st.button("Submit")
    
    # Process query when submitted
    if submit_button and query:
        # Initialize logger
        logger = RAGLogger()
        logger.log_query(query)
        
        # Show processing indicator
        with st.spinner("Retrieving information..."):
            try:
                # Initialize RAG pipeline (or use cached instance)
                rag_pipeline = initialize_rag_pipeline()
                
                if rag_pipeline:
                    # Start timer
                    start_time = time.time()
                    
                    # Run RAG pipeline
                    response_data = rag_pipeline.run(
                        query=query,
                        top_k=top_k,
                        temperature=config.get("LLM_TEMPERATURE", 0.2),
                        use_query_expansion=use_query_expansion,
                        rerank_results=use_reranking
                    )
                    
                    # Calculate elapsed time
                    elapsed_time = time.time() - start_time
                    
                    # Log response
                    logger.log_response(response_data)
                    
                    # Add to history
                    st.session_state.query_history.append({
                        "query": query,
                        "response_data": response_data,
                        "timestamp": time.time(),
                        "elapsed_time": elapsed_time
                    })
                    
                    # Display processing time
                    st.caption(f"Processed in {elapsed_time:.2f} seconds")
                    
                    # Display response
                    display_response(response_data)
                else:
                    st.error("Failed to initialize RAG pipeline. Please check your configuration.")
            
            except Exception as e:
                logger.log_error(f"Error processing query: {str(e)}")
                st.error(f"Error processing your query: {str(e)}")
    
    # Display history if available
    if st.session_state.query_history:
        with st.expander("Recent Queries", expanded=False):
            for i, item in enumerate(reversed(st.session_state.query_history[-5:])):
                st.markdown(f"**Q: {item['query']}**")
                st.markdown(f"*{time.strftime('%H:%M:%S', time.localtime(item['timestamp']))} · {item['elapsed_time']:.2f}s*")
                if st.button(f"Show Answer #{i+1}", key=f"history_{i}"):
                    display_response(item['response_data'])
                st.markdown("---")

if __name__ == "__main__":
    main()