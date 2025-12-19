# Quickstart Guide: Integrated RAG Chatbot

This document provides a quick overview and initial setup instructions for the Integrated RAG Chatbot.

## Backend Setup (FastAPI)

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd physical-AI-and-humanoid-robotics/backend
    ```
2.  **Set up Python environment**:
    ```bash
    uv venv
    uv pip install -r requirements.txt
    ```
3.  **Configure environment variables**:
    Create a `.env` file in the `backend/` directory with the following (replace with actual values):
    ```
    QDRANT_URL="<your_qdrant_url>"
    QDRANT_API_KEY="<your_qdrant_api_key>"
    QDRANT_CLUSTER_ID="<your_qdrant_cluster_id>"
    DATABASE_URL="<your_neon_postgres_url>"
    COHERE_API_KEY="<your_cohere_api_key>"
    GEMINI_API_KEY="<your_gemini_api_key>"
    ```
4.  **Run the FastAPI application**:
    ```bash
    uvicorn main:app --reload
    ```
    The API documentation will be available at `http://127.0.0.1:8000/docs`.

## Frontend Setup (Docusaurus)

(Detailed instructions for embedding the chatbot UI into Docusaurus will be provided in later phases.)

1.  **Navigate to the frontend directory**:
    ```bash
    cd physical-AI-and-humanoid-robotics/frontend
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    ```
3.  **Start Docusaurus**:
    ```bash
    npm run start
    ```

## Content Ingestion

(Instructions for parsing, chunking, and embedding book content into Qdrant using standalone scripts will be provided separately.)
