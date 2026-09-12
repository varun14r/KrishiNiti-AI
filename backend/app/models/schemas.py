from pydantic import BaseModel, Field
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str = Field(min_length=2, max_length=4000)
    language: Optional[str] = "auto"
    location: Optional[str] = None
    crop: Optional[str] = None
    crop_age: Optional[str] = None
    soil_type: Optional[str] = None
    irrigation: Optional[str] = None

class Source(BaseModel):
    document: str
    topic: str
    score: float

class ChatResponse(BaseModel):
    answer: str
    assessment: str = ""
    recommended_actions: List[str] = []
    what_to_monitor: List[str] = []
    limitations: List[str] = []
    sources: List[Source] = []
    live_data_available: bool = False
    model: str
    retrieval_used: bool

class HealthResponse(BaseModel):
    status: str
    granite_configured: bool
    embedding_configured: bool
    vector_store: str
