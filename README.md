# AI RAG Knowledge Assistant

A production-style Retrieval-Augmented Generation application built with FastAPI, ChromaDB, Sentence Transformers, OpenAI, Docker, and GitHub Actions.

The application allows users to upload TXT, Markdown, or PDF documents, generate embeddings, store document chunks in a vector database, retrieve relevant context, and answer questions through REST APIs.

## Architecture

```text
Document Upload
      |
      v
Text Extraction
      |
      v
Chunking and Normalization
      |
      v
Sentence Transformer Embeddings
      |
      v
ChromaDB Vector Storage
      |
      v
User Question
      |
      v
Query Embedding and Similarity Search
      |
      v
Relevant Document Chunks
      |
      v
OpenAI Generation or Local Fallback
      |
      v
Answer with Sources
```
