# Tasks: Integrated RAG Chatbot

**Input**: Design documents from `/specs/003-integrate-frontend-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The implementation plan and research findings indicate the use of `pytest` with `httpx` and `pytest-mock`. Therefore, test tasks are included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

-   **[P]**: Can run in parallel (different files, no dependencies)
-   **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
-   Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, basic structure, and environment setup.

- [x] T001 Create backend directory `backend/` and frontend directory `frontend/`
- [x] T002 Initialize Python 3.12 environment in `backend/` using `uv` and create `backend/requirements.txt`
- [x] T003 [P] Install core backend dependencies: `fastapi`, `uvicorn`, `qdrant-client`, `cohere`, `psycopg2-binary`, `python-dotenv` in `backend/requirements.txt`
- [x] T004 Configure environment variable loading mechanism in `backend/src/core/config.py`
- [x] T005 Create base FastAPI application instance in `backend/src/main.py`
- [x] T006 [P] Initialize frontend project structure (assumed to be integrated with root Docusaurus `package.json`)
- [x] T007 [P] Create `.env.example` in `backend/` with all required environment variables

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure and common clients that MUST be complete before ANY user story can be implemented.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 [P] Implement Qdrant client initialization and basic collection management in `backend/src/storage/qdrant_client.py`
- [x] T009 [P] Implement Cohere client initialization for embeddings in `backend/src/embedding/client.py`
- [x] T010 Configure structured logging for the backend application in `backend/src/core/logging.py`
- [x] T011 Setup `pytest` as the testing framework in `backend/` with initial configuration for unit/integration/contract tests.
- [x] T012 Create `backend/src/ingestion/models.py` for content chunk and metadata models.
- [x] T013 Create `backend/src/embedding/models.py` for embedding models.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Ask a Question about Book Content (Priority: P1) 🎯 MVP

**Goal**: Enable the chatbot to answer questions by retrieving relevant information from the book content stored in Qdrant. This phase covers content ingestion and basic retrieval.

**Independent Test**: Can be fully tested by ingesting a sample of book content, then sending queries to the `/search` endpoint to verify relevant chunks are returned, and finally to the `/chat` endpoint to ensure basic question answering from context works.

### Tests for User Story 1

- [x] T014 [P] [US1] Unit test for Markdown/MDX parsing in `backend/tests/unit/test_ingestion_parser.py`
- [x] T015 [P] [US1] Unit test for deterministic chunking in `backend/tests/unit/test_ingestion_chunker.py`
- [x] T016 [P] [US1] Unit test for Cohere embedding client in `backend/tests/unit/test_embedding_client.py`
- [x] T017 [P] [US1] Unit test for Qdrant storage operations in `backend/tests/unit/test_storage_qdrant.py`
- [x] T018 [P] [US1] Contract test for POST `/embed` API endpoint in `backend/tests/contract/test_embed_api.py`
- [x] T019 [P] [US1] Contract test for POST `/search` API endpoint in `backend/tests/contract/test_search_api.py`
- [x] T020 [US1] Integration test for content ingestion pipeline (parse->chunk->embed->store) in `backend/tests/integration/test_ingestion_pipeline.py`

### Implementation for User Story 1

- [x] T021 [P] [US1] Implement Markdown/MDX parsing logic in `backend/src/ingestion/parser.py` (FR-001)
- [x] T022 [P] [US1] Implement deterministic chunking logic (500-800 tokens) in `backend/src/ingestion/chunker.py` (FR-001)
- [x] T023 [US1] Implement `/embed` endpoint logic in `backend/src/api/embed_endpoints.py` (FR-008)
- [x] T024 [US1] Implement `/search` endpoint logic in `backend/src/api/search_endpoints.py` (FR-009)
- [x] T025 [P] [US1] Implement retrieval service (top-k from Qdrant) in `backend/src/retrieval/searcher.py` (FR-004)
- [x] T026 [US1] Integrate `parser`, `chunker`, `embedding client`, `Qdrant client` into `/embed` endpoint flow (FR-002, FR-003)
- [x] T027 [US1] Integrate `embedding client` and `retrieval service` into `/search` endpoint flow (FR-004)

**Checkpoint**: At this point, content can be ingested, and basic search (retrieval) should be functional and testable independently.

---

## Phase 4: User Story 2 - Ask a Question with User-Selected Text (Priority: P1)

**Goal**: Implement the core RAG agent logic, including handling user-selected text and general question answering from retrieved content.

**Independent Test**: Can be fully tested by sending queries to the `/chat` endpoint, both with and without selected text, and verifying that answers are correctly generated based on the provided context, without hallucination.

### Tests for User Story 2

- [x] T028 [P] [US2] Unit test for agent reasoning logic (context handling, prompt construction) in `backend/tests/unit/test_agent_orchestrator.py`
- [x] T029 [P] [US2] Contract test for POST `/chat` API endpoint (both selected text and no selected text scenarios) in `backend/tests/contract/test_chat_api.py`
- [x] T030 [US2] Integration test for RAG chat flow (query->retrieve->generate) in `backend/tests/integration/test_rag_chat_flow.py`

### Implementation for User Story 2

- [x] T031 [P] [US2] Implement agent orchestrator with prompt construction in `backend/src/agent/orchestrator.py` (FR-005, FR-011, FR-012)
- [x] T032 [P] [US2] Define system prompts for agent in `backend/src/agent/prompts.py` (FR-005, FR-011)
- [x] T033 [US2] Implement `/chat` endpoint logic in `backend/src/api/chat_endpoints.py` (FR-010)
- [x] T034 [US2] Integrate agent orchestrator and retrieval service into `/chat` endpoint (FR-005)
- [x] T035 [US2] Implement logic to prioritize `selected_text` over Qdrant retrieval within the agent orchestrator/`/chat` endpoint (FR-006)
- [x] T036 [US2] Add logic to reference chapter/section from source_references in generated answers (FR-013)

**Checkpoint**: At this point, the core RAG chatbot should be functional and testable, handling both general questions and selected-text queries.

---

## Phase 5: User Story 3 - Ask a Question Not Covered by the Book (Priority: P2)

**Goal**: Ensure the chatbot gracefully handles queries for which there is insufficient information in the provided context, preventing hallucination.

**Independent Test**: Can be fully tested by sending queries known to be outside the book's scope to the `/chat` endpoint and verifying the "not found" response.

### Tests for User Story 3

- [x] T037 [P] [US3] Unit test for agent's "not found" response logic in `backend/tests/unit/test_agent_orchestrator.py` (Covered by `test_generate_response_insufficient_context`)
- [x] T038 [US3] Integration test for "not found" scenarios in `backend/tests/integration/test_rag_chat_flow.py`

### Implementation for User Story 3

- [x] T039 [US3] Implement agent logic to respond "This information is not found in the book." when context is insufficient (FR-007)

**Checkpoint**: The RAG chatbot now handles out-of-scope questions as per the specification.

---

## Phase 6: Neon Postgres Integration (Optional Metadata Logging)

**Purpose**: Store chat interactions and references for analytics and auditing.

**Independent Test**: Can be fully tested by sending chat queries and verifying that corresponding log entries are created in the Neon Postgres database without impacting chat response latency.

### Tests for Neon Postgres Integration

- [x] T040 [P] Unit test for Postgres database client in `backend/tests/unit/test_core_database.py`
- [x] T041 [US_N/A] Integration test for chat history logging in `backend/tests/integration/test_chat_history_logging.py`

### Implementation for Neon Postgres Integration

- [x] T042 Implement Postgres database client and connection in `backend/src/core/database.py`
- [x] T043 Define database models for chat history in `backend/src/core/database.py`
- [x] T044 Integrate chat history logging into POST `/chat` endpoint in `backend/src/api/chat_endpoints.py` (Phase 5 from plan)

**Checkpoint**: Chat history is now persisted in Neon Postgres.

---

## Phase 7: Frontend Integration

**Purpose**: Embed the chatbot UI into the Docusaurus site and connect it to the backend API.

**Independent Test**: Can be fully tested by deploying the Docusaurus site and interacting with the embedded chatbot UI, verifying correct display, query submission, and response rendering.

### Tests for Frontend Integration

- [x] T045 [P] End-to-end test for chatbot UI interaction (e.g., using Playwright or Cypress) in `e2e_tests/rag_chatbot.spec.js` (if a new file)
- [x] T046 [P] Unit test for frontend API service in `frontend/tests/unit/test_chat_service.js`

### Implementation for Frontend Integration

- [x] T047 Create Docusaurus chatbot UI components (`ChatWindow.js`, `FloatingButton.js`, `index.js`, `styles.module.css`) in `frontend/src/components/Chatbot/`
- [x] T048 Implement frontend API service (`ChatService.js`) to interact with backend endpoints (`/chat`) in `frontend/src/services/`
- [x] T049 Integrate chatbot UI components and API service into Docusaurus site (`frontend/src/theme/Root.js` or similar)
- [x] T050 Implement logic to send selected text from Docusaurus content to the backend `/chat` endpoint

**Checkpoint**: The RAG chatbot is fully integrated and functional within the Docusaurus frontend.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and overall project quality.

- [x] T051 [P] Ensure all secrets are loaded from environment variables and not hardcoded (security review)
- [x] T052 Review and improve logging verbosity and clarity across backend services
- [x] T053 Run `quickstart.md` validation, update as necessary.
- [x] T054 Create comprehensive `backend/tests/integration/test_performance.py` for latency targets (SC-001, SC-002 from research.md)
- [x] T055 Document deployment steps for backend FastAPI service (e.g., Dockerfile, CI/CD integration)
- [x] T056 Document deployment steps for frontend Docusaurus application

---

## Dependencies & Execution Order

### Phase Dependencies

-   **Setup (Phase 1)**: No dependencies - can start immediately
-   **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
-   **User Stories (Phases 3, 4, 5)**: All depend on Foundational phase completion
    -   User Story 1 (Phase 3): No dependency on other user stories.
    -   User Story 2 (Phase 4): Depends on User Story 1 (retrieval is a prerequisite).
    -   User Story 3 (Phase 5): Depends on User Story 2 (agent logic).
-   **Neon Postgres Integration (Phase 6)**: Can be largely parallel to User Stories, but integration into `/chat` endpoint depends on Phase 4.
-   **Frontend Integration (Phase 7)**: Depends on Phases 3, 4, 5 completion for backend API.
-   **Final Phase: Polish (Phase 8)**: Depends on all previous phases being substantially complete.

### User Story Dependencies

-   **User Story 1 (P1 - Phase 3)**: Can start after Foundational (Phase 2) - No dependencies on other stories.
-   **User Story 2 (P1 - Phase 4)**: Depends on User Story 1 completion (specifically the retrieval capabilities).
-   **User Story 3 (P2 - Phase 5)**: Depends on User Story 2 completion (agent reasoning logic).

### Within Each User Story

-   Tests MUST be written and FAIL before implementation.
-   Models/Clients before services.
-   Services before endpoints.
-   Core implementation before integration.

### Parallel Opportunities

-   All Setup tasks marked [P] can run in parallel.
-   All Foundational tasks marked [P] can run in parallel (within Phase 2).
-   Tests within each user story marked [P] can run in parallel.
-   Certain model/client implementations within a user story marked [P] can run in parallel.

---

## Parallel Example: User Story 1 (Phase 3)

```bash
# Launch all tests for User Story 1 together:
pytest backend/tests/unit/test_ingestion_parser.py backend/tests/unit/test_ingestion_chunker.py ...

