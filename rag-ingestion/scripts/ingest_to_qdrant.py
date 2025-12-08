import os
from typing import List, Dict
from qdrant_client import QdrantClient, models
from rag_backend.app.core.qdrant_client import get_qdrant_client # Import actual qdrant client

def ingest_chunks_to_qdrant(chunks: List[Dict], collection_name: str):
    """
    Ingests a list of chunks (with embeddings and metadata) into Qdrant.
    """
    client = get_qdrant_client() # Get configured client

    # Ensure collection exists or create it
    try:
        collection_info = client.get_collection(collection_name=collection_name)
        print(f"Collection '{collection_name}' already exists.")
    except Exception: # Collection not found, create it
        if not chunks:
            print("No chunks to ingest, cannot determine vector size for new collection.")
            return

        # Dynamically determine vector size from the first embedding
        vector_size = len(chunks[0]["embedding"])
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
        )
        print(f"Collection '{collection_name}' created with vector size {vector_size}.")
        
    points = []
    for chunk in chunks:
        # Ensure payload keys are string, as Qdrant sometimes has issues with non-string keys
        payload = {str(k): v for k, v in chunk["metadata"].items()}
        points.append(
            models.PointStruct(
                id=chunk["id"],
                vector=chunk["embedding"],
                payload=payload
            )
        )
    
    client.upsert(
        collection_name=collection_name,
        points=points,
        wait=True
    )
    print(f"Successfully ingested {len(chunks)} chunks into Qdrant collection '{collection_name}'.")

if __name__ == "__main__":
    # Example usage with dummy chunks (assuming they have embeddings)
    # Ensure QDRANT_URL and QDRANT_API_KEY are set in environment
    # os.environ["QDRANT_URL"] = "https://your-url.qdrant.io"
    # os.environ["QDRANT_API_KEY"] = "your-api-key"

    dummy_chunks_with_embeddings = [
        {
            "id": "doc1_chunk1",
            "content": "This is the first part of document 1.",
            "embedding": [0.1] * 768, # Dummy embedding, matching Gemini's
            "metadata": {"source_chapter": "chapter-01", "source_section": "1.1 Intro"}
        },
        {
            "id": "doc1_chunk2",
            "content": "This is the second part of document 1.",
            "embedding": [0.2] * 768, # Dummy embedding, matching Gemini's
            "metadata": {"source_chapter": "chapter-01", "source_section": "1.2 Content"}
        }
    ]
    
    # Placeholder for a collection name
    test_collection_name = "test_book_chunks"
    
    print(f"Attempting to ingest into collection: {test_collection_name}")
    try:
        ingest_chunks_to_qdrant(dummy_chunks_with_embeddings, test_collection_name)
    except Exception as e:
        print(f"Error during example ingestion: {e}")
