from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.models.schemas import HealthResponse
from app.routes.chat import router as chat_router

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.cors_origins.split(",") if x.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)

@app.get("/api/v1/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="ok",
        granite_configured=bool(settings.ibm_watsonx_api_key and settings.ibm_watsonx_project_id),
        embedding_configured=bool(settings.ibm_watsonx_api_key and settings.ibm_watsonx_project_id),
        vector_store="ChromaDB",
    )

@app.get("/")
def root():
    return {"name": settings.app_name, "version": settings.app_version, "docs": "/docs"}
