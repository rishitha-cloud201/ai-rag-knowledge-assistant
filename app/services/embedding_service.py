from pathlib import Path

import chromadb
from chromadb.api.models.Collection import Collection
from sentence_transformers import SentenceTransformer

from app.config import get_settings


class EmbeddingService:
    def __init__(self) -> None:
        self.settings = get_settings()

        persist_directory = Path(
            self.settings.chroma_persist_directory
        )
        persist_directory.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=str(persist_directory)
        )

        self.collection: Collection = (
            self.client.get_or_create_collection(
                name=self.settings.collection_name,
                metadata={"hnsw:space": "cosine"},
            )
        )

        self.model = SentenceTransformer(
            self.settings.embedding_model
        )

    def add_document(
        self,
        document_id: str,
        filename: str,
        chunks: list[str],
    ) -> int:
        if not chunks:
            raise ValueError("No document chunks were provided.")

        embeddings = self.model.encode(
            chunks,
            normalize_embeddings=True,
        ).tolist()

        ids = [
            f"{document_id}-chunk-{index}"
            for index in range(len(chunks))
        ]

        metadata = [
            {
                "document_id": document_id,
                "filename": filename,
                "chunk_index": index,
            }
            for index in range(len(chunks))
        ]

        self.collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadata,
        )

        return len(chunks)

    def embed_query(self, query: str) -> list[float]:
        return self.model.encode(
            query,
            normalize_embeddings=True,
        ).tolist()