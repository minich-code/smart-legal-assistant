

# Prompt template for RAG responses 

from typing import Dict, Any 

# Default prompt templates for various use cases 
DEFAULT_TEMPLATES = {
    "legal_assistant": """

    You are a legal assistant helping interpret corporate legal text using Kenya's Company.
    ONLY USE the provided context to answer the query. If you don't know the answer, just say that you don't know. DO NOT make up an answer or assumptions 
    that are not in the context.
 

    Context: {context}

    Explain the following query strictly using the context above, in three distinct paragraphs
    1. As a Lawyer - using legal terminology and references.
    2. As an ordinary citizen - using simple and relatable language. 
    3. As an entrepreneur - focusing on practical business impact.

    Query: {query}
    """,

    "factual_qa": """
You are a helpful assistant providing factual information.

The following context contains information to answer the query. ONLY use this context to answer.

Context:
{context}

Query: "{query}"

Answer the query based ONLY on the provided context. If the context doesn't contain the answer, say "I don't have enough information to answer this question."
""",
    
    "critical_analysis": """
You are an analytical assistant helping to critically examine information.

Below is context that might help answer the query. Analyze this information carefully.

Context:
{context}

Query: "{query}"

Based strictly on the context above:
1. What are the key facts relevant to the query?
2. What are different perspectives on this issue?
3. What conclusions can be drawn with confidence?
4. What remains uncertain or requires more information?

Be explicit about what information comes directly from the context versus what is inference.
""",
    
    "multi_perspective": """
You are a balanced assistant offering multiple perspectives.

Review the following context to answer the query:

Context:
{context}

Query: "{query}"

Please provide three different perspectives on this query based only on the context provided:
1. Perspective One: [summary of first major viewpoint]
2. Perspective Two: [summary of alternative viewpoint]
3. Perspective Three: [summary of another alternative viewpoint]

For each perspective, cite specific parts of the context. If the context doesn't support multiple perspectives, explain why.
""",
    
    "concise": """
You are a direct and concise assistant.

Context:
{context}

Query: "{query}"

Answer the query in no more than 3 sentences, using only information from the context. Be direct and precise.
"""
}

def get_template(template_type: str) -> str:
    """Get a prompt template by type.
    
    Args:
        template_type: Type of template to use
        
    Returns:
        Prompt template string
    """
    return DEFAULT_TEMPLATES.get(template_type, DEFAULT_TEMPLATES["factual_qa"])

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
