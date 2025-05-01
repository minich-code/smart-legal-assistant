# import streamlit as st
#
#
# def render_sidebar():
#     """Render the sidebar with configuration options."""
#     st.sidebar.header("Configuration")
#
#     # Template selection
#     template_options = ["legal_assistant", "factual_qa", "critical_analysis",
#                         "multi_perspective", "concise"]
#     selected_template = st.sidebar.selectbox("Select Response Template",
#                                              template_options,
#                                              index=0)
#
#     # User role selection
#     user_role = st.sidebar.selectbox(
#         "I am a...",
#         ["Ordinary Citizen", "Entrepreneur", "Lawyer", "Researcher"]
#     )
#
#     # Answer style selection
#     answer_style = st.sidebar.radio(
#         "Answer Style",
#         ["Brief Summary", "Detailed Explanation"],
#         horizontal=True
#     )
#
#     # Advanced options in expander
#     with st.sidebar.expander("Advanced Options"):
#         top_k = st.slider("Number of chunks to retrieve", 5, 50, 25)
#         use_reranking = st.checkbox("Use reranking", value=True)
#         use_query_expansion = st.checkbox("Use query expansion", value=False)
#         temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.1)
#
#     # References expander (initially empty, will be populated after query)
#     with st.sidebar.expander("Sources and References", expanded=False):
#         if "last_result" in st.session_state and st.session_state.last_result:
#             result = st.session_state.last_result
#
#             # Display table of sources with scores
#             source_data = [
#                 {
#                     "Index": i + 1,
#                     "Reference": chunk["reference"],
#                     "Score": f"{chunk['score']:.4f}",
#                     "Preview": chunk["text"][:100] + "..."
#                 }
#                 for i, chunk in enumerate(result["formatted_chunks"])
#             ]
#             st.dataframe(source_data)
#
#             # Display detailed sources
#             for i, chunk in enumerate(result["formatted_chunks"]):
#                 with st.expander(f"Source {i + 1}: {chunk['reference']} (Score: {chunk['score']:.4f})"):
#                     st.write(chunk["text"])
#
#     # Help information
#     with st.sidebar.expander("Help"):
#         st.markdown("""
#         **How to use this app:**
#         1. Enter your legal question in the text area
#         2. Select your role to get tailored responses
#         3. Choose between brief or detailed answers
#         4. Click 'Submit Question'
#         5. View sources in the sidebar if needed
#
#         **Role Options:**
#         - **Ordinary Citizen**: Simple, plain language explanations
#         - **Entrepreneur**: Practical business implications
#         - **Lawyer**: Formal legal terminology and references
#         - **Researcher**: Academic and research-focused perspective
#         """)
#
#     return selected_template, user_role, answer_style, top_k, use_reranking, use_query_expansion, temperature
#------------------------------------------------------------------------
# import streamlit as st
#
#
# def render_sidebar():
#     """Render the sidebar with all configuration options."""
#     st.sidebar.header("Configuration")
#
#     # User role selection
#     user_role = st.sidebar.selectbox(
#         "Select Your Role",
#         ["Ordinary Citizen", "Entrepreneur", "Researcher", "Lawyer", "Student", "Legal Professional"],
#         index=0
#     )
#
#     # Template selection
#     template_options = ["legal_assistant", "factual_qa", "critical_analysis",
#                         "multi_perspective", "concise"]
#     selected_template = st.sidebar.selectbox(
#         "Select Response Template",
#         template_options,
#         index=0
#     )
#
#     # Answer style selection
#     answer_style = st.sidebar.radio(
#         "Answer Style",
#         ["Brief Summary", "Detailed Explanation"],
#         index=0
#     )
#
#     # Advanced options
#     with st.sidebar.expander("Advanced Options"):
#         top_k = st.slider("Number of chunks to retrieve", 5, 50, 25)
#         use_reranking = st.checkbox("Use reranking", value=True)
#         use_query_expansion = st.checkbox("Use query expansion", value=False)
#         temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.1)
#
#     # Help section
#     with st.sidebar.expander("Help"):
#         st.markdown("""
#         **How to use this app:**
#         1. Enter your legal question in the text area
#         2. Adjust your role and answer style as needed
#         3. Click 'Submit Question'
#
#         **Template Options:**
#         - **Legal Assistant**: Detailed legal interpretation in multiple perspectives
#         - **Factual QA**: Just the facts from the documents
#         - **Critical Analysis**: Analytical breakdown of the information
#         - **Multi Perspective**: Multiple viewpoints on the issue
#         - **Concise**: Brief, to-the-point answers
#
#         **User Roles:**
#         Your selected role helps tailor responses to your background and needs.
#         """)
#
#     return selected_template, user_role, answer_style, top_k, use_reranking, use_query_expansion, temperature