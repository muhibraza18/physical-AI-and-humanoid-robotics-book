# Data Model for RAG Text Chunks

## Overview
This document defines the data model for text chunks, their metadata, and embeddings stored in Qdrant for the RAG chatbot system.

## Chunk Structure
- **`id`**: Unique identifier for the chunk.
- **`content`**: The raw text content of the chunk.
- **`embedding`**: Vector representation of the chunk.
- **`metadata`**: Additional information about the chunk.
  - **`source_chapter`**: (e.g., "chapter-01")
  - **`source_section`**: (e.g., "1.2.1 Defining Physical AI")
  - **`page_number`**: (if applicable)
  - **`original_slug`**: (e.g., "/docs/chapter-01")
  - **`chunk_hash`**: Hash of the content for change detection.

## Qdrant Collection Configuration
- **Collection Name**: [To be decided]
- **Vector Size**: [Embedding model dimensionality]
- **Distance Metric**: [e.g., Cosine]

## Relationships
- Text chunks are derived from book chapters.
- Each chunk is associated with its original source.

## Validation Rules
- `content` must not be empty.
- `embedding` must be a valid vector of expected dimensionality.
- `source_chapter` must map to an existing chapter.
