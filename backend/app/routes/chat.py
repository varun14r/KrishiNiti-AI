from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/api/v1", tags=["chat"])
_service = None

def get_service():
    global _service
    if _service is None:
        _service = ChatService()
    return _service

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        return get_service().answer(request)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {exc}")
