
import streamlit as st

def apply_styling():
    """Apply custom CSS styling to the app."""
    st.markdown("""
    <style>
        .stButton > button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            background-color: #4285f4;
            color: white;
            font-weight: 500;
        }

        .stExpander {
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        }

        .stExpander > div {
            padding: 15px;
        }

        .stTextArea > div > div > textarea {
            border-radius: 5px;
            border: 1px solid #e0e0e0;
        }

        h1, h2, h3 {
            color: #1a73e8;
        }

        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }

        .stDataFrame {
            border-radius: 5px;
            border: 1px solid #e0e0e0;
        }
    </style>
    """, unsafe_allow_html=True)