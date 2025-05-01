# import streamlit as st
#
#
# def render_follow_up(rag_pipeline, selected_template, user_role, answer_style):
#     """Render follow-up question input after an answer."""
#     # Show follow-up input only if we have a previous answer
#     if "last_result" not in st.session_state:
#         return
#
#     st.subheader("Ask a follow-up question")
#     follow_up_query = st.text_input("", key="follow_up_query")
#     follow_up_submitted = st.button("Submit Follow-up")
#
#     if follow_up_submitted and follow_up_query:
#         with st.spinner("Processing your follow-up question..."):
#             # Set follow-up mode
#             st.session_state.follow_up_mode = True
#
#             # Get the context from previous query
#             prev_query = st.session_state.query_history[-1]
#             prev_answer = st.session_state.last_result["answer"]
#
#             # Create a combined query with context
#             combined_query = f"""
#             Previous question: {prev_query}
#             Previous answer: {prev_answer}
#
#             Follow-up question: {follow_up_query}
#             """
#
#             # Process the follow-up query
#             result = rag_pipeline.process_query(
#                 query=combined_query,
#                 top_k=25,  # Can use the same parameters as before
#                 use_query_expansion=False,
#                 rerank_results=True,
#                 template_type=selected_template
#             )
#
#             # Update session state
#             st.session_state.query_history.append(follow_up_query)
#             st.session_state.last_result = result
#
#             # Apply highlighting and render
#             from utils.formatting import apply_highlighting
#             highlighted_answer = apply_highlighting(result["answer"])
#
#             # Clear the follow-up input
#             st.session_state.follow_up_query = ""
#
#             # Reset follow-up mode so the main view rerenders
#             st.session_state.follow_up_mode = False
#
#             # Rerun to update the UI
#             st.rerun()

#-----------------------------222222------------------------------------
# import streamlit as st
#
#
# def render_follow_up(rag_pipeline, template_type, user_role, answer_style):
#     """Render follow-up question input and processing."""
#     st.subheader("Ask a follow-up question")
#
#     # Follow-up question input
#     follow_up_query = st.text_input("", key="follow_up_input",
#                                     placeholder="Type your follow-up question here...")
#
#     # Process follow-up if entered
#     if follow_up_query:
#         try:
#             with st.spinner("Processing your follow-up question..."):
#                 # Get the previous query and answer
#                 previous_query = st.session_state.query_history[-1]
#                 previous_answer = st.session_state.last_result["answer"]
#
#                 # Construct a contextualized query
#                 contextualized_query = f"""
#                 Given this previous question: "{previous_query}"
#                 And this previous answer: "{previous_answer}"
#                 Please answer this follow-up question: {follow_up_query}
#                 """
#
#                 # Process the follow-up query
#                 result = rag_pipeline.process_query(
#                     query=contextualized_query,
#                     top_k=st.session_state.last_top_k,
#                     use_query_expansion=st.session_state.last_use_query_expansion,
#                     rerank_results=st.session_state.last_use_reranking,
#                     template_type=template_type
#                 )
#
#                 # Store the follow-up query in history
#                 st.session_state.query_history.append(follow_up_query)
#
#                 # Store the result
#                 st.session_state.last_result = result
#
#                 # Apply highlighting to the answer
#                 from utils.formatting import apply_highlighting
#                 highlighted_answer = apply_highlighting(result["answer"])
#
#                 # Display the answer
#                 st.subheader("Follow-up Answer")
#
#                 # Display based on style preference
#                 if answer_style == "Brief Summary":
#                     st.write(highlighted_answer)
#                 else:
#                     st.write(highlighted_answer)
#
#                     # Add button to view references
#                     if st.button("View References", key="view_refs_followup"):
#                         st.session_state.show_references = True
#                         st.rerun()
#
#                 # Add another follow-up section
#                 render_follow_up(rag_pipeline, template_type, user_role, answer_style)
#
#         except Exception as e:
#             st.error(f"Error processing follow-up: {str(e)}")