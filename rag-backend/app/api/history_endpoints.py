from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models.rag_models import ChatResponse # Using ChatResponse to model chat history entries for now
from app.core.database import get_db
from app.services.chat_service import ChatService
from app.models.db_models import ChatHistory

router = APIRouter()

@router.get("/history/{session_id}", response_model=List[ChatResponse])
async def get_chat_history_endpoint(session_id: str, db: AsyncSession = Depends(get_db)):
    """
    Retrieves the chat history for a given session ID.
    """
    chat_service = ChatService(db)
    history: List[ChatHistory] = await chat_service.get_chat_history(session_id)

    if not history:
        raise HTTPException(status_code=404, detail="Chat history not found for this session.")
    
    # Convert ChatHistory ORM objects to ChatResponse-like structure
    # For now, we'll return a simple list of query/response pairs
    formatted_history = []
    for entry in history:
        # Assuming ChatResponse structure can represent history well enough
        # In a more complex scenario, a dedicated HistoryEntryResponse model might be better
        formatted_history.append(ChatResponse(
            answer=entry.response,
            evidence=entry.retrieved_evidence if entry.retrieved_evidence else [],
        ))
    
    return formatted_history

@router.post("/session", response_model=str)
async def create_session_endpoint(user_id: str = None, db: AsyncSession = Depends(get_db)):
    """
    Creates a new user session and returns the session ID.
    """
    chat_service = ChatService(db)
    session_id = await chat_service.create_new_session(user_id)
    return session_id