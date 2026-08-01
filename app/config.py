from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI RAG Knowledge Assistant"
    app_env: str = "development"

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    chroma_persist_directory: str = "./data/chroma"
    collection_name: str = "knowledge_base"

    embedding_model: str = "all-MiniLM-L6-v2"
    top_k_results: int = 4
    chunk_size: int = 700
    chunk_overlap: int = 100

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()