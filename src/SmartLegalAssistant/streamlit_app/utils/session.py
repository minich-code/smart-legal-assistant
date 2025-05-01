# import streamlit as st
#
#
# def initialize_session_state():
#     """Initialize session state variables."""
#     if "query_history" not in st.session_state:
#         st.session_state.query_history = []
#
#     if "follow_up_mode" not in st.session_state:
#         st.session_state.follow_up_mode = False


import streamlit as st


def initialize_session_state():
    """Initialize session state variables."""
    if "query_history" not in st.session_state:
        st.session_state.query_history = []

    if "last_result" not in st.session_state:
        st.session_state.last_result = None

    if "show_references" not in st.session_state:
        st.session_state.show_references = False

    # Store last used parameters
    if "last_top_k" not in st.session_state:
        st.session_state.last_top_k = 25

    if "last_use_reranking" not in st.session_state:
        st.session_state.last_use_reranking = True

    if "last_use_query_expansion" not in st.session_state:
        st.session_state.last_use_query_expansion = False