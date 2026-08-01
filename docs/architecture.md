# Architecture

## Request Flow

1. A user uploads a TXT, Markdown, or PDF document.
2. The document service extracts and normalizes text.
3. The text is divided into overlapping chunks.
4. Sentence Transformers generates embeddings.
5. ChromaDB stores document chunks and vectors.
6. A user submits a question.
7. The question is converted into an embedding.
8. ChromaDB retrieves the most relevant document chunks.
9. The generation service creates an answer using retrieved context.
10. If no OpenAI API key is configured, the application returns a local fallback response.

## Components

- FastAPI: REST API and Swagger documentation
- Sentence Transformers: Local embeddings
- ChromaDB: Persistent vector storage
- OpenAI API: Optional answer generation
- Pydantic: Validation and configuration
- Docker: Containerized deployment
- GitHub Actions: Automated testing
