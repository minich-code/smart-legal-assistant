import streamlit as st
from components.user_input import render_user_input
from components.answer_display import render_answer
from components.references import render_references
from utils.session import initialize_session, update_history
from utils.styling import apply_styling
from services.rag_service import process_query

def main():
    apply_styling()
    initialize_session()

    st.title("Smart Legal Assistant")
    st.markdown("Ask questions about legal matters and get accurate answers with references.")

    # Sidebar
    with st.sidebar:
        st.title("Options")

        user_role = st.selectbox(
            "Select your role",
            ["Ordinary Citizen", "Entrepreneur", "Researcher", "Lawyer", "Law Student"]
        )

        answer_style = st.radio(
            "Answer style:",
            ["Brief Summary", "Detailed Explanation"]
        )

        if st.session_state.get("formatted_chunks"):
            with st.expander("Sources and References"):
                render_references(st.session_state.formatted_chunks)

    # Show conversation history
    if st.session_state.get("history"):
        st.subheader("Recent History")
        for i, (q, a) in enumerate(st.session_state.history[-3:]):
            with st.expander(f"Q: {q}", expanded=False):
                st.markdown(a)

    # 🛠 NEW SECTION: User input
    query, submitted = render_user_input(is_followup="answer" in st.session_state)

    # 🛠 NEW LOGIC: Fresh query handling
    if submitted and query:
        st.session_state.answer = None  # Clear previous answer
        st.session_state.sources = None
        st.session_state.formatted_chunks = None

        with st.spinner("Generating Answer..."):
            result = process_query(
                query=query,
                user_role=user_role,
                detailed=(answer_style == "Detailed Explanation")
            )

            st.session_state.answer = result["answer"]
            st.session_state.sources = result["sources"]
            st.session_state.formatted_chunks = result["formatted_chunks"]
            st.session_state.query = query

            update_history(query, result["answer"])

    # 🛠 Display the answer
    if st.session_state.get("answer"):
        render_answer(st.session_state.answer)

if __name__ == "__main__":
    main()

