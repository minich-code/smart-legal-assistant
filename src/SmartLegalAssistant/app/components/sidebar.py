

"""
Sidebar component for the Streamlit app.
"""
import streamlit as st
from typing import Dict, Any, Callable

def render_sidebar(config: Dict[str, Any], on_settings_change: Callable[[Dict[str, Any]], None]) -> None:
    """Render the sidebar with configuration options.
    
    Args:
        config: Current configuration
        on_settings_change: Callback when settings change
    """
    st.sidebar.title("Settings")
    
    # Create sections with expanders
    with st.sidebar.expander("Retrieval Settings", expanded=False):
        top_k = st.slider(
            "Number of documents to retrieve",
            min_value=5,
            max_value=100,
            value=config.get("DEFAULT_TOP_K", 40),
            step=5
        )
        
        use_query_expansion = st.checkbox(
            "Enable query expansion",
            value=config.get("USE_QUERY_EXPANSION", False),
            help="Expands queries to improve recall (may be slower)"
        )
        
        use_reranking = st.checkbox(
            "Enable result reranking",
            value=config.get("USE_RERANKING", False),
            help="Reranks retrieved results for better precision (may be slower)"
        )
    
    with st.sidebar.expander("Response Settings", expanded=False):
        template_options = {
            "legal_assistant": "Legal Assistant",
            "factual_qa": "Factual Q&A",
            "critical_analysis": "Critical Analysis",
            "multi_perspective": "Multiple Perspectives",
            "concise": "Concise Answer"
        }
        
        prompt_template = st.selectbox(
            "Response Format",
            options=list(template_options.keys()),
            format_func=lambda x: template_options[x],
            index=list(template_options.keys()).index(config.get("DEFAULT_PROMPT_TEMPLATE", "factual_qa"))
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=config.get("LLM_TEMPERATURE", 0.2),
            step=0.1,
            help="Higher values make output more random, lower values more deterministic"
        )
    
    # Apply button
    if st.sidebar.button("Apply Settings"):
        updated_settings = {
            "DEFAULT_TOP_K": top_k,
            "USE_QUERY_EXPANSION": use_query_expansion,
            "USE_RERANKING": use_reranking,
            "DEFAULT_PROMPT_TEMPLATE": prompt_template,
            "LLM_TEMPERATURE": temperature
        }
        on_settings_change(updated_settings)
        st.sidebar.success("Settings updated!")
    
    # About section
    with st.sidebar.expander("About", expanded=False):
        st.markdown("""
        **RAG Assistant**
        
        This application uses Retrieval-Augmented Generation (RAG) to answer questions based on a knowledge base.
        
        - Queries your vector database
        - Retrieves relevant information
        - Generates accurate responses
        
        Built with Streamlit, Pinecone, and Together AI.
        """)