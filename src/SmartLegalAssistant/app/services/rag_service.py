from typing import Dict, Any


def process_query(query: str, user_role: str = "Ordinary Citizen", detailed: bool = False) -> Dict[str, Any]:
    """Process a query through the RAG pipeline.

    Args:
        query: The user's query
        user_role: The role of the user (affects answer style)
        detailed: Whether to provide a detailed explanation

    Returns:
        Dictionary with answer and metadata
    """
    # In a real implementation, this would call your actual RAG pipeline
    # For now, we'll simulate the response

    # Adjust template type based on user role and detail level
    template_type = "legal_assistant"  # default

    if user_role == "Lawyer":
        template_type = "legal_expert"
    elif user_role == "Researcher":
        template_type = "academic"
    elif detailed and user_role in ["Ordinary Citizen", "Entrepreneur"]:
        template_type = "legal_explainer"
    elif not detailed:
        template_type = "legal_summary"

    # Simulate the RAG pipeline call
    # In production, this would be replaced with an actual call to your pipeline

    # For demo purposes, we'll return a mock response
    mock_chunks = [
        {
            "text": "Section 143 of the Companies Act 2015 states that directors have a duty to act within their powers. Directors must act in accordance with the company's constitution and only exercise powers for the purposes for which they were conferred.",
            "reference": "Companies Act 2015, Section 143",
            "score": 0.92
        },
        {
            "text": "Section 145 of the Companies Act 2015 requires directors to promote the success of the company. A director must act in the way they consider, in good faith, would be most likely to promote the success of the company for the benefit of its members as a whole.",
            "reference": "Companies Act 2015, Section 145",
            "score": 0.88
        },
        {
            "text": "Directors in Kenya must exercise reasonable care, skill and diligence according to Section 147 of the Companies Act 2015. This means the care, skill and diligence that would be exercised by a reasonably diligent person with the general knowledge, skill and experience that may reasonably be expected.",
            "reference": "Companies Act 2015, Section 147",
            "score": 0.85
        }
    ]

    # Generate mock answer based on role and detail level
    if detailed:
        mock_answer = f"""As a response tailored for a {user_role}, I can provide a detailed explanation of directors' duties in Kenya.

Under the Companies Act 2015, directors in Kenya have several key duties:

1. **Duty to act within powers (Section 143)**: Directors must act according to the company's constitution and only exercise powers for the purposes they were granted.

2. **Duty to promote the success of the company (Section 145)**: Directors must act in good faith to promote the company's success for the benefit of its members as a whole.

3. **Duty to exercise independent judgment (Section 146)**: Directors must exercise independent judgment and not delegate their responsibilities improperly.

4. **Duty to exercise reasonable care, skill and diligence (Section 147)**: Directors must exercise reasonable care, skill and diligence that would be expected of someone with their knowledge and experience.

5. **Duty to avoid conflicts of interest (Section 148)**: Directors must avoid situations where their personal interests conflict with the company's interests.

6. **Duty not to accept benefits from third parties (Section 149)**: Directors must not accept benefits from third parties that are offered because of their position or for taking certain actions.

7. **Duty to declare interest in proposed transaction (Section 151)**: Directors must declare any personal interest in proposed transactions with the company.

These duties are legally binding, and directors can face personal liability for breaches, including financial penalties and disqualification from serving as directors in the future."""
    else:
        mock_answer = f"""For a {user_role} looking for a brief summary:

Directors in Kenya have seven main duties under the Companies Act 2015:
- Act within their powers (Section 143)
- Promote company success (Section 145)
- Exercise independent judgment (Section 146)
- Exercise reasonable care and skill (Section 147)
- Avoid conflicts of interest (Section 148)
- Reject improper third-party benefits (Section 149)
- Declare interests in transactions (Section 151)

Failure to comply can result in personal liability."""

    # Construct the result dictionary
    result = {
        "answer": mock_answer,
        "sources": [{"reference": chunk["reference"], "score": chunk["score"]} for chunk in mock_chunks],
        "retrieved_chunks": [chunk["text"] for chunk in mock_chunks],
        "formatted_chunks": mock_chunks,
        "retrieval_count": len(mock_chunks),
        "query": query,
        "template_used": template_type
    }

    return result