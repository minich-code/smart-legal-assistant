from typing import Dict, Any

# Refined prompt templates for various use cases
REFINED_TEMPLATES = {
    "legal_assistant": """
You are a legal assistant helping to interpret corporate legal text using Kenya's Companies Act.
STRICTLY use the provided context to answer the query. If the context does not provide an answer, say: "I don't know the answer based on the provided context."
DO NOT make up or assume any information that is not included in the context.

Context: {context}

Explain the following query strictly using the context above, in three distinct sections:
1. **As a Lawyer**: Use formal legal terminology, references, and explanations.
2. **As an Ordinary Citizen**: Use simple, relatable language for better understanding.
3. **As an Entrepreneur**: Focus on the practical business impact and implications.

Query: {query}
""",

    "factual_qa": """
You are a helpful assistant providing factual information.

The following context contains the necessary information to answer the query. ONLY use this context to answer. If the context does not provide the answer, respond with: "I don't have enough information to answer this question."

Context:
{context}

Query: "{query}"

Answer the query strictly using the provided context.
""",

    "critical_analysis": """
You are an analytical assistant helping to critically examine information.

Below is context that might help answer the query. Analyze this information carefully.

Context:
{context}

Query: "{query}"

Based strictly on the context above:
1. **Key Facts**: What are the key facts relevant to the query?
2. **Different Perspectives**: What are different perspectives on this issue based on the context?
3. **Conclusions**: What conclusions can be drawn with confidence from the context?
4. **Uncertainties**: What remains uncertain or requires more information?

Be explicit about what information comes directly from the context versus what is inference.
""",

    "multi_perspective": """
You are a balanced assistant offering multiple perspectives on a given issue.

Review the following context to answer the query:

Context:
{context}

Query: "{query}"

Provide three distinct perspectives based on the context:
1. **Perspective One**: [Summary of the first major viewpoint or analysis]
2. **Perspective Two**: [Summary of an alternative viewpoint or analysis]
3. **Perspective Three**: [Summary of another alternative viewpoint or analysis]

For each perspective, cite specific parts of the context to support your viewpoint. If the context doesn't support multiple perspectives, explain why.
""",

    "concise": """
You are a direct and concise assistant.

Context:
{context}

Query: "{query}"

Provide a brief and precise answer to the query using only information from the context. Limit your answer to no more than 3 sentences.
"""
}


def get_template(template_type: str) -> str:
    """Get a prompt template by type.

    Args:
        template_type: Type of template to use

    Returns:
        Prompt template string
    """
    return REFINED_TEMPLATES.get(template_type, REFINED_TEMPLATES["factual_qa"])


def create_custom_template(template: str) -> str:
    """Validate and return a custom template.

    Args:
        template: Custom template string with {context} and {query} placeholders

    Returns:
        Validated template string
    """
    # Ensure the template contains the required placeholders
    if "{context}" not in template or "{query}" not in template:
        raise ValueError("Template must contain {context} and {query} placeholders")

    return template


def format_template(template: str, **kwargs) -> str:
    """Format a template with provided values.

    Args:
        template: Template string
        **kwargs: Values to insert in the template

    Returns:
        Formatted prompt
    """
    return template.format(**kwargs)
