import os
import glob
import asyncio
import sys # Import sys
from typing import List, Dict, Optional
from datetime import datetime
from dotenv import load_dotenv

# Add project root to sys.path for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Load environment variables from .env file for local development
load_dotenv()

from rag_ingestion.scripts.parse_content import parse_markdown_to_chunks
from rag_backend.app.core.embedding_client import generate_embeddings_for_chunks
from rag_ingestion.scripts.ingest_to_qdrant import ingest_chunks_to_qdrant # Keep this for now
from rag_backend.app.core.database import AsyncSessionLocal # Import AsyncSessionLocal for session management
from rag_backend.app.models.db_models import IngestionRecord
from rag_backend.app.services.ingestion_service import IngestionService
from qdrant_client import QdrantClient # For checking Qdrant client directly

async def run_initial_ingestion(book_docs_path: str, qdrant_collection_name: str, session: AsyncSession):
    """
    Orchestrates the initial ingestion of all book chapters into Qdrant and records in Postgres.
    """
    ingestion_service = IngestionService(session)
    all_chunks_count = 0
    
    # Get all chapter files (e.g., chapter-01.md, chapter-02.md, etc.)
    chapter_files = glob.glob(os.path.join(book_docs_path, "chapter-*.md"))
    chapter_files = [f for f in chapter_files if "chapter-template.md" not in f and "bibliography.md" not in f]

    if not chapter_files:
        print(f"No chapter files found in {book_docs_path}. Skipping ingestion.")
        return

    for filepath in chapter_files:
        document_id = os.path.basename(filepath).replace('.md', '')
        print(f"Processing {filepath} for document_id: {document_id}...")
        
        try:
            # 1. Parse content into chunks
            chunks = parse_markdown_to_chunks(filepath)
            if not chunks:
                print(f"No content chunks found for {filepath}.")
                await ingestion_service.record_ingestion(document_id, filepath, 0, "failed", {"error": "No chunks found"})
                continue
            
            # 2. Generate embeddings for chunks
            chunks_with_embeddings = generate_embeddings_for_chunks(chunks)
            
            # 3. Ingest all chunks into Qdrant
            ingest_chunks_to_qdrant(chunks_with_embeddings, qdrant_collection_name)
            all_chunks_count += len(chunks_with_embeddings)
            
            # 4. Record ingestion in Postgres
            await ingestion_service.record_ingestion(document_id, filepath, len(chunks_with_embeddings), "completed")
            print(f"Successfully ingested {len(chunks_with_embeddings)} chunks from {filepath}.")

        except Exception as e:
            print(f"Error ingesting {filepath}: {e}")
            await ingestion_service.record_ingestion(document_id, filepath, 0, "failed", {"error": str(e)})

    print(f"\nInitial ingestion process finished. Total chunks ingested: {all_chunks_count}.")

async def main():
    """Main function to run the ingestion pipeline."""
    # Ensure Qdrant credentials are set in environment
    qdrant_url = os.environ.get("QDRANT_URL")
    qdrant_api_key = os.environ.get("QDRANT_API_KEY")
    qdrant_collection_name = os.environ.get("QDRANT_COLLECTION_NAME")

    # Ensure Gemini API key and base URL are set
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    gemini_base_url = os.environ.get("GEMINI_BASE_URL")

    # Ensure Database URL is set
    database_url = os.environ.get("DATABASE_URL")

    if not all([qdrant_url, qdrant_api_key, qdrant_collection_name, gemini_api_key, gemini_base_url, database_url]):
        print("Error: All required environment variables (QDRANT_*, GEMINI_*, DATABASE_URL) must be set.")
        return

    print("All environment variables are set. Proceeding with Qdrant client check...")
    
    # Verify Qdrant connection
    try:
        q_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        q_client.get_collections() # A simple call to check connection
        print("Successfully connected to Qdrant.")
    except Exception as e:
        print(f"Failed to connect to Qdrant: {e}")
        return

    print("Proceeding with Postgres database connection and ingestion...")
    # Get an async DB session for ingestion records
    async with AsyncSessionLocal() as session:
        await run_initial_ingestion("./docs", qdrant_collection_name, session)

if __name__ == "__main__":
    asyncio.run(main())