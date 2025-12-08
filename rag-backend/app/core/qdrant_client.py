import os
from qdrant_client import QdrantClient

def get_qdrant_client() -> QdrantClient:
    """
    Initializes and returns a Qdrant client using credentials from environment variables.
    Environment variables expected:
    - QDRANT_URL: The URL of the Qdrant Cloud instance.
    - QDRANT_API_KEY: The API key for authenticating with Qdrant.
    """
    qdrant_url = os.environ.get("QDRANT_URL")
    qdrant_api_key = os.environ.get("QDRANT_API_KEY")

    if not qdrant_url or not qdrant_api_key:
        raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables must be set.")

    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        prefer_grpc=True  # Optional: use GRPC for faster communication
    )
    return client

# Example usage (for testing purposes)
if __name__ == "__main__":
    # For local testing, set environment variables like this:
    # os.environ["QDRANT_URL"] = "https://your-url.qdrant.io"
    # os.environ["QDRANT_API_KEY"] = "your-api-key"

    try:
        client = get_qdrant_client()
        print("Qdrant client initialized using environment variables.")
        # You can add a test call here if Qdrant is expected to be reachable during local execution
        # client.get_collections() 
        # print("Successfully connected to Qdrant and fetched collections.")
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")