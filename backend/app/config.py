from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "KrishiNiti AI"
    app_version: str = "1.0.0"
    debug: bool = False
    cors_origins: str = "http://localhost:5173"

    ibm_watsonx_api_key: str = ""
    ibm_watsonx_project_id: str = ""
    ibm_watsonx_url: str = "https://eu-de.ml.cloud.ibm.com"
    ibm_granite_model_id: str = "ibm/granite-4-h-small"
    ibm_embedding_model_id: str = "ibm/granite-embedding-278m-multilingual"

    chroma_persist_dir: str = str(Path(__file__).resolve().parents[2] / "data" / "chroma")
    chroma_collection: str = "krishiniti_agriculture"
    top_k: int = 5
    chunk_size: int = 1200
    chunk_overlap: int = 180

    model_max_new_tokens: int = 500
    model_temperature: float = 0.2
    request_timeout_seconds: int = 90

    model_config = SettingsConfigDict(
    env_file=Path(__file__).resolve().parents[2] / ".env",
    case_sensitive=False,
    extra="ignore",
)

@lru_cache
def get_settings() -> Settings:
    return Settings()
