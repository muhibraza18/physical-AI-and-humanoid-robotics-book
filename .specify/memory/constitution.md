<!--
---
Sync Impact Report
---
Version Change: 1.0.0 -> 2.0.0
Modified Principles: All principles have been re-written to reflect new project scope and focus.
Added Sections:
- New Requirement: Integrated RAG Chatbot System
- Deployment Rules
- Interaction Model Requirements
- Project Goal Alignment
Removed Sections: None (principles entirely re-written, but no top-level sections removed)
Templates Requiring Updates:
- ⚠ .specify/templates/plan-template.md (Constitution Check section needs update to reflect new principles, especially RAG system integration and deployment rules)
- ⚠ .specify/templates/spec-template.md (Scope/requirements alignment with RAG system)
- ⚠ .specify/templates/tasks-template.md (Task categorization reflecting RAG system development)
Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics Constitution

This constitution defines mandatory rules that govern all future writing, planning, and execution steps for the “Physical AI & Humanoid Robotics” technical book project and all modules connected to it. The assistant must always follow this constitution when generating content, proposing structure, or answering questions.

## Core Guidance Principles
- Write neutral, academic, technically rigorous content
- Prioritize peer-reviewed, citable scientific sources
- Avoid speculation without citations
- Prefer clarity, correctness, formal terminology, and reproducibility

## Safety, Scientific Accuracy, and Verification
- All technical claims MUST be verifiable using real-world sources
- Avoid hallucinating citations, numerical claims, or research results
- Prefer missing information acknowledgement over invented detail
- Always cite original research instead of blogs or marketing sites when possible

## Mandatory Writing Voice
- Scientific, graduate-level writing style
- Avoid sensationalism, hype language, vendor advertising, or exaggerated predictions
- Use precise engineering vocabulary and clearly defined mathematical or architectural notation

## Technical Completeness Requirements
- All implementations must be grounded in actual robotics frameworks (ROS 2, Isaac, Gazebo, etc.)
- All diagrams must have captions + cite sources if derived work
- All code must be syntactically valid and consistent with targeted toolchains
- Use APA 7th style consistently for all references

## Zero-Tolerance Rules
- No plagiarism
- No hallucinated references
- No unverifiable statements presented as fact
- No rewriting research claims without attribution

## New Requirement: Integrated RAG Chatbot System
A Retrieval-Augmented Generation (RAG) chatbot MUST be developed, integrated, and embedded into the published Docusaurus site. This system must:
- Use OpenAI Agents and/or ChatKit SDKs
- Use FastAPI for backend orchestration
- Use Qdrant Cloud Free Tier as the vector database
- Provide document-grounded answers based only on book content
- Restrict knowledge to selected text fragments chosen by the user (select-and-ask interaction)
- Run inference only after retrieving relevant chunks from Qdrant embeddings
- Provide a UI experience directly inside the book
- Display as a chatbot icon (floating button) that opens an agent window interface

### Deployment Rules
- Must be functional inside the deployed Docusaurus site
- Must persist vector embeddings in Qdrant Cloud
- Must support incremental document updates (continuous ingestion)
- Must support future extension to Vision-Language-Action models referencing book content

### Interaction Model Requirements
When answering questions, the system MUST:
- Perform retrieval first
- Show or cite retrieved text in the answer
- Avoid answering if content is not available in retrieval
- Clearly state “insufficient data” if no relevant chunk is returned

## Project Goal Alignment
The RAG chatbot is considered a core deliverable of the final project.
The book and the chatbot together represent one integrated educational product, not separate projects.

**Version**: 2.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07