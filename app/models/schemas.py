from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    service: str
    environment: str


class DocumentUploadResponse(BaseModel):
    filename: str
    document_id: str
    chunks_created: int
    message: str


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Question to answer using uploaded documents.",
    )


class SourceChunk(BaseModel):
    content: str
    metadata: dict[str, Any]
    distance: float | None = None


class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceChunk]
    generation_mode: str