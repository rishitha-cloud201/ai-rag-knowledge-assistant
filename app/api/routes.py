from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import get_settings
from app.models.schemas import (
    DocumentUploadResponse,
    HealthResponse,
    QuestionRequest,
    QuestionResponse,
    SourceChunk,
)
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.generation_service import GenerationService
from app.services.retrieval_service import RetrievalService

router = APIRouter()

settings = get_settings()
document_service = DocumentService()
embedding_service = EmbeddingService()
retrieval_service = RetrievalService()
generation_service = GenerationService()


@router.get(
    "/health",
    response_model=HealthResponse,
)
def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        service=settings.app_name,
        environment=settings.app_env,
    )


@router.post(
    "/documents/upload",
    response_model=DocumentUploadResponse,
)
async def upload_document(
    file: UploadFile = File(...),
) -> DocumentUploadResponse:
    try:
        document_id, filename, text = (
            await document_service.save_and_extract(file)
        )

        chunks = document_service.create_chunks(text)

        chunk_count = embedding_service.add_document(
            document_id=document_id,
            filename=filename,
            chunks=chunks,
        )

        return DocumentUploadResponse(
            filename=filename,
            document_id=document_id,
            chunks_created=chunk_count,
            message="Document uploaded and indexed successfully.",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Document processing failed.",
        ) from exc


@router.post(
    "/questions/ask",
    response_model=QuestionResponse,
)
def ask_question(
    request: QuestionRequest,
) -> QuestionResponse:
    try:
        sources = retrieval_service.retrieve(request.question)

        answer, generation_mode = (
            generation_service.generate_answer(
                question=request.question,
                sources=sources,
            )
        )

        return QuestionResponse(
            question=request.question,
            answer=answer,
            sources=[
                SourceChunk(**source)
                for source in sources
            ],
            generation_mode=generation_mode,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Question processing failed.",
        ) from exc