from typing import List, Dict
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

from app.core.embedding_client import generate_embedding # Corrected import
from app.core.qdrant_client import get_qdrant_client

def retrieve_chunks(query: str, collection_name: str, top_k: int = 5) -> List[Dict]:
    """
    Retrieves relevant chunks from Qdrant based on a user query using semantic search.
    Returns an empty list if no relevant chunks are found.
    """
    client = get_qdrant_client()
    
    # Generate embedding for the query
    query_embedding = generate_embedding(query) # Using the placeholder embedding function

    search_result = client.search_points(
        collection_name=collection_name,
        vector=query_embedding,
        limit=top_k,
        # Optional: add filters if metadata needs to be considered
        # query_filter=Filter(
        #     must=[
        #         FieldCondition(
        #             key="source_chapter",
        #             match=MatchValue(value="chapter-01")
        #         )
        #     ]
        # )
    )

    retrieved_chunks = []
    for hit in search_result:
        retrieved_chunks.append({
            "content": hit.payload["content"], # Assuming 'content' is stored in payload
            "source": hit.payload.get("source_chapter", "unknown"),
            "score": hit.score
        })
    return retrieved_chunks

if __name__ == "__main__":
    # Example usage
    test_query = "What is Physical AI?"
    test_collection = "physical-ai-robotics-book-chunks" # Example collection name
    
    print(f"Retrieving chunks for query: '{test_query}' from collection '{test_collection}'")
    # retrieved = retrieve_chunks(test_query, test_collection) # This would need a running Qdrant and embeddings
    print("Retrieval logic executed (Qdrant connection/search might need actual credentials/host).")
    # for chunk in retrieved:
    #     print(f"  - Score: {chunk['score']:.2f}, Source: {chunk['source']}, Content: {chunk['content'][:100]}...")