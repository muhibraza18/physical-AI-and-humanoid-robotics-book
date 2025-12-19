# Implementation Plan: Integrated RAG Chatbot

**Branch**: `003-integrate-frontend-chatbot` | **Date**: 2025-12-17 | **Spec**: [specs/003-integrate-frontend-chatbot/spec.md](specs/003-integrate-frontend-chatbot/spec.md)
**Input**: Feature specification from `/specs/003-integrate-frontend-chatbot/spec.md`

## Summary

The plan outlines the implementation of an Integrated RAG Chatbot for a Docusaurus-based book. This involves setting up a Python 3.12 FastAPI backend for content ingestion, embedding with Cohere, vector storage in Qdrant, retrieval, and LLM-based agent reasoning. The frontend will integrate a chatbot UI into Docusaurus. The core functionality is to answer user questions accurately from book content, prioritizing user-selected text, and clearly stating when information is not found.

## Technical Context

**Language/Version**: Python 3.12  
**Primary Dependencies**: FastAPI, Uvicorn, Qdrant-client, Cohere, Psycopg2 (or asyncpg), python-dotenv  
**Storage**: Qdrant Cloud (vector storage), Neon Serverless Postgres (metadata logging)  
**Testing**: NEEDS CLARIFICATION (specific testing framework for Python backend)  
**Target Platform**: Linux server (for FastAPI backend), Web browser (for Docusaurus frontend)
**Project Type**: Web application (Frontend + Backend)  
**Performance Goals**: NEEDS CLARIFICATION (specific latency targets for chat responses and retrieval)  
**Constraints**: Python 3.12 only, No TensorFlow/incompatible ML libs, Modular backend, Secrets as env vars, Qdrant Free Tier limits, Qdrant Cloud Free Tier limits.  
**Scale/Scope**: Single Docusaurus book, no authentication/user management, no multi-book RAG, no external web search, no model fine-tuning.
**Agent Architecture**: OpenAI Agents / ChatKit-style reasoning (abstract description of desired reasoning style)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

-   **Accuracy**: All answers must strictly reflect the content of the book.
    -   **Compliance**: Yes. Plan phases emphasize content ingestion, embedding, retrieval, and agent reasoning all based on book content. Agent behavior rules in the spec explicitly state "No hallucinations" and "No external knowledge beyond provided context".
-   **Context Awareness**: Use selected text from the user if provided; otherwise, retrieve relevant sections from the book’s Qdrant vector store.
    -   **Compliance**: Yes. Phase 4 explicitly defines agent logic to prioritize selected text or use retrieval.
-   **Spec-Driven Consistency**: Follow the Spec-Kit Plus structure for data embedding, retrieval, and agent responses.
    -   **Compliance**: Yes. The planning process itself follows Spec-Driven Development.
-   **Safety**: Do not hallucinate; if information is missing, respond with "Not found in book."
    -   **Compliance**: Yes. Phase 4's agent logic includes responding "Not found in book" if context is insufficient.
-   **Technical Compatibility**: All backend code must run on Python 3.12 and be free of TensorFlow dependencies.
    -   **Compliance**: Yes. Phase 0 explicitly initializes Python 3.12 environment and verifies no TensorFlow.
-   **API Standardization**: Use Cohere embeddings for vectorization, FastAPI for backend, and Qdrant Cloud Free Tier for storage.
    -   **Compliance**: Yes. Phases 0, 2, 3, 4 explicitly mention Cohere, FastAPI, and Qdrant Cloud Free Tier.

**GATE**: All constitution checks pass.

## Project Structure

### Documentation (this feature)

```text
specs/003-integrate-frontend-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── ingestion/             # Phase 1, 2 logic
│   │   ├── parser.py
│   │   └── chunker.py
│   ├── embedding/             # Phase 2 logic
│   │   ├── client.py
│   │   └── models.py
│   ├── storage/               # Phase 2 logic
│   │   ├── qdrant_client.py
│   │   └── models.py
│   ├── retrieval/             # Phase 3 logic
│   │   ├── searcher.py
│   │   └── models.py
│   ├── agent/                 # Phase 4 logic
│   │   ├── orchestrator.py
│   │   └── prompts.py
│   ├── api/                   # Phase 3, 4 endpoints
│   │   ├── __init__.py
│   │   ├── embed_endpoints.py # For POST /embed
│   │   ├── search_endpoints.py # For POST /search
│   │   └── chat_endpoints.py  # For POST /chat
│   ├── core/                  # Common utilities, config
│   │   ├── config.py
│   │   ├── database.py        # Phase 5 logic
│   │   └── logging.py
│   └── main.py                # FastAPI app entry point
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
├── .env.example
├── pyproject.toml
└── requirements.txt

frontend/
├── src/
│   ├── components/            # Chatbot UI components
│   │   ├── ChatWindow.js
│   │   ├── FloatingButton.js
│   │   └── index.js
│   ├── pages/                 # Docusaurus pages, if needed
│   └── services/              # API interaction logic
│       └── ChatService.js
├── tests/                     # Frontend tests
└── package.json
```

