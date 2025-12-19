# Feature Specification: Integrated RAG Chatbot

**Feature Branch**: `003-integrate-frontend-chatbot`  
**Created**: 2025-12-17  
**Status**: Draft  
**Input**: User description: "Integrated RAG Chatbot for AI & Humanoid Robotics BookTarget audience:- Readers of the Docusaurus-based book on Physical AI and Humanoid Robotics- Evaluators assessing Spec-Driven RAG system implementationPrimary goal:- Build and embed a Retrieval-Augmented Generation (RAG) chatbot within a published Docusaurus book- Enable accurate question answering strictly from book content- Support answering questions based only on user-selected textTechnology stack:- Backend: FastAPI (Python 3.12)- Embeddings: Cohere API- Vector database: Qdrant Cloud (Free Tier)- Relational database: Neon Serverless Postgres- Agent architecture: OpenAI Agents / ChatKit-style reasoning- Frontend: Docusaurus-integrated chatbot UIRuntime configuration (environment variables — values provided at runtime):- QDRANT_URL = "<https://a6ae135d-580b-4a28-9803-0adb84ab9d55.us-east4-0.gcp.cloud.qdrant.io>"- QDRANT_API_KEY = "<eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.Ve7ohi2ESSOOUBF6QFNv-YiZKQeOfQ5d_B5b3PG7ptM>"- QDRANT_CLUSTER_ID = "<a6ae135d-580b-4a28-9803-0adb84ab9d55>"- DATABASE_URL = "<psql 'postgresql://neondb_owner:npg_NWBpJf5Umso3@ep-icy-dream-adlmb2or-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'>"- COHERE_API_KEY = "<QqHPH4IvJOEym6X7jQ2gCtOBwpbAs28QzArlzcU0>"- GEMINI_API_KEY = "<AIzaSyBhF75iGl7KaTk5yYxktUnv8GYUx33u4y8>"Core functional requirements:- Parse and chunk Markdown / MDX book content- Generate embeddings using Cohere- Store vectors and metadata in Qdrant- Retrieve top-k relevant chunks for user queries- Generate answers strictly from retrieved context- If user provides selected text, bypass retrieval and answer only from that text- If information is missing, respond: "Not found in book."API requirements:- POST /embed- POST /search- POST /chatAgent behavior rules:- No hallucinations- No external knowledge beyond provided context- Concise, technically accurate answers- Reference chapter or section when applicableConstraints:- Python 3.12 only- No TensorFlow or incompatible ML libraries- Modular backend design: - ingestion - embedding - storage - retrieval - reasoning- Secrets must never appear in code, specs, or repositories- Must work within Qdrant Cloud Free Tier limitsSuccess criteria:- Chatbot answers book-related questions accurately- Selected-text queries always take precedence- Backend runs without dependency conflicts- Frontend successfully communicates with FastAPI- Clear RAG flow demonstrated during evaluationNot building:- Model fine-tuning- External web search- Multi-book RAG system- Authentication or user management"

## User Scenarios & Testing

### User Story 1 - Ask a Question about Book Content (Priority: P1)

As a reader of the book, I want to ask questions about the book's content through a chatbot and receive accurate answers, so that I can quickly find information without manually searching.

**Why this priority**: This is the primary goal of the RAG chatbot and provides immediate value to the user by enabling quick access to information within the book.

**Independent Test**: Can be fully tested by providing diverse questions related to the book's content and verifying the accuracy and relevance of the chatbot's responses.

**Acceptance Scenarios**:

1.  **Given** the chatbot UI is active, **When** a user types a question about a topic covered in the book, **Then** the chatbot responds with a concise and accurate answer derived solely from the book's content.
2.  **Given** the chatbot UI is active, **When** a user types a question about a topic covered in the book, **Then** the chatbot's response includes references to relevant chapters or sections if available.

### User Story 2 - Ask a Question with User-Selected Text (Priority: P1)

As a reader of the book, I want to select specific text from the book and ask a question that the chatbot answers using only the selected text, so that I can get highly contextual answers without interference from other parts of the book.

**Why this priority**: This provides a powerful, precise way for users to interact with specific snippets of information, enhancing the utility and accuracy for detailed queries.

**Independent Test**: Can be fully tested by selecting specific text segments and asking questions that can only be answered by the selected text, verifying that the chatbot ignores other book content.

**Acceptance Scenarios**:

1.  **Given** a user has selected a portion of text in the book, **When** the user asks a question via the chatbot, **Then** the chatbot's answer is based exclusively on the selected text.
2.  **Given** a user has selected text from the book, **When** the user asks a question whose answer is not present in the selected text, **Then** the chatbot responds exactly with "This information is not found in the book."

