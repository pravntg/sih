"""
Conversational Marine Advisory API Endpoints
"""
from fastapi import APIRouter, HTTPException
from ...models.chat import ChatRequest, ChatResponse
from ...services.marine_chat_service import marine_chat_service

router = APIRouter(prefix="", tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat_marine_advisor(request: ChatRequest) -> ChatResponse:
    """
    Conversational marine reasoning endpoint with automated safety threshold checking and provenance tracking.
    """
    try:
        response = marine_chat_service.process_message(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Marine chat advisor failure: {str(e)}")
