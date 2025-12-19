# Research Findings: Integrated RAG Chatbot

This document consolidates research findings for the "Integrated RAG Chatbot" feature, specifically addressing identified unknowns from the planning phase.

## Resolved Unknowns from Technical Context

### 1. Python Testing Framework for FastAPI Projects

-   **Decision**: `pytest` with `httpx` for API testing and `pytest-mock` for mocking.
-   **Rationale**: `pytest` is the de-facto standard for Python testing, highly extensible, and integrates well with FastAPI. `httpx` provides a robust asynchronous HTTP client suitable for testing FastAPI applications, while `pytest-mock` simplifies mocking external dependencies.
-   **Alternatives Considered**:
    -   `unittest`: Built-in, but `pytest` offers a more modern and concise syntax with better features.
    -   `FastAPI's TestClient`: Useful for basic synchronous testing, but `httpx` allows for more comprehensive asynchronous test scenarios and direct client configuration.

### 2. Typical Latency Targets for RAG Chatbots

-   **Decision**: Target maximum latency (p95) of **3 seconds** for chat responses. For retrieval (Qdrant + Cohere embedding), target maximum latency (p95) of **1 second**.
-   **Rationale**: 3 seconds for a chat response is generally acceptable for interactive AI applications, providing a balance between user experience and computational cost. 1 second for retrieval ensures that the most time-consuming part (LLM generation) has enough budget within the overall response time. These targets are achievable with efficient RAG implementations and cloud services like Cohere and Qdrant Cloud Free Tier.
-   **Alternatives Considered**:
    -   Faster targets (<1 second for chat): While desirable, this might require more expensive infrastructure or highly optimized LLMs, potentially exceeding the "Simplicity First" and "Qdrant Cloud Free Tier" constraints.
    -   Slower targets (>5 seconds): Would degrade user experience for an interactive chatbot.
