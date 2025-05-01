# BASE

import streamlit as st
import os
from dotenv import load_dotenv

# Import components from your project
from SmartLegalAssistant.core.embeddings import get_embedding_model
from SmartLegalAssistant.core.vector_store import get_vector_store
from SmartLegalAssistant.core.llm import get_language_model
from SmartLegalAssistant.core.reranker import get_reranker
from SmartLegalAssistant.core.answer_generator import AnswerGenerator, RAGPipeline
from SmartLegalAssistant.utils.prompt_templates import get_template
from SmartLegalAssistant.core.retriever import Retriever

# Load environment variables
load_dotenv()

# App title and description
st.title("Smart Legal Assistant")
st.markdown("Ask questions about legal documents and get AI-powered answers")

# Sidebar for configuration
st.sidebar.header("Configuration")

# Template selection
template_options = ["legal_assistant", "factual_qa", "critical_analysis",
                    "multi_perspective", "concise"]
selected_template = st.sidebar.selectbox("Select Response Template",
                                         template_options,
                                         index=0)

# Advanced options
with st.sidebar.expander("Advanced Options"):
    top_k = st.slider("Number of chunks to retrieve", 5, 50, 25)
    use_reranking = st.checkbox("Use reranking", value=True)
    use_query_expansion = st.checkbox("Use query expansion", value=False)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.1)


# Initialize the RAG components
@st.cache_resource
def initialize_rag_pipeline():
    try:
        # Initialize embedding model
        embedding_model = get_embedding_model(model_type="together")

        # Initialize vector store
        vector_store = get_vector_store(
            store_type="pinecone",
            index_name=os.getenv("PINECONE_INDEX_NAME"),
            namespace=os.getenv("PINECONE_NAMESPACE", "")
        )

        # Initialize LLM
        llm = get_language_model(model_type="together")

        # Initialize reranker
        reranker = get_reranker(reranker_type="together_ai")

        # Initialize retriever
        retriever = Retriever(
            embedding_model=embedding_model,
            vector_store=vector_store,
            reranker=reranker,
            llm=llm
        )

        # Initialize answer generator
        answer_generator = AnswerGenerator(
            llm=llm,
            default_template_type="legal_assistant",
            temperature=0.2
        )

        # Initialize RAG pipeline
        rag_pipeline = RAGPipeline(
            retriever=retriever,
            answer_generator=answer_generator,
            default_top_k=25
        )

        return rag_pipeline, True

    except Exception as e:
        st.error(f"Error initializing RAG pipeline: {str(e)}")
        return None, False


# Initialize RAG pipeline
rag_pipeline, initialization_success = initialize_rag_pipeline()

# Main query input
query = st.text_area("Enter your legal question:", height=100)

# Process query button
if st.button("Submit Question") and query and initialization_success:
    try:
        with st.spinner("Processing your query..."):
            # Process the query
            result = rag_pipeline.process_query(
                query=query,
                top_k=top_k,
                use_query_expansion=use_query_expansion,
                rerank_results=use_reranking,
                template_type=selected_template
            )

            # Display the answer
            st.header("Answer")
            st.write(result["answer"])

            # Display the retrieved chunks
            st.header("Retrieved Sources")

            # Create tabs for different views
            tabs = st.tabs(["Ranked Sources", "Source Details"])

            with tabs[0]:
                for i, chunk in enumerate(result["formatted_chunks"]):
                    with st.expander(f"Source {i + 1}: {chunk['reference']} (Score: {chunk['score']:.4f})"):
                        st.write(chunk["text"])

            with tabs[1]:
                # Display table of sources with scores
                source_data = [
                    {
                        "Index": i + 1,
                        "Reference": chunk["reference"],
                        "Score": f"{chunk['score']:.4f}",
                        "Preview": chunk["text"][:100] + "..."
                    }
                    for i, chunk in enumerate(result["formatted_chunks"])
                ]
                st.dataframe(source_data)

    except Exception as e:
        st.error(f"Error processing query: {str(e)}")