**Structure Decision**: A clear separation of concerns between backend and frontend is adopted. The backend is structured into logical components for ingestion, embedding, storage, retrieval, and agent reasoning, each with its dedicated `src` sub-directory. API endpoints are grouped under `api/`. The frontend integrates directly into the existing Docusaurus structure, with specific components and services for the chatbot.

## Complexity Tracking

## Phase 0: Outline & Research

### Unknowns identified from Technical Context:

1.  **Testing framework for Python backend**: The plan specifies Python 3.12 and FastAPI, but no explicit testing framework.
2.  **Specific latency targets**: "Performance Goals" is marked "NEEDS CLARIFICATION".

### Research Tasks:

-   Research: "Best Python testing framework for FastAPI projects"
-   Research: "Typical latency targets for RAG chatbots"

## Phase 1: Design & Contracts

### Prerequisites: `research.md` complete

### Extract entities from feature spec → `data-model.md`:

-   **Book Content Chunk**:
    -   `text`: string (actual content of the chunk)
    -   `embedding`: array of floats (vector representation)
    -   `metadata`: object
        -   `file_path`: string (source Markdown/MDX file)
        -   `chapter`: string (chapter title)
        -   `section`: string (section heading)
        -   `page_number`: integer (optional, if extractable)
        -   `chapter_id`: string (optional, unique identifier for chapter)
-   **Embedding**:
    -   `vector`: array of floats (numerical representation of text)
-   **User Query**:
    -   `query_text`: string (the user's question)
    -   `selected_text`: string (optional, text selected by user)
-   **Chat Response**:
    -   `answer`: string (generated response text)
    -   `source_references`: array of objects (metadata from chunks used for answer)
        -   `file_path`: string
        -   `chapter`: string
        -   `section`: string
        -   `page_number`: integer (optional)
        -   `chapter_id`: string (optional)
-   **Chat History/Log Entry (for Neon Postgres)**:
    -   `session_id`: string (unique ID for a chat session)
    -   `query_id`: string (unique ID for each query)
    -   `query_text`: string
    -   `timestamp`: datetime
    -   `retrieved_references`: array of objects (metadata from chunks retrieved)
    -   `generated_response_text`: string
    -   `selected_text`: string (optional)
    -   `response_latency_ms`: integer (optional)
    -   `llm_model_used`: string (optional)

### Generate API contracts from functional requirements:

#### **contracts/api.yaml**

```yaml
openapi: 3.0.0
info:
  title: RAG Chatbot API
  version: 1.0.0
paths:
  /embed:
    post:
      summary: Embed and store book content chunks
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - content
                - metadata
              properties:
                content:
                  type: string
                  description: The text content to embed.
                metadata:
                  type: object
                  description: Metadata associated with the content chunk.
                  properties:
                    file_path:
                      type: string
                    chapter:
                      type: string
                    section:
                      type: string
                    page_number:
                      type: integer
                      nullable: true
                    chapter_id:
                      type: string
                      nullable: true
      responses:
        '200':
          description: Content embedded and stored successfully.
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: success
                  message:
                    type: string
                    example: Content embedded and stored
        '400':
          description: Invalid input provided.
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: string
        '500':
          description: Internal server error.
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: string

  /search:
    post:
      summary: Retrieve relevant book content chunks based on a query
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - query
              properties:
                query:
                  type: string
                  description: The user's search query.
                top_k:
                  type: integer
                  description: Number of top relevant chunks to retrieve.
                  default: 5
      responses:
        '200':
          description: Retrieved content chunks.
          content:
            application/json:
              schema:
                type: object
                properties:
                  results:
                    type: array
                    items:
                      type: object
                      properties:
                        text:
                          type: string
                        metadata:
                          type: object
                          properties:
                            file_path:
                              type: string
                            chapter:
                              type: string
                            section:
                              type: string
                            page_number:
                              type: integer
                              nullable: true
                            chapter_id:
                              type: string
                              nullable: true
        '400':
          description: Invalid input provided.
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: string
        '500':
          description: Internal server error.
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: string

  /chat:
    post:
      summary: Get a RAG-generated response to a user query
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - query
              properties:
                query:
                  type: string
                  description: The user's question.
                selected_text:
                  type: string
                  nullable: true
                  description: Optional text selected by the user for contextual answering.
      responses:
        '200':
          description: RAG-generated answer and source references.
          content:
            application/json:
              schema:
                type: object
                properties:
                  answer:
                    type: string
                  source_references:
                    type: array
                    items:
                      type: object
                      properties:
                        file_path:
                          type: string
                        chapter:
                          type: string
                        section:
                          type: string
                        page_number:
                          type: integer
                          nullable: true
                        chapter_id:
                          type: string
                          nullable: true
        '400':
          description: Invalid input provided.
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: string
        '500':
          description: Internal server error.
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: string
```