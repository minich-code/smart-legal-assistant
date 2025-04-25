# smart-legal-assistants using Retrieval Augmented Generation 

A scalable Retrieval-Augmented Generation application for answering questions using your document knowledge base.

## Features

- **Document Retrieval**: Efficiently retrieve relevant information from your vector database
- **Advanced RAG Pipeline**: Modular components for embeddings, retrieval, and response generation
- **Customizable Prompts**: Multiple prompt templates for different response styles
- **Query Enhancement**: Optional query expansion and result reranking
- **User-Friendly Interface**: Clean Streamlit UI with feedback collection
- **Deployment Ready**: Docker and Render configurations included

## Setup Instructions

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
TOGETHER_API_KEY=your_together_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX_NAME=your_pinecone_index_name
PINECONE_NAMESPACE=optional_namespace
```

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/rag-assistant.git
   cd rag-assistant
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   streamlit run app/main.py
   ```

### Docker Deployment

1. Build the Docker image:
   ```
   docker build -t rag-assistant .
   ```

2. Run the container:
   ```
   docker run -p 8501:8501 --env-file .env rag-assistant
   ```

### Render Deployment

1. Connect your GitHub repository to Render
2. Create a new Web Service using the `render.yaml` configuration
3. Set the environment variables in the Render dashboard

## Project Structure

- `app/`: Streamlit application code
- `core/`: Core RAG components (embeddings, vector store, LLM)
- `utils/`: Utilities (prompt templates, logging)
- `Dockerfile`: Docker configuration
- `render.yaml`: Render deployment configuration

## Customization

### Adding New Prompt Templates

Add your custom templates to `utils/prompt_templates.py` by extending the `DEFAULT_TEMPLATES` dictionary.

### Using Different Embedding Models

Implement a new embedding model class in `core/embeddings.py` by extending the `EmbeddingModel` base class.

### Changing Vector Stores

Implement a new vector store in `core/vector_store.py` by extending the `VectorStore` base class.

## Advanced Retrieval Techniques

- **Query Expansion**: Enhances recall by adding related terms to the query
- **Result Reranking**: Improves precision by reordering results based on relevance
- **Hybrid Search**: Combines vector and keyword-based search (configurable in settings)

## Feedback and Improvement

The system collects user feedback to help improve response quality. Feedback is stored in `logs/feedback/`.