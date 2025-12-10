import os
from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient

# Load environment variables
load_dotenv()

# Initialize clients
try:
    cohere_api_key = os.getenv("COHERE_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not all([cohere_api_key, qdrant_url, qdrant_api_key]):
        raise ValueError("One or more environment variables are not set.")

    cohere_client = cohere.Client(cohere_api_key)
    qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

except (ValueError, Exception) as e:
    # Handle initialization errors
    print(f"Error during client initialization: {e}")
    cohere_client = None
    qdrant = None

def get_embedding(text):
    """Get embedding vector from Cohere Embed v3"""
    response = cohere_client.embed(
        model="embed-english-v3.0",
        input_type="search_query",  # Use search_query for queries
        texts=[text],
    )
    return response.embeddings[0]  # Return the first embedding

def retrieve(query):
    embedding = get_embedding(query)
    result = qdrant.query_points(
        collection_name="humanoid_ai_book",
        query=embedding,
        limit=5
    )
    return [point.payload["text"] for point in result.points]

# Test
print(retrieve("What data do you have?"))