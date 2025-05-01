#
#
# # utils/formatting.py
# import re
# import streamlit as st
#
#
# def highlight_legal_citations(text):
#     """Apply highlighting to legal citations in text."""
#     # Pattern for legal citations like "Section 145 of Companies Act"
#     pattern = r'(Section|Article|Regulation|Rule)\s+(\d+)(\s+of\s+[\w\s]+Act)'
#
#     # Replace with highlighted version
#     highlighted_text = re.sub(
#         pattern,
#         r'<span class="legal-citation">\1 \2\3</span>',
#         text
#     )
#
#     # Return with HTML rendering enabled
#     return st.markdown(highlighted_text, unsafe_allow_html=True)
#
#
# # Alias for backward compatibility
# apply_highlighting = highlight_legal_citations


import re
import streamlit as st


def apply_highlighting(text):
    """Apply highlighting to legal citations in text."""
    # Pattern for section references like "Section 345 (2) (a)"
    section_pattern = r'(Section \d+(\s*\(\d+\))*(\s*\([a-z]\))*)'

    # Pattern for act references like "Companies Act 2006"
    act_pattern = r'([A-Z][a-z]+(\s+[A-Z][a-z]+)*\s+Act(\s+of)?\s+\d{4})'

    # Pattern for legal case citations like "Smith v. Jones"
    case_pattern = r'([A-Z][a-z]+\s+v\.\s+[A-Z][a-z]+)'

    # Replace section references
    highlighted_text = re.sub(
        section_pattern,
        r'<span class="legal-citation">\1</span>',
        text
    )

    # Replace act references
    highlighted_text = re.sub(
        act_pattern,
        r'<span class="legal-citation">\1</span>',
        highlighted_text
    )

    # Replace case citations
    highlighted_text = re.sub(
        case_pattern,
        r'<span class="legal-citation">\1</span>',
        highlighted_text
    )

    return highlighted_text