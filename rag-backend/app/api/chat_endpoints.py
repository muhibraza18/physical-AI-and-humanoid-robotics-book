import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Optional

from app.models.rag_models import ChatQuery, ChatResponse # Import new models
from app.services.retriever import retrieve_chunks # Import actual retriever
from app.services.llm_orchestrator import generate_llm_response # Import actual LLM orchestrator
from app.core.database import get_db # Import get_db dependency
from app.services.chat_service import ChatService # Import ChatService

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_query: ChatQuery, db: AsyncSession = Depends(get_db)):
    """
    Handles chat queries, performs RAG, and returns a generated response.
    Saves the chat interaction to the database.
    """
    collection_name = os.environ.get("QDRANT_COLLECTION_NAME", "default_book_rag_collection") # Defined in plan/config
    
    retrieved_chunks = retrieve_chunks(chat_query.query, collection_name)
    
    if not retrieved_chunks:
        answer = "Insufficient data. No relevant information found in the book."
        evidence = []
    else:
        llm_response = generate_llm_response(chat_query.query, retrieved_chunks)
        answer = llm_response["answer"]
        evidence = llm_response["evidence"]
    
    chat_service = ChatService(db)
    await chat_service.save_chat_history(
        session_id=chat_query.session_id if chat_query.session_id else "anonymous", # Use provided session_id or 'anonymous'
        query=chat_query.query,
        response=answer,
        retrieved_evidence=evidence,
    )
    
    return ChatResponse(answer=answer, evidence=evidence)

@router.post("/select-and-ask", response_model=ChatResponse)
async def select_and_ask_endpoint(chat_query: ChatQuery, db: AsyncSession = Depends(get_db)):
    """
    Handles queries about selected text, performs RAG, and returns a generated response.
    Saves the chat interaction to the database.
    """
    if not chat_query.selected_text:
        raise HTTPException(status_code=400, detail="selected_text is required for select-and-ask")
    
    collection_name = os.environ.get("QDRANT_COLLECTION_NAME", "default_book_rag_collection") # Defined in plan/config
    
    # In a real scenario, retrieval could be biased by selected_text
    retrieved_chunks = retrieve_chunks(chat_query.query, collection_name)
    
    if not retrieved_chunks:
        answer = "Insufficient data. No relevant information found in the book."
        evidence = []
    else:
        # Combine selected_text with retrieved_chunks for LLM context
        llm_response = generate_llm_response(chat_query.query, retrieved_chunks, selected_text=chat_query.selected_text)
        answer = llm_response["answer"]
        evidence = llm_response["evidence"]

    chat_service = ChatService(db)
    await chat_service.save_chat_history(
        session_id=chat_query.session_id if chat_query.session_id else "anonymous", # Use provided session_id or 'anonymous'
        query=chat_query.query,
        response=answer,
        retrieved_evidence=evidence,
    )
    
    return ChatResponse(answer=answer, evidence=evidence)