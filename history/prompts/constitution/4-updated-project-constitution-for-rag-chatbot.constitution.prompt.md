---
id: 4
title: Updated project constitution for RAG chatbot
stage: constitution
date: 2025-12-17
surface: agent
model: gemini-1.5-flash
feature: none
branch: 004-fix-qdrant-rest
user: user
command: /sp.constitution Project: RAG Chatbot for AI & Humanoid Robotics BookCore Principles:- Accuracy: Answers must strictly reflect the content of the book.- Context Awareness: Use selected text from the user if provided; otherwise, retrieve relevant sections from the book’s Qdrant vector store.- Spec-Driven Consistency: Follow the Spec-Kit Plus structure for data embedding, retrieval, and agent responses.- Safety: Do not hallucinate; if information is missing, respond with "Not found in book."- Technical Compatibility: All backend code must run on Python 3.12 and be free of TensorFlow dependencies.- API Standardization: Use Cohere embeddings for vectorization, FastAPI for backend, and Qdrant Cloud Free Tier for storage.Key Standards:- Embeddings: All book text must be chunked properly and embedded with Cohere.- Retrieval: Return top-k relevant chunks based on user query if no text is selected.- Agent Responses: Combine retrieved chunks to generate coherent, accurate answers.- Format: Responses must be concise, factual, and in plain language.- Integration: Frontend chatbot must query backend via FastAPI endpoints.- Traceability: All content references must indicate chapter and section when relevant.Constraints:- No external ML libraries incompatible with Python 3.12 (e.g., TensorFlow).- Must support answering questions using only text explicitly selected by the user.- Chatbot should be able to handle multiple simultaneous queries efficiently.- Backend must be modular (embedding → storage → retrieval → agent reasoning).Success Criteria:- All answers are consistent with the book content.- Selected-text queries always take precedence.- RAG retrieval returns top-k relevant chunks accurately.- Chatbot works reliably in the Docusaurus frontend.- Fully compatible with Python 3.12 and Cohere API key workflow.
labels: ["constitution", "update"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - 
---

## Prompt

/sp.constitution Project: RAG Chatbot for AI & Humanoid Robotics BookCore Principles:- Accuracy: Answers must strictly reflect the content of the book.- Context Awareness: Use selected text from the user if provided; otherwise, retrieve relevant sections from the book’s Qdrant vector store.- Spec-Driven Consistency: Follow the Spec-Kit Plus structure for data embedding, retrieval, and agent responses.- Safety: Do not hallucinate; if information is missing, respond with "Not found in book."- Technical Compatibility: All backend code must run on Python 3.12 and be free of TensorFlow dependencies.- API Standardization: Use Cohere embeddings for vectorization, FastAPI for backend, and Qdrant Cloud Free Tier for storage.Key Standards:- Embeddings: All book text must be chunked properly and embedded with Cohere.- Retrieval: Return top-k relevant chunks based on user query if no text is selected.- Agent Responses: Combine retrieved chunks to generate coherent, accurate answers.- Format: Responses must be concise, factual, and in plain language.- Integration: Frontend chatbot must query backend via FastAPI endpoints.- Traceability: All content references must indicate chapter and section when relevant.Constraints:- No external ML libraries incompatible with Python 3.12 (e.g., TensorFlow).- Must support answering questions using only text explicitly selected by the user.- Chatbot should be able to handle multiple simultaneous queries efficiently.- Backend must be modular (embedding → storage → retrieval → agent reasoning).Success Criteria:- All answers are consistent with the book content.- Selected-text queries always take precedence.- RAG retrieval returns top-k relevant chunks accurately.- Chatbot works reliably in the Docusaurus frontend.- Fully compatible with Python 3.12 and Cohere API key workflow.

## Response snapshot

New constitution version: 3.0.0 (MAJOR bump due to significant changes in principles and project scope).

Files flagged for manual follow-up:
- ⚠ .specify/templates/plan-template.md (Constitution Check section needs update to reflect new principles, RAG system integration, and deployment rules)
- ⚠ .specify/templates/spec-template.md (Scope/requirements alignment with RAG system)
- ⚠ .specify/templates/tasks-template.md (Task categorization reflecting RAG system development)

Suggested commit message:
`docs: amend constitution to v3.0.0 (re-define principles for RAG Chatbot project)`

## Outcome

- ✅ Impact: Constitution updated with new RAG chatbot principles.
- 🧪 Tests: No new tests were created, but existing templates need review.
- 📁 Files: One file (.specify/memory/constitution.md) was modified.
- 🔁 Next prompts: User will likely address the manual follow-up items.
- 🧠 Reflection: The constitution was successfully updated based on the user's detailed input, involving a major version bump. The process highlighted the need for robust handling of shell script execution across different OS and reliance on agent-native tools for critical tasks like PHR creation.

## Evaluation notes (flywheel)

- Failure modes observed: PHR script failed due to OS incompatibility (bash script on PowerShell).
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Improve OS compatibility for PHR creation script or fully deprecate shell script for agent-native PHR creation.
