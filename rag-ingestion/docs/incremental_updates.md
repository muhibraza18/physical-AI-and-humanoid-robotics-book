# Design for Incremental Embedding Updates

## Overview
This document outlines the design for implementing incremental updates to the Qdrant vector database. The goal is to efficiently re-embed and update only the book content that has changed, rather than re-ingesting the entire book every time.

## Strategy
1.  **Content Hashing**: For each book chapter/chunk, calculate a hash of its content.
2.  **Metadata Storage**: Store this content hash as part of the chunk's metadata in Qdrant.
3.  **Change Detection**: When an ingestion run starts, compare the current content hash of each chapter/chunk with the hash stored in Qdrant.
4.  **Conditional Re-embedding**: Only re-embed and re-ingest chunks whose content hashes have changed.
5.  **Deletion/Addition**: Identify deleted chapters/chunks (no matching current content) and remove them from Qdrant. Identify new chapters/chunks and ingest them.

## Implementation Details
-   **Hash Function**: Use a fast and reliable hashing algorithm (e.g., MD5 or SHA-256) for content hashing.
-   **API for Updates**: The `/ingest` API endpoint in FastAPI should support accepting a list of updated/deleted chunks.
-   **Workflow**:
    *   Scan all book content files.
    *   For each file, parse into chunks and calculate current hashes.
    *   Query Qdrant for existing chunks and their hashes for the given chapter.
    *   Compare and determine `to_add`, `to_update`, `to_delete` lists.
    *   Execute Qdrant upsert and delete operations.

## Risks & Considerations
-   **Performance**: Hashing all content might be slow for very large books. Optimize file traversal.
-   **Consistency**: Ensure atomicity of updates to avoid inconsistent states in Qdrant.
-   **Error Handling**: Robust error handling for Qdrant API calls during updates.
