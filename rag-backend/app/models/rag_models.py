from typing import List, Dict, Optional
from pydantic import BaseModel, Field

# --- Data Models for Qdrant Chunks ---

class ChunkMetadata(BaseModel):
    """
    Metadata associated with each text chunk.
    """
    source_chapter: str = Field(..., description="The chapter the chunk originated from (e.g., 'chapter-01').")
    source_section: Optional[str] = Field(None, description="The section or heading within the chapter.")
    page_number: Optional[int] = Field(None, description="The page number if applicable.")
    original_slug: Optional[str] = Field(None, description="The original Docusaurus slug for the source page.")
    chunk_hash: str = Field(..., description="SHA-256 hash of the chunk content for change detection.")

class TextChunk(BaseModel):
    """
    Represents a single text chunk with its content, embedding, and metadata.
    """
    id: str = Field(..., description="Unique identifier for the chunk.")
    content: str = Field(..., description="The raw text content of the chunk.")
    embedding: List[float] = Field(..., description="Vector embedding of the chunk content.")
    metadata: ChunkMetadata = Field(..., description="Metadata associated with the chunk.")

# --- API Request/Response Models ---

class IngestChunkPayload(BaseModel):
    """
    Payload for ingesting a single text chunk.
    This will be used by the ingestion pipeline to send data to the backend.
    """
    id: str = Field(..., description="Unique identifier for the chunk.")
    content: str = Field(..., description="The raw text content of the chunk.")
    embedding: List[float] = Field(..., description="Vector embedding of the chunk content.")
    metadata: ChunkMetadata = Field(..., description="Metadata associated with the chunk.")

class ChatQuery(BaseModel):
    """
    Query model for the /chat and /select-and-ask endpoints.
    """
    query: str = Field(..., description="The user's natural language query.")
    selected_text: Optional[str] = Field(None, description="Optional: text selected by the user for context.")
    session_id: Optional[str] = Field(None, description="Optional: ID of the current chat session.")

class ChatResponse(BaseModel):
    """
    Response model for the /chat and /select-and-ask endpoints.
    """
    answer: str = Field(..., description="The chatbot's generated answer.")
    evidence: List[Dict] = Field(..., description="List of retrieved evidence chunks (content, source).")

class HealthCheckResponse(BaseModel):
    """
    Response model for the /health endpoint.
    """
    status: str = Field(..., description="Status of the API.")