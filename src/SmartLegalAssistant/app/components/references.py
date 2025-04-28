
import streamlit as st
import pandas as pd

def render_references(formatted_chunks):
    """Render the references in a table format.

    Args:
        formatted_chunks: List of dictionaries with chunk information
    """
    if not formatted_chunks:
        st.info("No references available for this query.")
        return

    st.subheader("Sources and References")

    # Create a DataFrame for better display
    df = pd.DataFrame([
        {
            "Source": chunk["reference"],
            "Relevance Score": f"{chunk['score']:.2f}",
            "Text Excerpt": chunk["text"][:150] + "..." if len(chunk["text"]) > 150 else chunk["text"]
        }
        for chunk in formatted_chunks
    ])

    # Sort by relevance score (descending)
    df = df.sort_values("Relevance Score", ascending=False)

    # Display as a table
    st.dataframe(df, use_container_width=True)

    # Option to view full text of each reference
    selected_ref = st.selectbox(
        "View full text of reference:",
        options=["Select a reference..."] + [f"{ i +1}. {chunk['reference']}"
                                             for i, chunk in enumerate(formatted_chunks)]
    )

    if selected_ref != "Select a reference...":
        idx = int(selected_ref.split(".")[0]) - 1
        st.text_area(
            f"Full text of {formatted_chunks[idx]['reference']}",
            value=formatted_chunks[idx]["text"],
            height=300
        )