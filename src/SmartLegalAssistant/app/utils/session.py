import streamlit as st


def initialize_session():
    """Initialize session state variables if they don't exist."""
    if "history" not in st.session_state:
        st.session_state.history = []  # List of (query, answer) tuples

    if "answer" not in st.session_state:
        st.session_state.answer = None

    if "sources" not in st.session_state:
        st.session_state.sources = None

    if "formatted_chunks" not in st.session_state:
        st.session_state.formatted_chunks = None

    if "query" not in st.session_state:
        st.session_state.query = None


def update_history(query, answer):
    """Update the conversation history.

    Args:
        query: The user's query
        answer: The system's answer
    """
    # Add the new Q&A pair to history
    st.session_state.history.append((query, answer))

    # Keep only the last 5 items
    if len(st.session_state.history) > 5:
        st.session_state.history = st.session_state.history[-5:]