# Launch all parallel implementation tasks for User Story 1 together:
python backend/src/ingestion/parser.py
python backend/src/ingestion/chunker.py
python backend/src/retrieval/searcher.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 1
4.  **STOP and VALIDATE**: Test User Story 1 independently (content ingestion and basic retrieval via `/search` and basic chat via `/chat` if context is directly passed without advanced agent logic)
5.  Deploy/demo if ready

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready
2.  Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3.  Add User Story 2 → Test independently → Deploy/Demo
4.  Add User Story 3 → Test independently → Deploy/Demo
5.  Proceed with Phase 6 (Postgres) and Phase 7 (Frontend) as independent increments.
6.  Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together
2.  Once Foundational is done:
    -   Developer A: User Story 1 (Content Ingestion & Basic Retrieval)
    -   Developer B: User Story 2 (Core Agent Logic & Chat Endpoint)
    -   Developer C: User Story 3 (Insufficient Content Handling)
    -   Developer D: Phase 6 (Neon Postgres)
    -   Developer E: Phase 7 (Frontend Integration)
3.  Stories/Phases complete and integrate independently based on the defined dependencies.

---

## Notes

-   [P] tasks = different files, no dependencies
-   [Story] label maps task to specific user story for traceability
-   Each user story should be independently completable and testable
-   Verify tests fail before implementing
-   Commit after each task or logical group
-   Stop at any checkpoint to validate story independently
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
