
import streamlit as st

def render_user_input(is_followup=False):
    """Render the user input component
    Args:
        Is followup: Boolean indicating if this is a followup question

    Returns:
        Tuple of (query, submitted)

    """
    if is_followup:
        label = "Ask a follow-up question:"
        placeholder = "E.g. Can you explain that in simple terms?"

    else:
        label = "What legal question do you want to ask?"
        placeholder = "E.g. What are the duties of company directors in Kenya?"

    query = st.text_area(

        label,
        height = 100,
        placeholder = placeholder,
        key = "query_input"
    )

    submitted = st.button("Submit" if not is_followup else "Ask Follow up")

    return query, submitted

