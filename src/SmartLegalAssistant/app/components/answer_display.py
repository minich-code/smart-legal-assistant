import streamlit as st
from utils.highlighting import highlight_legal_citations


def render_answer(answer_text):
    """Render the answer with highlighted legal citations.

    Args:
        answer_text: The text of the answer
    """
    # Apply highlighting to legal citations
    highlighted_answer = highlight_legal_citations(answer_text)

    # Display in a nice card format
    st.subheader("Answer")

    with st.container():
        st.markdown("""
        <div style="background-color: #f8f9fa; border-radius: 10px; padding: 20px; 
                    border-left: 5px solid #4285f4;">
            {}
        </div>
        """.format(highlighted_answer), unsafe_allow_html=True)