# Display help information
with st.sidebar.expander("Help"):
    st.markdown("""
    **How to use this app:**
    1. Enter your legal question in the text area
    2. Adjust advanced options if needed
    3. Click 'Submit Question'

    **Template Options:**
    - **Legal Assistant**: Detailed legal interpretation in multiple perspectives
    - **Factual QA**: Just the facts from the documents
    - **Critical Analysis**: Analytical breakdown of the information
    - **Multi Perspective**: Multiple viewpoints on the issue
    - **Concise**: Brief, to-the-point answers
    """)

# Footer
st.markdown("---")
st.caption("Smart Legal Assistant - Powered by WordLoom Technology")

# --------------MINICH---------------

# import streamlit as st
# import os
# from dotenv import load_dotenv
#
# # Import components
# from components.sidebar import render_sidebar
# from components.main_view import render_query_input, render_answer
# from components.follow_up import render_follow_up
# from utils.session import initialize_session_state
# from utils.formatting import apply_highlighting
# #from utils.formatting import apply_highlighting
#
# # Import RAG components
# from SmartLegalAssistant.core.embeddings import get_embedding_model
# from SmartLegalAssistant.core.vector_store import get_vector_store
# from SmartLegalAssistant.core.llm import get_language_model
# from SmartLegalAssistant.core.reranker import get_reranker
# from SmartLegalAssistant.core.answer_generator import AnswerGenerator, RAGPipeline
# from SmartLegalAssistant.core.retriever import Retriever
#
# # Load environment variables
# load_dotenv()
#
# # Set page config
# st.set_page_config(
#     page_title="Smart Legal Assistant",
#     page_icon="⚖️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )
#
# # Add custom CSS
# # with open("styles/custom.css") as f:
# #     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
#
# # With this:
# import os
#
# # Get the directory where app.py is located
# current_dir = os.path.dirname(os.path.abspath(__file__))
# css_path = os.path.join(current_dir, "styles", "custom.css")
#
# # Check if file exists before opening
# if os.path.exists(css_path):
#     with open(css_path) as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# else:
#     # Use inline CSS as fallback
#     st.markdown("""
#     <style>
#     .legal-citation {
#         background-color: #f0f7ff;
#         color: #0066cc;
#         font-weight: bold;
#         padding: 2px 4px;
#         border-radius: 3px;
#         border-bottom: 1px solid #0066cc;
#     }
#     </style>
#     """, unsafe_allow_html=True)
#
# # App title and description
# st.title("Smart Legal Assistant")
# st.markdown("Ask questions about legal documents and get AI-powered answers")
#
# # Initialize session state
# initialize_session_state()
#
#
# # Initialize the RAG components
# @st.cache_resource
# def initialize_rag_pipeline():
#     try:
#         # Initialize embedding model
#         embedding_model = get_embedding_model(model_type="together")
#
#         # Initialize vector store
#         vector_store = get_vector_store(
#             store_type="pinecone",
#             index_name=os.getenv("PINECONE_INDEX_NAME"),
#             namespace=os.getenv("PINECONE_NAMESPACE", "")
#         )
#
#         # Initialize LLM
#         llm = get_language_model(model_type="together")
#
#         # Initialize reranker
#         reranker = get_reranker(reranker_type="together_ai")
#
#         # Initialize retriever
#         retriever = Retriever(
#             embedding_model=embedding_model,
#             vector_store=vector_store,
#             reranker=reranker,
#             llm=llm
#         )
#
#         # Initialize answer generator
#         answer_generator = AnswerGenerator(
#             llm=llm,
#             default_template_type="legal_assistant",
#             temperature=0.2
#         )
#
#         # Initialize RAG pipeline
#         rag_pipeline = RAGPipeline(
#             retriever=retriever,
#             answer_generator=answer_generator,
#             default_top_k=25
#         )
#
#         return rag_pipeline, True
#
#     except Exception as e:
#         st.error(f"Error initializing RAG pipeline: {str(e)}")
#         return None, False
#
#
# # Initialize RAG pipeline
# rag_pipeline, initialization_success = initialize_rag_pipeline()
#
# # Render sidebar with configuration options
# selected_template, user_role, answer_style, top_k, use_reranking, use_query_expansion, temperature = render_sidebar()
#
# # Helper function to customize template based on role and style
# def customize_template_for_role(template_type, role, style):
#     """Modify the template based on user role and answer style."""
#     # In a real implementation, you'd modify the template here
#     # For now, we'll just pass along the base template
#     return template_type
#
#
# # Main query input and processing
# query, submitted = render_query_input()
#
# if submitted and query and initialization_success:
#     try:
#         with st.spinner("Processing your query..."):
#             # Store the query in session state
#             st.session_state.query_history.append(query)
#
#             # Update template based on user role and answer style
#             modified_template = customize_template_for_role(selected_template, user_role, answer_style)
#
#             # Process the query
#             result = rag_pipeline.process_query(
#                 query=query,
#                 top_k=top_k,
#                 use_query_expansion=use_query_expansion,
#                 rerank_results=use_reranking,
#                 template_type=selected_template  # We'll handle custom templates in a moment
#             )
#
#             # Store the result in session state
#             st.session_state.last_result = result
#
#             # Apply highlighting to the answer (for legal citations)
#             highlighted_answer = apply_highlighting(result["answer"])
#
#             # Render the answer with the appropriate style
#             render_answer(highlighted_answer, result, answer_style)
#
#             # Render follow-up question input
#             render_follow_up(rag_pipeline, selected_template, user_role, answer_style)
#
#     except Exception as e:
#         st.error(f"Error processing query: {str(e)}")
#
#
# # # Helper function to customize template based on role and style
# # def customize_template_for_role(template_type, role, style):
# #     """Modify the template based on user role and answer style."""
# #     # In a real implementation, you'd modify the template here
# #     # For now, we'll just pass along the base template
# #     return template_type
#
#
# # Footer
# st.markdown("---")
# st.caption("Smart Legal Assistant - Powered by RAG Technology")


