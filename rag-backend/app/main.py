import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware # Import CORSMiddleware
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

from app.models.rag_models import HealthCheckResponse
from app.core.database import init_db, check_db_connection

# Import routers (will be created in subsequent steps)
from app.api.chat_endpoints import router as chat_endpoints_router
from app.api.ingestion_endpoints import router as ingestion_endpoints_router
from app.api.history_endpoints import router as history_endpoints_router

app = FastAPI(
    title="RAG Chatbot Backend",
    description="FastAPI backend for the Integrated RAG Chatbot System.",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production to specific origins (e.g., your Docusaurus URL)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

QDRANT_COLLECTION_NAME = os.environ.get("QDRANT_COLLECTION_NAME", "default_book_rag_collection") # Default or get from env

@app.on_event("startup")
async def startup_event():
    """
    Handles startup events for the FastAPI application.
    Initializes the database and checks connection.
    """
    await init_db() # Create tables if they don't exist
    await check_db_connection() # Verify database connection

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    API endpoint for checking the health of the FastAPI application.
    Returns:
        HealthCheckResponse: A dictionary indicating the status of the API.
    """
    return {"status": "ok"}

# Include routers
app.include_router(chat_endpoints_router, prefix="/api/chat", tags=["Chat"])
app.include_router(ingestion_endpoints_router, prefix="/api/ingest", tags=["Ingestion"])
app.include_router(history_endpoints_router, prefix="/api/history", tags=["History"])

# The /ingest_chunk endpoint is removed from here as it will be in ingestion_endpoints.py