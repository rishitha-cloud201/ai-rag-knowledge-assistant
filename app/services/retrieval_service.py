from typing import Any

from app.config import get_settings
from app.services.embedding_service import EmbeddingService


class RetrievalService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.embedding_service = EmbeddingService()

    def retrieve(self, question: str) -> list[dict[str, Any]]:
        query_embedding = self.embedding_service.embed_query(question)

        results = self.embedding_service.collection.query(
            query_embeddings=[query_embedding],
            n_results=self.settings.top_k_results,
            include=["documents", "metadatas", "distances"],
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        sources: list[dict[str, Any]] = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            sources.append(
                {
                    "content": document,
                    "metadata": metadata or {},
                    "distance": float(distance),
                }
            )

        return sources