### User Story 3 - Ask a Question Not Covered by the Book (Priority: P2)

As a reader, I want the chatbot to clearly indicate when it cannot find an answer within the book's content, so that I am not misled by fabricated information.

**Why this priority**: Prevents hallucination and builds user trust by clearly setting boundaries on the chatbot's knowledge.

**Independent Test**: Can be fully tested by asking questions that are demonstrably outside the scope of the book's content and verifying the chatbot's refusal message.

**Acceptance Scenarios**:

1.  **Given** the chatbot UI is active, **When** a user asks a question that is not covered by the book's content (and no text is selected), **Then** the chatbot responds exactly with "This information is not found in the book."
2.  **Given** the chatbot UI is active, **When** a user asks a question about general knowledge outside the book's scope, **Then** the chatbot responds exactly with "This information is not found in the book."

### Edge Cases

- What happens when a user provides selected text that is too short or too long for effective processing?
- How does the system handle very ambiguous or malformed user queries?
- What is the behavior if the embedding or LLM API calls fail or timeout?
- How does the system ensure privacy and security, especially with user queries and API keys?

## Requirements

### Functional Requirements

- **FR-001**: System MUST parse and chunk Markdown/MDX book content.
- **FR-002**: System MUST generate embeddings for book content using Cohere API.
- **FR-003**: System MUST store generated vectors and associated metadata (file, section, heading) in Qdrant Cloud (Free Tier).
- **FR-004**: System MUST retrieve top-k relevant chunks from Qdrant for user queries when no specific text is selected.
- **FR-005**: System MUST generate answers strictly from the provided context (retrieved chunks or selected text).
- **FR-006**: If a user provides selected text, the system MUST prioritize this text as the sole context for answering the question, bypassing Qdrant retrieval.
- **FR-007**: If the provided context (retrieved or selected) is insufficient to answer a question, the system MUST respond exactly with "This information is not found in the book."
- **FR-008**: Backend system MUST expose a POST `/embed` API endpoint for content ingestion (triggering parsing, chunking, embedding, and storage).
- **FR-009**: Backend system MUST expose a POST `/search` API endpoint for direct vector retrieval (e.g., for debugging or advanced use cases).
- **FR-010**: Backend system MUST expose a POST `/chat` API endpoint for processing user queries and returning RAG-generated responses.
- **FR-011**: The agent MUST not hallucinate or incorporate external knowledge beyond the explicitly provided context.
- **FR-012**: The agent MUST provide concise, technically accurate answers.
- **FR-013**: The agent SHOULD reference the chapter or section from which information was retrieved when generating answers.

### Key Entities

-   **Book Content Chunk**: A segmented piece of the book content, typically 500-800 tokens, accompanied by metadata such as file path, chapter, and section headings.
-   **Embedding**: A numerical vector representation of a Book Content Chunk, generated by the Cohere API, used for semantic similarity search.
-   **User Query**: The natural language question submitted by a user, potentially including a specific text selection from the book as additional context.
-   **Chat Response**: The chatbot's generated answer to a User Query, derived from either retrieved Book Content Chunks or User-Selected Text.

## Success Criteria

### Measurable Outcomes

-   **SC-001**: The chatbot will answer 95% of book-related factual questions accurately during acceptance testing.
-   **SC-002**: For 100% of selected-text queries, the chatbot will exclusively use the provided text as context, as verified by response analysis.
-   **SC-003**: The backend service will successfully start and run on a Python 3.12 environment without dependency conflicts.
-   **SC-004**: The frontend Docusaurus chatbot UI will successfully communicate with all required FastAPI endpoints (e.g., `/chat`, `/embed`) for 100% of user interactions.
-   **SC-005**: During system evaluation, the end-to-end RAG flow (content chunking, embedding, retrieval, and response generation) will be clearly demonstrable.

## Constraints

-   Python 3.12 only.
-   No TensorFlow, PyTorch, or any other deep learning libraries that are incompatible with the specified Python version or environment.
-   Modular backend design: Ingestion, embedding, storage, retrieval, and reasoning components must be clearly separated.
-   Secrets (API keys, URLs) MUST never appear in code, specifications, or version control repositories. They must be managed via environment variables.
-   The system MUST operate within the limits of Qdrant Cloud Free Tier.

## Not Building

-   Model fine-tuning (e.g., fine-tuning LLMs).
-   External web search capabilities (chatbot will not access information outside the book).
-   Multi-book RAG system (limited to a single Docusaurus book).
-   User authentication or user management features.
-   Complex conversational state management beyond a single query-response cycle.