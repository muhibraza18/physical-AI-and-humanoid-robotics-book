# Data Flow: Select-and-Ask Interaction

## Overview
This document describes the data flow for the "select-and-ask" feature of the RAG chatbot, detailing the client-side interaction, backend processing, retrieval from Qdrant, and LLM reasoning.

## User Interaction
1.  **User selects text**: On a Docusaurus page, the user highlights a text snippet.
2.  **User triggers "Ask about selected text"**: A UI element appears (e.g., context menu, button) allowing the user to initiate a query based on the selected text.
3.  **User inputs question**: The user provides a natural language question related to the selected text.

## Client-Side Data Flow
- Frontend captures selected text and user's question.
- Frontend sends a POST request to `/select-and-ask` endpoint on FastAPI backend.
- Request body includes `selected_text` and `query`.

## Backend Processing (FastAPI)
1.  Receives `selected_text` and `query`.
2.  Optionally, pre-processes `selected_text` and `query` (e.g., cleaning, rephrasing).
3.  Generates an embedding for the `selected_text` (or uses it directly as context).
4.  Performs a Qdrant retrieval using the `query` and potentially biasing towards chunks semantically related to `selected_text`.
5.  Passes retrieved chunks and `query` to the LLM (OpenAI Agents / ChatKit SDKs).
6.  LLM generates a document-grounded answer.
7.  Extracts evidence (retrieved text snippets) used by the LLM.
8.  Returns `answer` and `evidence` to the client.

## Retrieval from Qdrant
- Query embedding generated from user's question.
- Semantic search against book content embeddings in Qdrant.
- Filter results based on metadata (e.g., `source_chapter` if the selected text provides strong context).

## LLM Reasoning
- LLM receives question and retrieved text.
- Generates a concise, factual answer, restricted to the provided context.
- Identifies and formats citations/evidence from the retrieved text.
- Handles "insufficient data" if retrieval yields no relevant results.

## Frontend Display
- Displays chatbot's answer.
- Presents retrieved evidence, potentially with links back to the source chapter/section.

## Risks & Considerations
- Latency of multiple API calls (client -> FastAPI -> OpenAI -> Qdrant -> OpenAI -> FastAPI -> client).
- Security of data transmission.
- Context window limitations of the LLM.
