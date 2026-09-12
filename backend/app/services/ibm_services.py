from typing import Sequence
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.embeddings import Embeddings
from ibm_watsonx_ai.foundation_models.schema import TextGenParameters
from app.config import get_settings

class IBMEmbeddingService:
    def __init__(self):
        s = get_settings()
        if not s.ibm_watsonx_api_key or not s.ibm_watsonx_project_id:
            raise RuntimeError("IBM watsonx.ai credentials are not configured.")
        credentials = Credentials(url=s.ibm_watsonx_url, api_key=s.ibm_watsonx_api_key)
        self.model = Embeddings(
            model_id=s.ibm_embedding_model_id,
            credentials=credentials,
            project_id=s.ibm_watsonx_project_id,
        )

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        return self.model.embed_documents(list(texts))

    def embed_query(self, text: str) -> list[float]:
        return self.model.embed_query(text)

class IBMGraniteService:
    def __init__(self):
        s = get_settings()
        if not s.ibm_watsonx_api_key or not s.ibm_watsonx_project_id:
            raise RuntimeError("IBM watsonx.ai credentials are not configured.")
        credentials = Credentials(url=s.ibm_watsonx_url, api_key=s.ibm_watsonx_api_key)
        params = {
            "max_new_tokens": s.model_max_new_tokens,
            "temperature": s.model_temperature, 
        }
        self.model_id = s.ibm_granite_model_id
        self.model = ModelInference(
            model_id=self.model_id,
            credentials=credentials,
            project_id=s.ibm_watsonx_project_id,
            params=params,
        )

    def generate(self, prompt: str) -> str:
        result = self.model.generate_text(prompt=prompt)
        if isinstance(result, str):
            return result.strip()
        if isinstance(result, dict):
            results = result.get("results", [])
            if results:
                return results[0].get("generated_text", "").strip()
        return str(result).strip()