# ------CEASER -----
# import streamlit as st
# import os
# from dotenv import load_dotenv
#
# # Import components
# from components.sidebar import render_sidebar
# from components.main_view import render_query_input, render_answer
# from components.follow_up import render_follow_up
# from utils.session import initialize_session_state
# from utils.formatting import apply_highlighting
#
# # Import RAG components
# from SmartLegalAssistant.core.embeddings import get_embedding_model
# from SmartLegalAssistant.core.vector_store import get_vector_store
# from SmartLegalAssistant.core.llm import get_language_model
# from SmartLegalAssistant.core.reranker import get_reranker
# from SmartLegalAssistant.core.answer_generator import AnswerGenerator, RAGPipeline
# from SmartLegalAssistant.core.retriever import Retriever
#
# # Load environment variables
# load_dotenv()
#
# # Set page config
# st.set_page_config(
#     page_title="Smart Legal Assistant",
#     page_icon="⚖️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )
#
# # Add custom CSS
# current_dir = os.path.dirname(os.path.abspath(__file__))
# css_path = os.path.join(current_dir, "styles", "custom.css")
#
# # Check if file exists before opening
# if os.path.exists(css_path):
#     with open(css_path) as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# else:
#     # Use inline CSS as fallback
#     st.markdown("""
#     <style>
#     .legal-citation {
#         background-color: #f0f7ff;
#         color: #0066cc;
#         font-weight: bold;
#         padding: 2px 4px;
#         border-radius: 3px;
#         border-bottom: 1px solid #0066cc;
#     }
#     </style>
#     """, unsafe_allow_html=True)
#
# # App title and description
# st.title("Smart Legal Assistant")
# st.markdown("Ask questions about legal documents and get AI-powered answers")
#
# # Initialize session state
# initialize_session_state()
#
#
# def customize_template_for_role(template_type, role, style):
#     """Modify the template based on user role and answer style."""
#     # Create a base template instruction
#     role_instruction = f"""
#     Please provide an answer tailored specifically for a {role}.
#     Only give one answer version - do not provide multiple answers for different roles.
#     Format legal citations properly using section numbers like "Section 123(4)(a)" instead of parenthetical references.
#     """
#
#     # Adjust based on answer style
#     if style == "Brief Summary":
#         role_instruction += " Keep the answer concise and to the point."
#     else:  # Detailed Explanation
#         role_instruction += " Provide a comprehensive explanation with appropriate legal detail."
#
#     # Return modified template with role-specific instructions
#     return {
#         "template_type": template_type,
#         "custom_instructions": role_instruction
#     }
#
#
# # Initialize the RAG components
# @st.cache_resource
# def initialize_rag_pipeline():
#     try:
#         # Initialize embedding model
#         embedding_model = get_embedding_model(model_type="together")
#
#         # Initialize vector store
#         vector_store = get_vector_store(
#             store_type="pinecone",
#             index_name=os.getenv("PINECONE_INDEX_NAME"),
#             namespace=os.getenv("PINECONE_NAMESPACE", "")
#         )
#
#         # Initialize LLM
#         llm = get_language_model(model_type="together")
#
#         # Initialize reranker
#         reranker = get_reranker(reranker_type="together_ai")
#
#         # Initialize retriever
#         retriever = Retriever(
#             embedding_model=embedding_model,
#             vector_store=vector_store,
#             reranker=reranker,
#             llm=llm
#         )
#
#         # Initialize answer generator
#         answer_generator = AnswerGenerator(
#             llm=llm,
#             default_template_type="legal_assistant",
#             temperature=0.2
#         )
#
#         # Initialize RAG pipeline
#         rag_pipeline = RAGPipeline(
#             retriever=retriever,
#             answer_generator=answer_generator,
#             default_top_k=25
#         )
#
#         return rag_pipeline, True
#
#     except Exception as e:
#         st.error(f"Error initializing RAG pipeline: {str(e)}")
#         return None, False
#
#
# # Initialize RAG pipeline
# rag_pipeline, initialization_success = initialize_rag_pipeline()
#
# # Render sidebar with configuration options
# selected_template, user_role, answer_style, top_k, use_reranking, use_query_expansion, temperature = render_sidebar()
#
# # Main query input and processing
# query, submitted = render_query_input()
#
# if submitted and query and initialization_success:
#     try:
#         with st.spinner("Processing your query..."):
#             # Store the query in session state
#             st.session_state.query_history.append(query)
#
#             # Store the parameters used
#             st.session_state.last_top_k = top_k
#             st.session_state.last_use_reranking = use_reranking
#             st.session_state.last_use_query_expansion = use_query_expansion
#
#             # Update this section in app.py where the query is processed
#             modified_template = customize_template_for_role(selected_template, user_role, answer_style)
#
#             # Process the query
#             result = rag_pipeline.process_query(
#                 query=query,
#                 top_k=top_k,
#                 use_query_expansion=use_query_expansion,
#                 rerank_results=use_reranking,
#                 template_type=modified_template["template_type"],
#                 custom_instructions=modified_template["custom_instructions"]  # Add this line
#             )
#
#             # Store the result in session state
#             st.session_state.last_result = result
#
#             # Apply highlighting to the answer (for legal citations)
#             highlighted_answer = apply_highlighting(result["answer"])
#
#             # Render the answer with the appropriate style
#             render_answer(highlighted_answer, result, answer_style)
#
#             # Render follow-up question input
#             render_follow_up(rag_pipeline, selected_template, user_role, answer_style)
#
#     except Exception as e:
#         st.error(f"Error processing query: {str(e)}")
#
# # Footer
# st.markdown("---")
# st.caption("Smart Legal Assistant - Powered by RAG Technology")