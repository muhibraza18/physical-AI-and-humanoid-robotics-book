import os
from typing import List, Dict
from openai import OpenAI

# Initialize OpenAI client to work with Gemini API via OpenAI-compatible endpoint
gemini_api_key = os.environ.get("GEMINI_API_KEY")
gemini_base_url = os.environ.get("GEMINI_BASE_URL")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable must be set.")
if not gemini_base_url:
    raise ValueError("GEMINI_BASE_URL environment variable must be set.")

client = OpenAI(api_key=gemini_api_key, base_url=gemini_base_url)

def generate_embedding(text: str) -> List[float]:
    """
    Generates an embedding for a given text using the configured Gemini model.
    """
    try:
        response = client.embeddings.create(
            input=text, 
            model="models/embedding-001" # Gemini's embedding model
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        # Fallback for now, in production consider raising or more robust error handling
        return [0.0] * 768 # Common embedding dimension for some models, adjust as needed

def generate_embeddings_for_chunks(chunks: List[Dict]) -> List[Dict]:
    """
    Generates embeddings for a list of text chunks.
    """
    for chunk in chunks:
        chunk["embedding"] = generate_embedding(chunk["content"])
    return chunks

if __name__ == "__main__":
    # Example usage with dummy chunks
    # Ensure GEMINI_API_KEY and GEMINI_BASE_URL are set in environment
    # os.environ["GEMINI_API_KEY"] = "YOUR_GEMINI_API_KEY"
    # os.environ["GEMINI_BASE_URL"] = "https://generativelanguage.googleapis.com/v1beta/openai/"

    dummy_chunks = [
        {"id": "c1", "content": "This is a test sentence."},
        {"id": "c2", "content": "Another sentence for embedding."}
    ]
    chunks_with_embeddings = generate_embeddings_for_chunks(dummy_chunks)
    for chunk in chunks_with_embeddings:
        print(f"ID: {chunk['id']}, Embedding length: {len(chunk['embedding'])}")
        print(f"Embedding snippet: {chunk['embedding'][:5]}...") # Print first 5 elements