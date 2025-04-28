import re


def highlight_legal_citations(text):
    """Highlight legal citations in the text.

    Args:
        text: The text to process

    Returns:
        HTML formatted text with highlighted citations
    """
    # Pattern for legal citations
    # Examples: "Section 145 of Companies Act", "Article 15(2)", etc.
    patterns = [
        r'(Section \d+[\w\(\)]*( of the| of)? [\w\s]+ Act)',
        r'(Article \d+[\w\(\)]*( of the| of)? [\w\s]+)',
        r'(Regulation \d+[\w\(\)]*( of the| of)? [\w\s]+)',
        r'(Rule \d+[\w\(\)]*( of the| of)? [\w\s]+)',
        r'([\w\s]+ Act,? \d{4})',
        r'([\w\s]+ Act \(No\. \d+\))'
    ]

    # Apply highlighting
    for pattern in patterns:
        text = re.sub(
            pattern,
            r'<span style="background-color: #e8f0fe; padding: 2px 4px; border-radius: 3px; font-weight: 500;">\1</span>',
            text
        )

    return text