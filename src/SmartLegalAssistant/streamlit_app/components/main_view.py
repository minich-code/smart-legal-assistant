# import streamlit as st
#
#
# def render_query_input():
#     """Render the main query input area."""
#     # If we're in follow-up mode, don't show the main input
#     if "follow_up_mode" in st.session_state and st.session_state.follow_up_mode:
#         return None, False
#
#     query = st.text_area("Enter your legal question:", height=100, key="main_query")
#     submitted = st.button("Submit Question")
#
#     return query, submitted
#
#
# def render_answer(answer, result=None, answer_style="Detailed Explanation"):
#     """Render the answer with the appropriate style."""
#     st.header("Answer")
#
#     # Display the answer based on style
#     if answer_style == "Brief Summary":
#         # For brief summary, we might truncate or summarize
#         # For now, we'll just show the full answer
#         st.write(answer)
#     else:
#         # For detailed explanation, show the full answer
#         st.write(answer)
#
#     # Add a divider
#     st.markdown("---")



#------------------------------------------------------------------------------------
# import streamlit as st
#
#
# def render_query_input():
#     """Render the main query input area."""
#     query = st.text_area("Enter your legal question:", height=100, key="main_query")
#     submitted = st.button("Submit Question")
#
#     return query, submitted
#
#
# def render_answer(answer, result, answer_style):
#     """Render the answer with the appropriate style."""
#     st.header("Answer")
#
#     # Display answer based on chosen style
#     if answer_style == "Brief Summary":
#         st.write(answer)
#     else:  # Detailed Explanation
#         st.write(answer)
#
#         # Add "View References" button that shows/hides references in sidebar
#         if st.button("View References"):
#             # Use session state to control visibility of references
#             st.session_state.show_references = True
#             st.rerun()
#
#     # Check if we should show references in sidebar
#     if st.session_state.get("show_references", False):
#         render_references_in_sidebar(result)
#
#
# def render_references_in_sidebar(result):
#     """Render references in the sidebar."""
#     with st.sidebar:
#         st.header("Sources and References")
#
#         # Create tabs for different views
#         ref_tabs = st.tabs(["Ranked Sources", "Source Details"])
#
#         with ref_tabs[0]:
#             for i, chunk in enumerate(result["formatted_chunks"]):
#                 with st.expander(f"Source {i + 1}: {chunk['reference']} (Score: {chunk['score']:.4f})"):
#                     st.write(chunk["text"])
#
#         with ref_tabs[1]:
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
#         # Add button to hide references
#         if st.button("Hide References"):
#             st.session_state.show_references = False
#             st.rerun()