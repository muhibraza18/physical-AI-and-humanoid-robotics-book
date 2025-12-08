import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict

from app.models.rag_models import IngestChunkPayload
from app.core.database import get_db
from app.core.qdrant_client import get_qdrant_client
from qdrant_client.http.models import PointStruct, VectorParams, Distance

router = APIRouter()

@router.post("/chunks", status_code=202)
async def ingest_chunks_endpoint(
    payloads: List[IngestChunkPayload], 
    db: AsyncSession = Depends(get_db) # Placeholder for db dependency if needed in ingestion service
):
    """
    Receives a list of IngestChunkPayloads and stores them in Qdrant.
    """
    qdrant_client = get_qdrant_client()
    collection_name = os.environ.get("QDRANT_COLLECTION_NAME", "default_book_rag_collection")

    if not collection_name:
        raise HTTPException(status_code=500, detail="QDRANT_COLLECTION_NAME not set.")

    # Ensure collection exists or create it
    try:
        # Check if collection exists
        if not qdrant_client.collection_exists(collection_name=collection_name):
            # Create collection if it doesn't exist
            qdrant_client.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=len(payloads[0].embedding), distance=Distance.COSINE), # Assuming all embeddings have same size
            )
            print(f"Qdrant collection '{collection_name}' created.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ensure Qdrant collection: {e}")

    points = []
    for payload in payloads:
        points.append(
            PointStruct(
                id=payload.id,
                vector=payload.embedding,
                payload=payload.metadata.dict() # Convert Pydantic model to dict for payload
            )
        )
    
    try:
        qdrant_client.upsert(
            collection_name=collection_name,
            points=points,
            wait=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest chunks to Qdrant: {e}")

    return {"message": f"Successfully ingested {len(payloads)} chunks to Qdrant collection '{collection_name}'."}