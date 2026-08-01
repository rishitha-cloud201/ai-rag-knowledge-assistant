from fastapi import FastAPI

from app.api.routes import router
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=(
        "Production-style RAG knowledge assistant with "
        "document upload, vector search, and AI-generated answers."
    ),
    version="1.0.0",
)

app.include_router(
    router,
    prefix="/api/v1",
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": settings.app_name,
        "documentation": "/docs",
        "health": "/api/v1/health",
    }