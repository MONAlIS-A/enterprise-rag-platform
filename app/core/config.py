from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    app_name: str = "enterprise-rag-platform"
    app_env: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Database
    database_url: str

    # Redis
    redis_url: str

    # Celery
    celery_broker_url: str
    celery_result_backend: str

    # LLM
    llm_provider: str = ""
    llm_model: str = ""
    llm_api_key: str = ""

    # Embedding
    embedding_provider: str = ""
    embedding_model: str = ""
    embedding_api_key: str = ""

    # Retrieval
    retrieval_top_k: int = 10
    rerank_top_k: int = 5

    chunk_size: int = 800
    chunk_overlap: int = 120

    max_context_tokens: int = 6000

    # Security
    auth_enabled: bool = False
    jwt_secret_key: str = ""

    # Observability
    enable_tracing: bool = False
    enable_metrics: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()