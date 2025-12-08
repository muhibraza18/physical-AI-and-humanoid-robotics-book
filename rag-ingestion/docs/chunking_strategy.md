# Content Chunking Strategy for RAG

## Overview
This document outlines the initial strategy for chunking the technical book content (Markdown/MDX files) into manageable units for embedding and retrieval by the RAG chatbot.

## Goals
- Preserve semantic coherence within chunks.
- Optimize for retrieval accuracy and LLM context window limits.
- Facilitate precise citation of retrieved evidence.

## Proposed Strategy
1.  **Hierarchical Chunking**: Prioritize natural breaks in the document structure (headings, paragraphs, lists).
    *   H2 sections will be primary chunking units.
    *   Subsections (H3) or paragraphs within H2 will form smaller chunks if needed.
2.  **Fixed-Size with Overlap**: If hierarchical breaks are too large, fall back to fixed-size chunks (e.g., 500 tokens) with a configurable overlap (e.g., 50 tokens) to maintain context.
3.  **Code Block Handling**: Code blocks will be treated as separate chunks, with their own metadata (e.g., `type: code`, `language: python`).
4.  **Metadata Preservation**: Ensure each chunk retains metadata such as `source_chapter`, `source_section`, `page_number` (if applicable), and `original_slug`.

## Tools/Libraries
- Markdown parsing library (e.g., `markdown-it`, `mistune` in Python).
- Text splitting utility (e.g., from `langchain` or custom implementation).

## Open Questions/Further Research
- Optimal token count for chunks based on embedding model.
- Impact of different overlap sizes on retrieval performance.
- Strategy for handling diagrams and images (e.g., OCR, image captions as text).
